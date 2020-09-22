"""Проверка наличия юзера в базе"""
import requests
import json

url = "http://127.0.0.1:5000/users_list"

users_list = json.loads(requests.get(url).text)

def check(id) -> bool: # Проверка на наличие в списке
	for user in users_list:
		if user["id"] == id:
			return True
	return False

print(check("Pooodwdwadd"))
print(check("ABC987655"))