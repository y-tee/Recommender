import sys
import pandas as pd
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import random

from sklearn.preprocessing import MinMaxScaler

import implicit

# Load the data like we did before
raw_data = pd.read_csv('C:/Users/Yingting L/Desktop/recommender/SVD implicit/356365.csv')
#raw_data = raw_data.drop(raw_data.columns[1], axis=1)
#raw_data.columns = ['user', 'st', 'count']

# Drop NaN columns
#data = raw_data.dropna()
data = raw_data

# Create a numeric user_id and artist_id column
#data['user_id'] = data['user_id'].astype("category")
#data['service_type_id'] = data['service_type_id'].astype("category")
#data['user_id'] = data['user'].cat.codes
#data['artist_id'] = data['artist'].cat.codes

# The implicit library expects data as a item-user matrix so we
# create two matricies, one for fitting the model (item-user) 
# and one for recommendations (user-item)
lalala=sparse.csr_matrix(data)
sparse_item_user = sparse.csr_matrix((data['count'].astype(float), (data['service_type_id'], data['user_id'])))
sparse_user_item = sparse.csr_matrix((data['count'].astype(float), (data['user_id'], data['service_type_id'])))

# Initialize the als model and fit it using the sparse item-user matrix
model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.1, iterations=20)

# Calculate the confidence by multiplying it by our alpha value.
alpha_val = 15
data_conf = (sparse_item_user * alpha_val).astype('double')

#Fit the model
model.fit(data_conf)


#---------------------
# FIND SIMILAR ITEMS
#---------------------


st = 522 
n_similar = 10

# Use implicit to get similar items.
similar = model.similar_items(st, n_similar)

# Print the names of our most similar artists
for item in similar:
    idx, score = item
    print (item)

    
#------------------------------
# CREATE USER RECOMMENDATIONS
#------------------------------

# Create recommendations for user with id 2025
user_id = 656

# Use the implicit recommender.
recommended = model.recommend(user_id,sparse_user_item)

artists = []
scores = []

# Get artist names from ids
for item in recommended:
    idx, score = item
    artists.append(idx)
    scores.append(score)

# Create a dataframe of artist names and scores
recommendations = pd.DataFrame({'st': artists, 'score': scores})

print (recommendations)


