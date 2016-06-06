import requests
from lxml import html

session_requests = requests.session()

login_url = "https://stackoverflow.com/users/login"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
token = list(set(tree.xpath("//input[@name='fkey']/@value")))[0]

print token

credentials = {
    "email": "msaadq94@gmail.com",
    "password": "samplepasswordforCarbyne",
    "fkey": token
}

result = session_requests.post(
    login_url,
    data=credentials,
    headers=dict(referer=login_url)
)

f = open("website.html", "w")
f.write(result.content)
f.close()

print result.ok
