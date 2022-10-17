import requests

response = requests.post(
    'http://127.0.0.1:5000/advertisement/',
    json={'header':'Куплю пианино', 'a_text':'Продам баян', 'owner_adv':'Иванова Иван'}
)
print(response.text)

response = requests.get(
    'http://127.0.0.1:5000/advertisement/'
)

print(response.text)

response = requests.delete(
    'http://127.0.0.1:5000/advertisement/',
    json={'id':'74'}
)

print(response.text)



