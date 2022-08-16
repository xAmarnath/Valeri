import requests


def digital_ocean(cc, exp_mo, exp_year, cvv):

    headers_s = {
        "authority": "api.stripe.com",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "accept": "application/json",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://js.stripe.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://js.stripe.com/",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    data = f"card[name]=RoseLoverX&card[address_line1]=4310+Northwest+215th+Street&card[address_line2]=&card[address_city]=Miami+Gardens&card[address_state]=FL&card[address_zip]=33055&card[address_country]=US&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={exp_mo}&card[exp_year]={exp_year}&guid=2502e27c-c4db-4af8-a601-f1d6983af82ef33d6c&muid=663aa3fc-2f3b-4fd3-b435-8dbbaa93cb3a9928fc&sid=13500aeb-2587-408c-b1f4-0cfe362342e0e75bed&payment_user_agent=stripe.js%2F70a10e913%3B+stripe-js-v3%2F70a10e913&time_on_page=225994&key=pk_live_ckPnmJJZTFKgKGv6RihxsV8g"

    response = requests.post(
        "https://api.stripe.com/v1/tokens", headers=headers_s, data=data
    )
    id = response.json()["id"]

    cookies = {
        "last_landing_page_timestamp": "1659078871362",
        "optimizelyEndUserId": "oeu1659078872536r0.8590729264374446",
        "ajs_anonymous_id": "541586b0-8e75-4919-a3a0-2a07ff2de44d",
        "cookieconsent_status": "dismiss",
        "_gcl_au": "1.1.1138764183.1659078880",
        "_rdt_uuid": "1659078880098.15c4bf9a-344a-4f3c-a35e-2bab6f80fd01",
        "_tt_enable_cookie": "1",
        "_ttp": "aa22443f-41db-47ab-9180-61b54d7eac47",
        "_fbp": "fb.1.1659078880793.1391522571",
        "__qca": "P0-1192495071-1659078881055",
        "_gid": "GA1.2.1300332890.1659432725",
        "_gac_UA-26573244-1": "1.1659432725.EAIaIQobChMI_97KvOyn-QIV5IxLBR12WwnMEAEYASAAEgLczvD_BwE",
        "_ga": "GA1.1.1603318136.1659078873",
        "_gcl_aw": "GCL.1659432725.EAIaIQobChMI_97KvOyn-QIV5IxLBR12WwnMEAEYASAAEgLczvD_BwE",
        "cebs": "1",
        "_ce.s": "v~ead83e60b42267d4f94223a23128a5aa5d7f1abd~vpv~1",
        "cebsp": "1",
        "_ga": "GA1.3.1603318136.1659078873",
        "_gid": "GA1.3.1300332890.1659432725",
        "_gac_UA-26573244-1": "1.1659432725.EAIaIQobChMI_97KvOyn-QIV5IxLBR12WwnMEAEYASAAEgLczvD_BwE",
        "__ssid": "5ec5cc6bebcab3e00ae60792da3598a",
        "_digitalocean2_session_v4": "WDRlYml4aEVhdWVtSXF5Um9XZmVTM1Vrc2k0ZXBBckVmTmEvaHM3WWVZWWtrK3B5ckhlZkUxanZLTlhBRVlvelUyTWpoR25KVzVVcTlHMWVZcExmd2ZFSVZCL3VQbytGRDRVNDVRaTRzNlZQMW1TalZDWFV3VUJxYmc2ck5ZSVFoSXhLSjZxOW1PU0R3WFB1RVYxWkNXN05OSU52L2J6Qi9MUVp4RXhYTWo0S2V1M3UrMnhQZVZoRWt0WXhOMi9ZMmJYYWZQNGxnVC9mYjcwditSaEtyY3l4M05SaEl2Yy9wb1lhUFVzMzQ3MHFoTXhyN0F4SEZhYU9lYXVOY3JHaVB4T3BtS2J1c2Z0MG1TYUlTaU04T0FUR2h5SU53Qm12M1d1amxpK3pKNXpMd1IyOFNvL0dOc3liTk5ucDJGSXl3K2xVK3pibmo4L2dnOVFzWnptZVREYkZOaEdLa1BOTkRlbGhLZnk0dFZWdVUrR0FXTFpqalJyWHo2bWxrVzZjbE9KcjkyeVhMWkpKMnpCYUkvaDdjUlpkOGhkTzJjd2tvMEFEck9aOU5WUT0tLW8reGxQZmdZdmdHaU9Ya0ZQUjZvbVE9PQ==--d4a9a3c5043ef50a10ea81392adc2d638347c5bf",
        "sessionID": "5173778",
        "ajs_user_id": "72408f7e-c9fd-4c01-96ae-429c7b6b76ef",
        "_digitalocean_initial_conversion": "72408f7e-c9fd-4c01-96ae-429c7b6b76ef",
        "_clck": "uaot4d|1|f3o|0",
        "__stripe_mid": "663aa3fc-2f3b-4fd3-b435-8dbbaa93cb3a9928fc",
        "__stripe_sid": "13500aeb-2587-408c-b1f4-0cfe362342e0e75bed",
        "_flash": "fc.eyJzZXZlcml0eSI6Im5vdGljZSIsIm1lc3NhZ2UiOiJZb3VyIGVtYWlsIHdhcyBjb25maXJtZWQuIn0=",
        "_uetsid": "2b5d0390124611ed80b6d3495537bef5",
        "_uetvid": "2b5eef20124611ed87b7531fc7a3114f",
        "_ga_TYR2BYTLL0": "GS1.1.1659432724.2.1.1659432938.0",
        "__cf_bm": "ZU3zPwtEpkGMYwcsVmyIZ_pjXqTsQFUDZlO8bq8tfdo-1659433034-0-AXmMrPdiDejFwa7eGOvGdrkyHl2GifmP/Y17ByFotjdNraTbDulKeYy66LtnmW6mwyWPTTBtNhnpe/D6vuOVZKdDau4FpFztLOLBjt07tDwA",
    }

    headers = {
        "authority": "cloud.digitalocean.com",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "apollographql-client-name": "mod-account-settings",
        "x-context-urn": "do:team:37c312d0-83d3-4e4b-9f05-5bd62573a7a4",
        "x-add-card-origin": "onboarding",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        # Already added when you pass json=
        # 'content-type': 'application/json',
        "accept": "*/*",
        "apollographql-client-version": "1.0",
        "origin": "https://cloud.digitalocean.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://cloud.digitalocean.com/welcome?i=72408f",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        # Requests sorts cookies= alphabetically
        # 'cookie': 'last_landing_page_timestamp=1659078871362; optimizelyEndUserId=oeu1659078872536r0.8590729264374446; ajs_anonymous_id=541586b0-8e75-4919-a3a0-2a07ff2de44d; cookieconsent_status=dismiss; _gcl_au=1.1.1138764183.1659078880; _rdt_uuid=1659078880098.15c4bf9a-344a-4f3c-a35e-2bab6f80fd01; _tt_enable_cookie=1; _ttp=aa22443f-41db-47ab-9180-61b54d7eac47; _fbp=fb.1.1659078880793.1391522571; __qca=P0-1192495071-1659078881055; _gid=GA1.2.1300332890.1659432725; _gac_UA-26573244-1=1.1659432725.EAIaIQobChMI_97KvOyn-QIV5IxLBR12WwnMEAEYASAAEgLczvD_BwE; _ga=GA1.1.1603318136.1659078873; _gcl_aw=GCL.1659432725.EAIaIQobChMI_97KvOyn-QIV5IxLBR12WwnMEAEYASAAEgLczvD_BwE; cebs=1; _ce.s=v~ead83e60b42267d4f94223a23128a5aa5d7f1abd~vpv~1; cebsp=1; _ga=GA1.3.1603318136.1659078873; _gid=GA1.3.1300332890.1659432725; _gac_UA-26573244-1=1.1659432725.EAIaIQobChMI_97KvOyn-QIV5IxLBR12WwnMEAEYASAAEgLczvD_BwE; __ssid=5ec5cc6bebcab3e00ae60792da3598a; _digitalocean2_session_v4=WDRlYml4aEVhdWVtSXF5Um9XZmVTM1Vrc2k0ZXBBckVmTmEvaHM3WWVZWWtrK3B5ckhlZkUxanZLTlhBRVlvelUyTWpoR25KVzVVcTlHMWVZcExmd2ZFSVZCL3VQbytGRDRVNDVRaTRzNlZQMW1TalZDWFV3VUJxYmc2ck5ZSVFoSXhLSjZxOW1PU0R3WFB1RVYxWkNXN05OSU52L2J6Qi9MUVp4RXhYTWo0S2V1M3UrMnhQZVZoRWt0WXhOMi9ZMmJYYWZQNGxnVC9mYjcwditSaEtyY3l4M05SaEl2Yy9wb1lhUFVzMzQ3MHFoTXhyN0F4SEZhYU9lYXVOY3JHaVB4T3BtS2J1c2Z0MG1TYUlTaU04T0FUR2h5SU53Qm12M1d1amxpK3pKNXpMd1IyOFNvL0dOc3liTk5ucDJGSXl3K2xVK3pibmo4L2dnOVFzWnptZVREYkZOaEdLa1BOTkRlbGhLZnk0dFZWdVUrR0FXTFpqalJyWHo2bWxrVzZjbE9KcjkyeVhMWkpKMnpCYUkvaDdjUlpkOGhkTzJjd2tvMEFEck9aOU5WUT0tLW8reGxQZmdZdmdHaU9Ya0ZQUjZvbVE9PQ==--d4a9a3c5043ef50a10ea81392adc2d638347c5bf; sessionID=5173778; ajs_user_id=72408f7e-c9fd-4c01-96ae-429c7b6b76ef; _digitalocean_initial_conversion=72408f7e-c9fd-4c01-96ae-429c7b6b76ef; _clck=uaot4d|1|f3o|0; __stripe_mid=663aa3fc-2f3b-4fd3-b435-8dbbaa93cb3a9928fc; __stripe_sid=13500aeb-2587-408c-b1f4-0cfe362342e0e75bed; _flash=fc.eyJzZXZlcml0eSI6Im5vdGljZSIsIm1lc3NhZ2UiOiJZb3VyIGVtYWlsIHdhcyBjb25maXJtZWQuIn0=; _uetsid=2b5d0390124611ed80b6d3495537bef5; _uetvid=2b5eef20124611ed87b7531fc7a3114f; _ga_TYR2BYTLL0=GS1.1.1659432724.2.1.1659432938.0; __cf_bm=ZU3zPwtEpkGMYwcsVmyIZ_pjXqTsQFUDZlO8bq8tfdo-1659433034-0-AXmMrPdiDejFwa7eGOvGdrkyHl2GifmP/Y17ByFotjdNraTbDulKeYy66LtnmW6mwyWPTTBtNhnpe/D6vuOVZKdDau4FpFztLOLBjt07tDwA',
    }

    json_data = {
        "operationName": "submitPaymentMethod",
        "variables": {
            "paymentMethodRequest": {
                "payment_profile": {
                    "first_name": "",
                    "last_name": "RoseLoverX",
                    "address": "4310 Northwest 215th Street",
                    "city": "Miami Gardens",
                    "state": "FL",
                    "zip": "33055",
                    "country": "US",
                    "is_default": True,
                },
                "payment_method_id": id,
            },
        },
        "query": "mutation submitPaymentMethod($paymentMethodRequest: PaymentMethodCreateRequest!) {\n  createPaymentMethodV2(paymentMethodRequest: $paymentMethodRequest) {\n    intent_secret\n    stripe_error\n    error {\n      messages\n      __typename\n    }\n    __typename\n  }\n}\n",
    }

    response = requests.post(
        "https://cloud.digitalocean.com/graphql",
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    try:
        error = response.json()["data"]["createPaymentMethodV2"]["error"]
        msg = error["messages"]
        if msg:
            return msg
    except:
        pass
    intent_secret = response.json()["data"]["createPaymentMethodV2"]["intent_secret"]
    intent = intent_secret.split("_secret")[0]

    params = {
        "key": "pk_live_ckPnmJJZTFKgKGv6RihxsV8g",
        "is_stripe_sdk": "false",
        "client_secret": intent_secret,
    }

    response = requests.get(
        f"https://api.stripe.com/v1/payment_intents/{intent}",
        params=params,
        headers=headers_s,
    )
    resp = response.json()
    if "status" in resp:
        if resp["status"] == "source_action_required":
            return "#3D Secure required"
    return "unknown status"


print(digital_ocean(5262053007987002, "08", 23, "040"))
