
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[53]:


scores = pd.read_csv('ml-20m/genome-scores.csv')
g_tags = pd.read_csv('ml-20m/genome-tags.csv')
links = pd.read_csv('ml-20m/links.csv')
movies = pd.read_csv('ml-20m/movies.csv')
ratings = pd.read_csv('ml-20m/ratings.csv')
tags = pd.read_csv('ml-20m/tags.csv')


# In[3]:


import pymongo


# In[4]:


from pymongo import MongoClient
client = MongoClient()


# In[5]:


client.imdb_movies


# In[54]:


links.drop('tmdbId', inplace=True, axis=1)


# In[45]:


import urllib
import bs4
import requests
from bs4 import BeautifulSoup


# In[146]:


base_movie_url = "https://www.imdb.com/title/tt0"
#page = requests.get(base_movie_url + str(links['imdbId'].iloc[1]) + '/')
#page.status_code
base_movie_url2 = "https://www.imdb.com/title/tt00"


# In[14]:


#soup1 = BeautifulSoup(page.content, 'html.parser')


# In[173]:


def create_movie_data(movie_id):
    if int(movie_id) // 100000 == 0 and int(movie_id) // 10000 > 0:
        page = requests.get(base_movie_url2 + movie_id + '/')
    elif int(movie_id) // 1000000 == 0 and int(movie_id) // 100000 > 0:
        page = requests.get(base_movie_url + movie_id + '/')
    if page.status_code == 200:
        print("Received successful page response")
        soup = BeautifulSoup(page.content, 'html.parser')
        movie = {}
        movie[str(movie_id)] = {}
        movie[str(movie_id)]['title'], movie[str(movie_id)]['release'] = get_title_and_release(soup)
        movie[str(movie_id)]['thumbnail_addr'] = get_thumbnail_addr(soup)
    elif page.status_code == 404:
        movie = {}
        print("Received No Data")
    return movie
        


# In[48]:


def get_title_and_release(soup):
    title_year = soup.title.text
    title_year = title_year[:-8]
    year = title_year[-4:]
    title = title_year[:-6]
    return title, year


# In[49]:


def get_thumbnail_addr(soup):
    scripts = soup.findAll('script')
    for i, element in enumerate(scripts):
        if "application/ld+json" in str(element):
            json = element
    json = str(json).split('\n')
    for i, element in enumerate(json):
        if "\"image\"" in element:
            image = element
    image = image.split()[-1][1:-2]
    return image


# In[11]:


genres = ['Adventure']
for i in range(len(movies['genres'].iloc[:])):
    temp_movie_genre = movies['genres'].iloc[i]
    temp_movie_genre = temp_movie_genre.split('|')
    for i, element in enumerate(temp_movie_genre):
        if element not in genres:
            genres.append(element)


# In[72]:


#Getting 30 movies for each genre
movies.head()
def get_genres(string):
    return string.split('|')

#get_genres(movies.iloc[0,2])

movie_ids = []

genre_count = dict(zip(genres, np.zeros(len(genres))))

flag = 0
for i in range(len(movies.iloc[:, 0])):
    flag = 0
    temp_movie = movies['title'].iloc[i]
    temp_genres = get_genres(movies['genres'].iloc[i])
    for j, element in enumerate(temp_genres):
        print(element)
        if genre_count[element] >= 15:
            print('Flag is ', 1)
            flag = 1
        print('Flag is ', 0)
    if flag == 1:
        continue
    else:
        for j, element in enumerate(temp_genres):
            genre_count[element] += 1
        movie_ids.append(movies['movieId'].iloc[i])
        print("New Movie added")
    


# In[209]:


def get_movies(movie_ids):
    """
    Generates final movies given genres, movies dataframe and number_of_movies_for_each_genre
    """
    movies = {}
    for i, element in enumerate(movie_ids):
        if i<86 or i in [123,172,175,178,180,181]:
            continue
        imdbId = str(links[links['movieId'] == int(element)]['imdbId'].iloc[0])
        movie_data = create_movie_data(imdbId)
        if len(movie_data[imdbId].items()) != 3:
            print("Error at ", i)
            continue
        movies[str(element)] = movie_data[imdbId]
        print(i + 1, " done")
    return movies


# In[210]:


to_post1 = get_movies(movie_ids)


# In[211]:


db = client.imdb_movies


# In[223]:


post = db.post
post.insert_many(list(to_post.values()))


# In[227]:


db.collection_names(include_system_collections=False)
import pprint
pprint.pprint(post.find_one())

