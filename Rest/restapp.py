import pymysql
from flask import Flask, g, request
from flask_mysqldb import MySQL
from settings import *

app = Flask(__name__)
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_DB'] = MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/users_list/<id>', methods=['GET'])
def get_user(id):
	cursor = mysql.connection.cursor()
	try:
		cursor.execute('''SELECT %s FROM %s WHERE %s = %d''' % (MYSQL_USERNAME_COLUMN_NAME, MYSQL_TALBE_NAME, MYSQL_TELEGRAM_ID_COLUMN_NAME, int(id)))
		result = cursor.fetchone()
		if result:
			return 'True\n{}'.format(result['name'])
		else:
			return 'False'
	except:
		return 'False'

if __name__ == '__main__':
	app.run(host = REST_HOST, port = REST_PORT)
