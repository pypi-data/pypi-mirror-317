import requests

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "app_version": "9.0.0",
    "appid": "30004",
    "appsiteid": "0",
    "channel": "official",
    "device_brand": "Linux_Chrome_131.0.0.0",
    "device_id": "64a8c630-acc2-11ef-aa5e-9f6ee3baa1a5",
    "lang": "ru-RU",
    "mainappid": "10009",
    "origin": "https://bingx.paycat.com",
    "platformid": "30",
    "priority": "u=1, i",
    "referer": "https://bingx.paycat.com/",
    "reg_channel": "official",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sign": "C2F082935161A29256CDD98F2E33FBE3C9B2C0864A6FBCB1881013CBE6272AC8",
    "timestamp": "1734637010958",
    "timezone": "3",
    "traceid": "3e38538d69fb43c9a009ea1fc00a9b8f",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

params = {
    "fiat": "RUB",
}

response = requests.get("https://api-app.we-api.com/api/c2c/v1/advert/payment/list", params=params, headers=headers)

print(i for i in response.json()["data"]["paymentMethodList"])
