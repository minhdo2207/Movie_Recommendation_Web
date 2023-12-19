import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import math
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request
from scipy import sparse

#Load dataset
movies_df = pd.read_csv("../preprocessor/movies_data_cleaned.csv", sep=',', index_col=False, dtype='unicode', usecols=['movie_id', 'title', 'img_url'])
df = pd.read_csv("../preprocessor/user_rating_cleaned.csv", sep=',', index_col=False, dtype='unicode')

#Functions to return dataset's features
def get_movie_url(movie_id):
    return movies_df[movies_df.movie_id == movie_id].img_url.values[0]

def get_user_id(user_id_number):
    return df[df.user_id_number == user_id_number].user_id.values[0]

def get_movie_id(movie_id_number):
    return df[df.movie_id_number == movie_id_number].movie_id.values[0]

#convert movie id string into numerical id
df['user_id_number'] = df['user_id'].astype('category').cat.codes.values
df['movie_id_number'] = df['movie_id'].astype('category').cat.codes.values
Y_data = df[['user_id_number', 'movie_id_number', 'rating']].values

#Colaborative filtering model creation
class Colaborative_Filtering(object):
    def __init__(self, Y_data):
        self.Y_data = Y_data
        self.Ybar_data = None
        # number of users and items. Remember to add 1 since id starts from 0
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1 
    def create_model(self,k):
        self.model = NearestNeighbors(n_neighbors=k,algorithm='brute',metric='cosine')
        self.model.fit(self.interaction_matrix)
    def create_matrix(self):
        # Create a pandas DataFrame
        new_df = pd.DataFrame(self.Y_data, columns=['user_id', 'movie_id', 'rating'])

        # Convert the 'rating' column to integers
        new_df['rating'] = new_df['rating'].astype(int)

        # Create a sparse matrix
        self.interaction_matrix = sparse.coo_matrix((new_df['rating'], (new_df['movie_id'], new_df['user_id'])))
        self.interaction_matrix= self.interaction_matrix.tocsr()
    def get_rated_movies(self,user_id):
        self.movies_rated = df[['user_id_number','movie_id_number','rating']]
        self.movies_rated = df.loc[df['user_id_number'] == user_id, ['user_id_number', 'movie_id_number', 'rating']]
        self.movies_rated = pd.DataFrame(self.movies_rated, columns=['user_id_number', 'movie_id_number', 'rating'])
        self.movies_rated= self.movies_rated[['movie_id_number','rating']].reset_index(drop=True)
        return self.movies_rated
    def calculate_score(self,user_id):
        similar_candidates_rating= pd.Series(dtype='float64')
        similar_candidates_score= pd.Series(dtype='float64')
        self.movies_list=self.interaction_matrix.getcol(user_id).toarray()
        self.movies_rated= self.movies_list
        self.movies_list = np.where(self.movies_list != 0)[0]
        
        for movie in self.movies_list:
            similar = self.model.kneighbors(
                [self.interaction_matrix.getrow(movie).toarray().squeeze()],
                return_distance=True
            )
            sim_score=similar[0]
            sim_id=similar[1]
            sim_id=np.array(list(map(lambda x: x,sim_id[0])))
            similar=pd.Series(data=sim_score[0],index=sim_id)
            similar=similar[similar!=0]
            # similar=similar[similar.index.isin(stats.index)]
            similar_candidates_score=pd.concat([similar_candidates_score,similar])
            similar=similar.map(lambda x: x*self.movies_rated[movie])
            similar_candidates_rating = pd.concat([similar_candidates_rating,similar])
        filtered_candidates_rating_sum= similar_candidates_rating.groupby(similar_candidates_rating.index).sum()
        filtered_candidates_score_sum= similar_candidates_score.groupby(similar_candidates_score.index).sum()
        similar_movies=filtered_candidates_rating_sum.index
        pred_rating= pd.Series(dtype='float64',index=similar_movies)
        for i in range(0,len(similar_movies)):
            pred_rating[similar_movies[i]]= filtered_candidates_rating_sum[similar_movies[i]]/filtered_candidates_score_sum[similar_movies[i]]
        return pred_rating

#Item-Based Colaborative Filtering
def item_based_recommender(uid='ur3032446'):
    #Create Colaborative filtering model
    recommender = Colaborative_Filtering(Y_data)
    recommender.create_matrix()
    recommender.create_model(k=4)
    user_id=uid

    # Check if there are any rows with the specified user_id
    matching_rows = df[df.user_id == user_id]

    if not matching_rows.empty:
        # If there are matching rows, retrieve the user_id_number
        user_id_number =matching_rows.values[0][3]
        movies_rated=recommender.get_rated_movies(user_id_number)
        pred_rating = recommender.calculate_score(user_id_number)
    else:
        print(f"No rows found for user_id: {user_id}")

    #Convert movie_id_number to movie_title
    movie_id_convert =df[['movie_id','movie_id_number']]
    movie_id_convert= movie_id_convert.drop_duplicates()
    movie_title = movies_df[['movie_id','title']]
    movie_title_convert = pd.merge(movie_id_convert,movie_title)

    #get recommendation
    pred_rating.sort_values(inplace=True,ascending=False)
    pred_rating_df = pd.DataFrame(pred_rating).reset_index()
    pred_rating_df.columns = ['movie_id_number', 'predicted_rating']
    final_pred_df = pd.merge(pred_rating_df,movie_id_convert)
    final_pred_df = pd.merge(final_pred_df,movies_df)
    final_pred_df = final_pred_df[['movie_id','title','predicted_rating']]
    return final_pred_df['title'].head(10).values

