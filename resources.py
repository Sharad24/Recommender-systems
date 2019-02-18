import json
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['Mongo_DBNAME'] = 'imdb_movies'
app.config['MONGO_URI'] = 'mongodb://localhost:27010/imdb_movies'

mongo = PyMongo(app)

@app.route('/add')
def add_user():
    user = mongo.db.users
    user.insert({'name':"Sharad"})
    return "Added User"

@app.route('/find')
def find():
    user = mongo.db.users
    user.find_one('')
    return "You found "

@app.route('/collection')
def collection():
    collection = mongo.db.post
    data = collection.find_one()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug = True)
