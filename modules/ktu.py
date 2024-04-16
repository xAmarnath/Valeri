import asyncio
import warnings

import requests

warnings.filterwarnings("ignore")
from ._config import bot


async def fetch_and_check_results():
    while True:
        json_data = {
            "program": "1",
        }

        response = requests.post(
            "https://api.ktu.edu.in/ktu-web-service/anon/result",
            json=json_data,
            verify=False,
        )

        res = response.json()
        res_valid = [
            {
                "examDefId": x["examDefId"],
                "resultName": x["resultName"],
                "schemeId": x["schemeId"],
            }
            for x in res
            if x["resultName"] != ""
        ]

        dob = "2003-11-28"
        rollno = "AJC22CS034"

        for x in res_valid:
            name = x["resultName"]
            if ("(R, S)" in name or "(R,S)" in name) and "S3" in name:
                print(f"Fetching {name}")

                req = {
                    "examDefId": x["examDefId"],
                    "schemeId": x["schemeId"],
                    "dateOfBirth": dob,
                    "registerNo": rollno,
                }

                response = requests.post(
                    "https://api.ktu.edu.in/ktu-web-service/anon/individualresult",
                    json=req,
                    verify=False,
                )

                res = response.json()

                import io
                import json

                with io.open(f"{name}.json", "w", encoding="utf-8") as f:
                    json.dump(res, f, ensure_ascii=False, indent=4)

                    try:
                        await bot.send_message(
                            "@roseloverx",
                            f"Results for {name} fetched and saved to file",
                        )
                        await bot.send_file("@roseloverx", f"{name}.json")
                    except:
                        pass
                    return

        await asyncio.sleep(30)  # 30 seconds
