import time
import requests

url = 'https://api.divar.ir/v8/web-search/1/apartment-sell'

json = {"json_schema": {"category": {"value": "apartment-sell"},
                        "districts": {"vacancies": ["951", "122", "123", "134", "946", "952", "953"]},
                        "cities": ["1"]}, "last-post-date": 1685052034513005}

headers = {"Content-Type": "application/json"}

res = requests.post(url, json=json, headers=headers)
data = res.json()
last_post_date = data['last_post_date']

list_of_tokens = []

count = 0
while True:
    time.sleep(1)
    json = {"json_schema": {"category": {"value": "apartment-sell"},
                            "districts": {"vacancies": ["951", "122", "123", "134", "946", "952", "953"]},
                            "cities": ["1"]}, "last-post-date": last_post_date}
    res = requests.post(url, json=json, headers=headers)
    data = res.json()
    last_post_date = data['last_post_date']

    for widget in data['web_widgets']['post_list']:
        token = widget['data']['token']
        list_of_tokens.append(token)
        count += 1
        print(token)

    if count >= 1890:
        break
print(list_of_tokens)
txt_file = open('Tokens.txt', 'w', encoding='utf-8')
txt_file.write(','.join(list_of_tokens))
txt_file.close()
