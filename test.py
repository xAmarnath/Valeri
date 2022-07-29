import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

response = requests.get('https://hackthebox.store/cart/30942215241867:1', headers=headers)

print(response.url)
#req1