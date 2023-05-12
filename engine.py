import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Load movie data
movies_df = pd.read_csv('sen.csv')

# Combine genres and average_sentiment as a single string
movies_df['combined_features'] = movies_df['genres'] + ' ' + movies_df['average_sentiment']

# Create a CountVectorizer and fit_transform the combined_features
count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(movies_df['combined_features'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix)

def get_title_from_index(index):
    return movies_df[movies_df.index == index]['movies'].values[0]

def get_index_from_title(title):
    return movies_df[movies_df.movies == title].index.values[0]

def get_movie_poster_path(movie_title, api_key):
    base_url = "https://api.themoviedb.org/3/search/movie?api_key={}&query={}"
    url = base_url.format(api_key, movie_title)
    response = requests.get(url)
    data = response.json()

    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return poster_path
    else:
        return None

def recommend_movies(movie_title, api_key):
    movie_index = get_index_from_title(movie_title)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    for movie in sorted_similar_movies[1:6]:
        movie_title = get_title_from_index(movie[0])
        poster_path = get_movie_poster_path(movie_title, api_key)
        recommended_movies.append({"title": movie_title, "poster_path": poster_path})
    return recommended_movies
