import requests
url = 'http://127.0.0.1:8000/api/v1/hello'
r = requests.post('http://127.0.0.1:8000/api/v1/api_token/', data={'username': 'username', 'password': 'password'})
r = requests.get(url, headers={'Authorization': 'Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'})
