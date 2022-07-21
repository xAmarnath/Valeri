"""Fast Upload Methods"""

import asyncio
import hashlib
import io
import logging
import math
import os

from telethon import functions, helpers, types, utils
from telethon.network import MTProtoSender
from telethon.tl.alltlobjects import LAYER
from telethon.tl.functions import InvokeWithLayerRequest

log = logging.getLogger("transfers")


class DownloadSender:
    """
    DownloadSender.__next__ = DownloadSender.next
    """

    def __init__(
        self,
        sender,
        file,
        offset,
        limit,
        stride,
        count,
    ):
        self.sender = sender
        self.request = functions.upload.GetFileRequest(file, offset=offset, limit=limit)
        self.stride = stride
        self.remaining = count

    async def next(self):
        """
        if self.remaining:
            self.remaining -= 1
            return await self.sender.send(self.request)
        """
        if not self.remaining:
            return None
        result = await self.sender.send(self.request)
        self.remaining -= 1
        self.request.offset += self.stride
        return result.bytes

    def disconnect(self):
        """disconnect the sender"""
        return self.sender.disconnect()


class UploadSender:
    """UploadSender.__aiter__ = UploadSender.next"""

    def __init__(
        self,
        sender,
        file_id: int,
        part_count: int,
        big: bool,
        index: int,
        stride: int,
        loop,
    ) -> None:
        self.sender = sender
        self.part_count = part_count
        if big:
            self.request = functions.upload.SaveBigFilePartRequest(
                file_id, index, part_count, b""
            )
        else:
            self.request = functions.upload.SaveFilePartRequest(file_id, index, b"")
        self.stride = stride
        self.previous = None
        self.loop = loop

    async def next(self, data: bytes) -> None:
        """
        load next part of the file
        """
        if self.previous:
            await self.previous
        self.previous = asyncio.create_task(self._next(data))

    async def _next(self, data: bytes) -> None:
        self.request.bytes = data
        log.debug("Sending file part %d/%d", self.request.file_part, self.part_count)
        await self.sender.send(self.request)
        self.request.file_part += self.stride

    async def disconnect(self) -> None:
        """disconnect the sender"""
        if self.previous:
            await self.previous
        return await self.sender.disconnect()


