"""Запуск Rest"""
from flask import Flask, json, jsonify

app = Flask(__name__)

with open('users_list.json') as f:
    users_list = json.load(f)

@app.route('/users_list', methods=['GET'])
def get_list():
	return jsonify(users_list)

if __name__ == '__main__':
	app.run()