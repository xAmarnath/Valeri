import time
from platform import platform

import psutil
import speedtest

from ._config import StartTime
from ._handler import newMsg
from ._helpers import human_readable_size
from .db.db import get_db_stats


@newMsg(pattern="speedtest")
async def _speedtest(e):
    msg = await e.reply("Testing internet speed...")
    st = speedtest.Speedtest()
    download = st.download()
    upload = st.upload()
    ping = st.results.ping
    server = st.results.server.get("name", "Unknown")
    isp = st.results.client.get("isp", "Unknown")
    ip = st.results.client.get("ip", "Unknown")
    country = st.results.client.get("country", "Unknown")
    result = (
        f"**Speedtest Results:**\n\n"
        f"**Download:** `{human_readable_size(download, True)}`\n"
        f"**Upload:** `{human_readable_size(upload, True)}`\n"
        f"**Ping:** `{ping} ms`\n"
        f"**Server:** `{server}`\n"
        f"**ISP:** `{isp}`\n"
        f"**IP:** `{ip}`\n"
        f"**Country:** `{country}`"
    )
    await msg.edit(result)


@newMsg(pattern="ping")
async def _ping(e):
    starttime = time.time()
    msg = await e.reply("Pinging...")
    endtime = time.time()
    ping = round((endtime - starttime) * 1000, 2)
    uptime = round(time.time() - StartTime, 2)
    result = f"**Ping:** `{ping} ms`\n" f"**Uptime:** `{uptime} s`"
    await msg.edit(result)


@newMsg(pattern="system")
async def _system(e):
    msg = await e.reply("Getting system info...")
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    cores = psutil.cpu_count()
    total_ram = psutil.virtual_memory().total
    free_ram = psutil.virtual_memory().free
    total_disk = psutil.disk_usage("/").total
    free_disk = psutil.disk_usage("/").free
    operating_system = platform()
    network = psutil.net_if_addrs()["Ethernet"][0].address if psutil.net_if_addrs().get("Ethernet") else "Unknown controller"
    db_free, db_total = get_db_stats()
    result = (
        f"**System Info:**\n\n"
        f"**CPU:** `{cpu}%`\n"
        f"**Memory:** `{mem}%`\n"
        f"**Disk:** `{disk}%`\n"
        f"**Cores:** `{cores}`\n"
        f"**RAM:** `{human_readable_size(total_ram)}`\n"
        f"**Free RAM:** `{human_readable_size(free_ram)}`\n"
        f"**Total Disk:** `{human_readable_size(total_disk)}`\n"
        f"**Free Disk:** `{human_readable_size(free_disk)}`\n"
        f"**Operating System:** `{operating_system}`\n"
        f"**Network:** `{network}`\n"
        f"**Database:** `{human_readable_size(db_free)}` of `{human_readable_size(db_total)}`"
    )

    await msg.edit(result)
