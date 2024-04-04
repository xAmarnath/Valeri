import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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",
}

json_data = {
    "model": "gpt-3.5-turbo-16k-0613",
    "messages": [
        {
            "role": "user",
            "content": "Hi",
        },
    ],
}

response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=json_data,
    verify=False,
)

with open("essay.txt", "wb") as f:
    f.write(response.content)

#   curl https://api.openai.com/v1/images/generations \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer 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" \
# -d '{
#  "model": "dall-e-3",
# "prompt": "a donkey riding a bicycle",
# "n": 1,
# "size": "1024x1024"
# }'
