import requests
from ._handler import new_cmd
from ._config import OPENAI_API_KEY

if OPENAI_API_KEY:

    GPT_CONV = []

    @new_cmd(pattern="gpt")
    async def gpt(e):
        async with e.client.action(e.chat_id, "typing"):
            try:
                q = e.text.split(" ", 1)[1]
            except IndexError:
                return await e.reply("Give me a prompt.")

            resp = chatgpt_prompt(q)

            if not resp:
                return await e.reply("An error occurred.")

            await e.reply(resp)

    @new_cmd(pattern="dalle")
    async def dalle(e):
        try:
            q = e.text.split(" ", 1)[1]
        except IndexError:
            return await e.reply("Give me a prompt.")

        resp = dalle_prompt(q)

        if not resp:
            return await e.reply("An error occurred.")

        try:
            await e.reply(file=resp)
        except:
            await e.reply(resp)

    def chatgpt_prompt(prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(OPENAI_API_KEY),
        }

        GPT_CONV.append({
            "role": "user",
            "content": prompt,
        })

        total_len = [len(x["content"]) for x in GPT_CONV]

        while sum(total_len) > 4096:
            GPT_CONV.pop(0)
            total_len.pop(0)

        json_data = {
            "model": "gpt-3.5-turbo-16k-0613",
            "messages": GPT_CONV,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
            timeout=10,
        )

        resp = response.json()

        try:
            GPT_CONV.append({
                "role": "bot",
                "content": resp["choices"][0]["message"]["content"],
            })

            return resp["choices"][0]["message"]["content"]
        except:
            return "An error occurred."

    def dalle_prompt(prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(OPENAI_API_KEY),
        }

        json_data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
        }

        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=json_data,
            timeout=40,
        )
        
        print(response.json())

        return response.json()["output"]["url"]


#   curl https://api.openai.com/v1/images/generations \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer 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" \
# -d '{
#  "model": "dall-e-3",
# "prompt": "a donkey riding a bicycle",
# "n": 1,
# "size": "1024x1024"
# }'
