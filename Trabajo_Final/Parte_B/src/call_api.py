import requests


BASE_URL = 'http://127.0.0.1'
PORT = 7860
ENDPOINT = '/prediccion'

data = {
    "orderAmount": 26.0,
    "orderState": "fulfilled",
    "paymentMethodRegistrationFailure": "True",
    "paymentMethodType": "bitcoin",
    "paymentMethodProvider": "VISA 16 digit",
    "paymentMethodIssuer": "Solace Banks",
    "transactionFailed": "False",
    "emailDomain": "com",
    "emailProvider": "yahoo",
    "customerIPAddressSimplified": "only_letters",
    "sameCity": "no"
}

response = requests.post(f'{BASE_URL}:{PORT}{ENDPOINT}', json=data)
print(response.json())
