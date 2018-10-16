import requests
res=requests.get('https://ipinfo.io/')
print(res.text)
