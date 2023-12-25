import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from fuzzywuzzy import fuzz
import urllib.request
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Set Matplotlib to use the Agg backend
import matplotlib.pyplot as plt

# Load data
movies = pd.read_csv('../preprocessor/movies_small.csv', sep=',', index_col=False, dtype='unicode')
selected_movies = movies

# Explore the Feature (genres)
selected_movies[['title', 'genres', 'overview']].head(5)

# Count the number of occurrences for each genre in the data set
counts = dict()

for i in selected_movies.index:
    for g in selected_movies.loc[i, 'genres'].split(' '):
        if g not in counts:
            counts[g] = 1
        else:
            counts[g] = counts[g] + 1

# Tidy up genre counts and plot
selected_movies.loc[:, 'genres'] = selected_movies['genres'].str.replace(',', ' ')
plt.figure(figsize=(12, 6))
plt.bar(list(counts.keys()), counts.values(), color='#A9A9A9')
plt.xticks(rotation=45)
plt.xlabel('Genres')
plt.ylabel('Counts')

# Term Frequency and Inverse Document Frequency (tf-idf)
selected_movies.loc[:, 'genres'] = selected_movies['genres'].str.replace('Sci-Fi', 'SciFi')
selected_movies.loc[:, 'genres'] = selected_movies['genres'].str.replace('Film-Noir', 'FilmNoir')
selected_movies.loc[:, 'genres'] = selected_movies['genres'].str.replace('Reality-TV', 'RealityTV')
selected_movies.loc[:, 'genres'] = selected_movies['genres'].str.replace('Talk-Show', 'TalkShow')

# Combine 'overview' and 'genres' into a single column
selected_movies.loc[:, 'overview_and_genres'] = selected_movies.loc[:, 'overview'] + ' ' + selected_movies.loc[:, 'genres']

# Create a TF-IDF vectorizer
tfidf_vector = TfidfVectorizer(stop_words='english')

# Compute the TF-IDF matrix
tfidf_matrix = tfidf_vector.fit_transform(selected_movies['overview_and_genres'])

# Create the cosine similarity matrix
sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
print(sim_matrix)


# Function to find the closest title
def matching_score(a, b):
    return fuzz.ratio(a, b)

# Function to return the most similar title to the words a user types
def find_closest_title(title):
    leven_scores = list(enumerate(selected_movies['title'].apply(matching_score, b=title)))
    sorted_leven_scores = sorted(leven_scores, key=lambda x: x[1], reverse=True)
    closest_title = get_title_from_index(sorted_leven_scores[0][0])
    distance_score = sorted_leven_scores[0][1]
    return closest_title, distance_score

# Function to get movie image URL from index
def get_movieimg_from_index(index):
    return movies[movies.index == index]['img_url'].values[0]

# Function to get index from title
def get_index_from_title(title):
    return movies[movies.title == title].index.values[0]

# Function to get title from index
def get_title_from_index(index):
    return movies[movies.index == index]['title'].values[0]

def contents_based_recommender(movie, num_of_recomm=10):
    closest_title, distance_score = find_closest_title(movie)
    recommended_movies = []

    if distance_score == 100:
        movie_index = get_index_from_title(closest_title)
        movie_list = list(enumerate(sim_matrix[int(movie_index)]))
        similar_movies = list(filter(lambda x: x[0] != int(movie_index), sorted(movie_list, key=lambda x: x[1], reverse=True)))

        for i, s in enumerate(similar_movies[:num_of_recomm]):
            recommended_movies.append(get_title_from_index(s[0]))

    else:
        print('Did you mean ' + '\033[1m' + str(closest_title) + '\033[0m' + '?', '\n')

        movie_index = get_index_from_title(closest_title)
        movie_list = list(enumerate(sim_matrix[int(movie_index)]))
        similar_movies = list(filter(lambda x: x[0] != int(movie_index), sorted(movie_list, key=lambda x: x[1], reverse=True)))

        for i, s in enumerate(similar_movies[:num_of_recomm]):
            recommended_movies.append(get_title_from_index(s[0]))

    return recommended_movies


