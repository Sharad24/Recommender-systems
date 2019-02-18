from flask import Flask, jsonify, request
import flask
from flask_pymongo import PyMongo
import pprint

import pymongo
from pymongo import MongoClient
client = MongoClient()
db1 = client.imdb_movies

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'imdb_movies'
app.config['MONGO_URI'] = 'mongodb://localhost:27010/'

mongo = PyMongo(app)

@app.route('/', methods = ['GET'])
def hello():
    return jsonify({'result':'Hello!'})

def is_collection():
    collection = db1.post.find()
    for doc in collection:
        pprint.pprint(doc)

@app.route('/framework', methods=['GET'])
def get_all_frameworks(db1 = db1):
    framework = db1.post 

    output = []

    for q in framework.find():
        output.append({'title' : q['title'], 'release' : q['release'], '_id':q['_id']})

    return jsonify({'result' : output})

@app.route('/users', methods = ['GET'])
def get_all_user_data(db1 = db1):
    post = db1.users
    
    output = []
    
    for q in post.find():
        output.append(q)
        
    return jsonify({'result' : output})

@app.route('/one_user/<id>', methods = ['GET'])
def get_one_user(id, db1 = db1):
    users = db1.users
    
    output = []
    
    q = users.find_one({'_id':int(id)})
    
    if q:
        output = {'result':q}
    else:
        output = "No results found"
        
    return jsonify(output)

@app.route('/add_user/<name>', methods = ['GET'])
def add_new_user(name, db1 = db1):
    users = db1.users
    
    output = []
    
    for q in post.find():
        output.append({'title': q['title'], 'release':q['release']})
        
    return jsonify({'result' : output})


@app.route('/framework/<name>', methods=['GET'])
def get_one_framework(name):
    framework = db1.post

    q = framework.find_one({'name' : name})

    if q:
        output = {'title' : q['title'], 'release' : q['release']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/framework', methods=['POST'])
def add_framework():
    framework = mongo.db.framework 

    name = request.json['name']
    language = request.json['language']

    framework_id = framework.insert({'name' : name, 'language' : language})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)