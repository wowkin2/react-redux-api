import os

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient


DIST_FOLDER = os.environ.get('REACTJS_DIST')
MONGODB_URI = os.environ.get('MONGODB_URI')

app = Flask(__name__, static_url_path='/static', static_folder=DIST_FOLDER+'dist')
api = Api(app)
db = MongoClient(MONGODB_URI).get_default_database()


@app.route('/images/favicon.ico')
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')

