import requests
import json


def get_movies_from_tastedive(name):
    base_url = "https://tastedive.com/api/similar"
    params_dict = {}
    params_dict["q"] = name
    params_dict["type"] = "movies"
    params_dict["limit"] = 5
    api_resp = requests.get(base_url, params = params_dict)
    return(json.loads(api_resp.text))


def extract_movie_titles(dictio):
    movies_list = dictio["Similar"]["Results"]
    movies = [movie["Name"] for movie in movies_list]
    return movies


def get_related_titles(movies_list):
    base_url = "https://tastedive.com/api/similar"
    params_list = []
    related_movies = []
    movie_list = []
    for movie in movies_list:
        params_dict = {}
        params_dict["q"] = movie
        params_dict["limit"] = 5
        params_dict["type"] = "movies"
        params_list.append(params_dict)
    for param in params_list:
        api_resp = requests.get(base_url, params = param)
        related_movies.append(json.loads(api_resp.text))
    for movies in related_movies:
        movie_list.append(extract_movie_titles(movies))
    related_movies = []
    for movies in movie_list:
        for movie in movies:
            if movie not in related_movies: related_movies.append(movie)
    return related_movies

#Enter your OMDB API Key here:
your_api_key = ""

def get_movie_data(title):
    base_url = "http://www.omdbapi.com/?apikey={}".format(your_api_key)
    params_dict = {}
    params_dict["t"] = title
    params_dict["r"] = "json"
    api_resp = requests.get(base_url, params = params_dict)
    return(json.loads(api_resp.text))


def get_movie_rating(movie_data):
    for ratings in movie_data["Ratings"]:
        if ratings["Source"] == "Rotten Tomatoes": return int((ratings["Value"])[:2])
    return 0


def get_sorted_recommendations(movie_list):
    related_movies = get_related_titles(movie_list)
    ratings = {}
    for movie in related_movies:
        rating = get_movie_rating(get_movie_data(movie))
        ratings[movie] = rating
    sorted_movies = []
    for movie, rating in sorted(ratings.items(), key=lambda item: (item[1], item[0]), reverse=True):
        sorted_movies.append(movie)
    return sorted_movies

#Some tests done
print(extract_movie_titles(get_movies_from_tastedive("Sherlock Holmes")))
print(get_related_titles(["Black Panther", "Captain Marvel"]))
print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))