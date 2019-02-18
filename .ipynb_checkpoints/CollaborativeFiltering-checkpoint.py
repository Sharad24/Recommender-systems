
# coding: utf-8

# In[100]:


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


# In[2]:


#scores = pd.read_csv('ml-20m/genome-scores.csv')
#g_tags = pd.read_csv('ml-20m/genome-tags.csv')
#links = pd.read_csv('ml-20m/links.csv')
#movies = pd.read_csv('ml-20m/movies.csv')
ratings = pd.read_csv('ml-20m/ratings.csv')
#tags = pd.read_csv('ml-20m/tags.csv')


# In[102]:


user_ratings = ratings.groupby('userId')


# In[120]:


user_ratings = {}
for k, v in ratings.groupby('userId'):
    user_ratings[k] = dict(zip(v['movieId'].values, v['rating'].values))
user_ratings_test = dict(list(user_ratings.items())[:1000])


# In[133]:


class userUserBasedCF(object):
    def __init__(self, dataset):
        self.dataset = dataset
        self.means = {}
        for user, user_ratings in self.dataset.items():
            mean = np.mean(np.array(list(user_ratings.values())))
            self.means[user] = mean

    def pearson_correlation(self, user1, user2):
        """
        user1, user2: dictionaries
        """
        common_movies = sorted(set(user1).intersection(set(user2)))
        if len(common_movies) != 0 and len(common_movies) != 1:
            user1_ratings = np.squeeze(normalize(np.array([user1[movie] for movie in common_movies])[np.newaxis, :]))
            user2_ratings = np.squeeze(normalize(np.array([user2[movie] for movie in common_movies])[np.newaxis, :]))
            corr = pearsonr(user1_ratings, user2_ratings)[0]
        else:
            corr = 0
            #print("No common movies")
        return corr
    
    def knn(self, user, k):
        """
        user: user_id
        k: number of KNN
        """
        neighbours={}
        i = 0
        for user_id, user_data in self.dataset.items():
            if user_id == user:
                continue
            corr = self.pearson_correlation(self.dataset[user], user_data)
            neighbours[user_id] = corr
            i+=1
        sort = sorted(neighbours.items(), key=lambda x: x[1], reverse = True)
        knn = sort[:k]
        knn_user_ids = [user_id for user_id, user_corr in knn]
        print("KNN")
        return knn_user_ids
    
    def predict(self, user, movie_id, knn):
        """
        user: user_id
        movie_id: movie_id
        knn: knn_user_ids
        
        prediction = mean_rating_of_active_user + sum_over_knn(user_rating_for_i * pearson(user, active_user))/sum_over_knn(pearson(user, active_user))
        """
        mean_user_rating = self.means[user]
        print("Mean user rating for the user is ", mean_user_rating)
        iter_rating = 0.0
        pear_corr = 0.0
        for i, element in enumerate(knn):
            temp_corr = self.pearson_correlation(self.dataset[user], self.dataset[element])
            if math.isnan(temp_corr):
                continue
            if movie_id in self.dataset[element].keys():
                iter_rating += (self.dataset[element][movie_id]-self.means[element]) * temp_corr
            else:
                iter_rating += 0
            pear_corr += temp_corr
            
        pred = mean_user_rating + iter_rating/pear_corr
        return pred    


# In[134]:


cf = userUserBasedCF(user_ratings_test)


# In[138]:


import warnings
warnings.filterwarnings('ignore')
knn = cf.knn(3, 100)
cf.predict(3, 45, knn)


# In[ ]:


item_ratings = {}
for k, v in ratings.groupby('movieId'):
    item_ratings[k] = dict(zip(v['userId'].values, v['rating'].values))


# In[139]:


class itemItemBasedCF(object):
    def __init__(self, dataset):
        self.dataset = dataset
        self.means = {}
        for user, user_ratings in self.dataset.items():
            mean = np.mean(np.array(list(user_ratings.values())))
            self.means[user] = mean

    def pearson_correlation(self, item1, item2):
        """
        item1, item2: dictionaries
        """
        common_users = sorted(set(item1).intersection(set(item2)))
        if len(common_users) != 0 and len(common_users) != 1:
            item1_ratings = np.squeeze(normalize(np.array([item1[user] for user in common_users])[np.newaxis, :]))
            item2_ratings = np.squeeze(normalize(np.array([item2[user] for user in common_users])[np.newaxis, :]))
            corr = pearsonr(item1_ratings, item2_ratings)[0]
        else:
            corr = 0
        return corr
    
    def knn(self, item, k):
        """
        item: item_id
        k: number
        """
        neighbours={}
        i = 1
        for item_id, item_data in self.dataset.items():
            if item_id == item:
                continue
            corr = self.pearson_correlation(self.dataset[item], item_data)
            neighbours[item_id] = corr
            i+=1
            
        sort = sorted(neighbours.items(), key=lambda x: x[1], reverse = True)
        knn = sort[:k]
        knn_item_ids = [item_id for item_id, item_corr in knn]
        return knn_item_ids
    
    def predict(self, item, user, knn):
        """
        user: user_id
        item: item_id
        knn: knn_item_ids
        
        prediction = mean_rating_of_active_item + sum_over_knn(item_k_rating_by_user * pearson(item_k, active_item))/sum_over_knn(pearson(item_k, active_item))
        """
        mean_item_rating = self.means[item]
        iter_rating = 0.0
        pear_corr = 0.0
        for i, element in enumerate(knn):
            temp_corr = self.pearson_correlation(self.dataset[item], self.dataset[element])
            if math.isnan(temp_corr):
                continue
            if user in self.dataset[element].keys():
                iter_rating += (self.dataset[element][user]-self.means[element]) * temp_corr
            else:
                iter_rating += 0
            pear_corr += temp_corr
                    
        pred = mean_item_rating + iter_rating/pear_corr
        print("Predicted rating for item ", str(item), " by user ", str(user), " is ", str(pred))
        return pred    


# In[140]:


iicf = itemItemBasedCF(item_ratings)
knn = iicf.knn(100, 100)
iicf.predict(100, 100, knn)


# In[141]:


class matrixfactorbasedCF(object):
    def __init__(self):
        pass

