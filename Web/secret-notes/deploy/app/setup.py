import requests
from uuid import uuid4
import os
url = "http://0.0.0.0:5000"
details = {
    "username": "25d1848d3fa54f4aa2404c03b63f11f9",
    "name": uuid4().hex,
    "password": "32c53b17fb164f86a0df9b5b188edf95",
}
session = requests.Session()

response = session.post(url + "/register", data=details)
login_data = {
    "username": details["username"],
    "password": details["password"],
}
response = session.post(url + "/login", data=login_data)

flag_data = {
    "title": "FLAG",
    "content": os.getenv("FLAG") or "ironCTF{master}",
}

response = session.post(url + "/create", data=flag_data)
print("Admin details", details)