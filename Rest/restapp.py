import pymysql
from flask import Flask, g, request
from flask_mysqldb import MySQL
from settings import *

app = Flask(__name__)
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'smartuniversity_users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/users_list/<id>', methods=['GET'])
def get_user(id):
	cursor = mysql.connection.cursor()
	cursor.execute('''SELECT name FROM users WHERE telegram_id = %d''' % int(id))
	result = cursor.fetchone()
	if result:
		return 'True\n{}'.format(result['name'])
	else:
		return 'False'

if __name__ == '__main__':
	app.run(host = REST_HOST, port = REST_PORT)
