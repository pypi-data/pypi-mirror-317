import requests

def send_bill(owner_id, name, summ):
    url = 'http://194.87.94.28:81/add_bill'
    payload = {
        'owner_id': owner_id,
        'name': name,
        'sum': summ
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data['link']
    else:
        print("Ошибка при отправке запроса:", response.status_code)

def check_bill(id):
    url = 'http://194.87.94.28:81/check_bill'
    payload = {
        'id': id
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data['status']
    else:
        return False

print(check_bill(5495))