class ParallelTransferrer:
    """ParallelTransferrer(sender, file, offset, limit, stride, count)"""

    def __init__(self, client, dc_id=None):
        self.client = client
        self.loop = self.client.loop
        self.dc_id = dc_id or self.client.session.dc_id
        self.auth_key = (
            None
            if dc_id and self.client.session.dc_id != dc_id
            else self.client.session.auth_key
        )
        self.senders = None
        self.upload_ticker = 0

    async def _cleanup(self):
        """Cleanup the senders."""
        await asyncio.gather(*(sender.disconnect() for sender in self.senders))
        self.senders = None

    @staticmethod
    def _get_connection_count(
        file_size: int, max_count: int = 20, full_size: int = 100 * 1024 * 1024
    ) -> int:
        """
        Return the number of connections needed to download the given file.
        """
        if file_size > full_size:
            return max_count
        return math.ceil((file_size / full_size) * max_count)

    async def _init_download(
        self, connections: int, file, part_count: int, part_size: int
    ) -> None:
        """Initialize the download."""
        minimum, remainder = divmod(part_count, connections)

        def get_part_count() -> int:
            nonlocal remainder
            if remainder > 0:
                remainder -= 1
                return minimum + 1
            return minimum

        self.senders = [
            await self._create_download_sender(
                file, 0, part_size, connections * part_size, get_part_count()
            ),
            *await asyncio.gather(
                *(
                    self._create_download_sender(
                        file, i, part_size, connections * part_size, get_part_count()
                    )
                    for i in range(1, connections)
                )
            ),
        ]

    async def _create_download_sender(
        self,
        file,
        index: int,
        part_size: int,
        stride: int,
        part_count: int,
    ) -> DownloadSender:
        """Create a DownloadSender for the given file and index."""
        return DownloadSender(
            await self._create_sender(),
            file,
            index * part_size,
            part_size,
            stride,
            part_count,
        )

    async def _init_upload(
        self,
        connections: int,
        file_id: int = None,
        part_count: int = None,
        big: bool = None,
    ) -> None:
        """Initialize the upload senders."""
        self.senders = [
            await self._create_upload_sender(file_id, part_count, big, 0, connections),
            *await asyncio.gather(
                *(
                    self._create_upload_sender(file_id, part_count, big, i, connections)
                    for i in range(1, connections)
                )
            ),
        ]

    async def _create_upload_sender(
        self, file_id: int, part_count: int, big: bool, index: int, stride: int
    ) -> UploadSender:
        """Returns an UploadSender"""
        return UploadSender(
            await self._create_sender(),
            file_id,
            part_count,
            big,
            index,
            stride,
            loop=self.loop,
        )

    async def _create_sender(self) -> MTProtoSender:
        datacenter = await self.client._get_dc(self.dc_id)
        sender = MTProtoSender(self.auth_key, loggers=self.client._log)
        await sender.connect(
            self.client._connection(
                datacenter.ip_address,
                datacenter.port,
                datacenter.id,
                loggers=self.client._log,
                proxy=self.client._proxy,
            )
        )
        if not self.auth_key:
            log.debug("Export auth key to DC %d", self.dc_id)
            auth = await self.client(
                functions.auth.ExportAuthorizationRequest(self.dc_id)
            )
            self.client._init_request.query = functions.auth.ImportAuthorizationRequest(
                id=auth.id, bytes=auth.bytes
            )
            req = InvokeWithLayerRequest(LAYER, self.client._init_request)
            await sender.send(req)
            self.auth_key = sender.auth_key
        return sender

    async def init_upload(
        self,
        file_id: int,
        file_size: int = None,
        part_size_kb=None,
        connection_count=None,
    ) -> tuple[int, int, bool]:
        """Initialize an upload."""
        connection_count = connection_count or self._get_connection_count(file_size)
        part_size = (part_size_kb or utils.get_appropriated_part_size(file_size)) * 1024
        part_count = (file_size + part_size - 1) // part_size
        is_large = file_size > 10 * 1024 * 1024
        await self._init_upload(connection_count, file_id, part_count, is_large)
        return part_size, part_count, is_large

    async def upload(self, part: bytes) -> None:
        """Uploads a part of the file."""
        await self.senders[self.upload_ticker].next(part)
        self.upload_ticker = (self.upload_ticker + 1) % len(self.senders)

    async def finish_upload(self) -> None:
        """Waits for all uploads to finish."""
        await self._cleanup()

    async def download(
        self,
        file,
        file_size: int,
        part_size_kb: float,
        connection_count: int,
    ):
        """Download a file from Telegram."""
        connection_count = connection_count or self._get_connection_count(file_size)
        part_size = (part_size_kb or utils.get_appropriated_part_size(file_size)) * 1024
        part_count = math.ceil(file_size / part_size)
        log.debug(
            "Starting parallel download: %s parts of %s bytes",
            part_count,
            file_size,
            extra={"file_id": file.id},
        )
        await self._init_download(connection_count, file, part_count, part_size)

        part = 0
        while part < part_count:
            tasks = []
            for sender in self.senders:
                tasks.append(asyncio.create_task(sender.next()))
            for task in tasks:
                data = await task
                if not data:
                    break
                yield data
                part += 1

        log.debug("Parallel download finished, cleaning up connections")
        await self._cleanup()


def stream_file(file_to_stream, chunk_size=1024):
    """Generator that yields chunks of a file."""
    while True:
        data_read = file_to_stream.read(chunk_size)
        if not data_read:
            break
        yield data_read


async def internal_transfer_to_telegram(client, response, filename="upload"):
    """Transfers a file to telegram"""
    file_id = helpers.generate_random_long()
    file_size = os.path.getsize(response.name)
    hash_md5 = hashlib.md5()
    uploader = ParallelTransferrer(client)
    part_size, part_count, is_large = await uploader.init_upload(file_id, file_size)
    buffer = bytearray()
    for data in stream_file(response, 2048):
        if not is_large:
            hash_md5.update(data)
        if len(buffer) == 0 and len(data) == part_size:
            await uploader.upload(data)
            continue
        new_len = len(buffer) + len(data)
        if new_len >= part_size:
            cutoff = part_size - len(buffer)
            buffer.extend(data[:cutoff])
            await uploader.upload(bytes(buffer))
            buffer.clear()
            buffer.extend(data[cutoff:])
        else:
            buffer.extend(data)
    if len(buffer) > 0:
        await uploader.upload(bytes(buffer))
    await uploader.finish_upload()
    if is_large:
        return types.InputFileBig(file_id, part_count, filename)
    return (types.InputFile(file_id, part_count, filename, hash_md5.hexdigest()),)


async def upload_file(client, file):
    """Uploads a file to telegram"""
    if isinstance(file, str):
        try:
            with open(file, "rb") as bfile:
                return await internal_transfer_to_telegram(
                    client, bfile, os.path.basename(file)
                )
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"File {file} not found") from exc
    if isinstance(file, io.IOBase):
        return await internal_transfer_to_telegram(client, file)
    if isinstance(file, bytes):
        file = io.BytesIO(file)
    if isinstance(file, io.BytesIO):
        return await internal_transfer_to_telegram(client, file, file.name)
    raise ValueError("Invalid file type")


async def progress_callback(current, total, message):
    """Callback for the progress of the upload."""
    if total == 0:
        return
    progress = int(current * 100 / total)
    if current % 4 == 0:
        return
    await message.edit(f"Uploading... {progress}%")
