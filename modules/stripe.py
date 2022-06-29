from requests import get
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
        buttons = Button.url("Payment Page", "https://google.com")
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
