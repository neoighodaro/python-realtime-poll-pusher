from flask import Flask, render_template, request, jsonify, make_response
from dbsetup import create_connection, select_all_items, update_item
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
pusher = Pusher(app_id=u'109121', key=u'3a2a219040583d8ee1b4', secret=u'09b8686698072e44711d', cluster=u'mt1')
database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()

def main():
	global conn, c

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/vote', methods=['POST'])
def vote():
	data = simplejson.loads(request.data)
	update_item(c, [data['member']])
	output = select_all_items(c, [data['member']])
	pusher.trigger(u'poll', u'vote', output)
	return request.data

if __name__ == '__main__':
	main()
	app.run(debug=True)