import numpy as np
import pandas as pd
import pymongo
#from pymongo import MongoClient
#client = MongoClient()
#db = client.imdb
import scipy
from scipy.stats import pearsonr
from sklearn.preprocessing import normalize
import math

ratings = pd.read_csv('ml-20m/ratings.csv')

user_ratings = {}
for k, v in ratings.groupby('userId'):
    user_ratings[k] = dict(zip(v['movieId'].values, v['rating'].values))
    
import pymongo
from pymongo import MongoClient
client = MongoClient()
db1 = client.imdb_movies

users = db1['users']

for k, v in user_ratings.items():
    to_post = {}
    to_post['_id'] = k
    for k2, v2 in v.items():
        to_post[str(k2)] = v2
    users.insert_one(v)