import numpy
from collections import defaultdict


class UtilitarianStrategies:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_max_rating_multiplicative(self):
        # Calculate the sum of the multiplied values of each column
        movie_ratings = [numpy.prod(rating) for rating in zip(*self.ratings)]
        # Get the highest rated movie
        max_rating = max(movie_ratings)
        return movie_ratings, max_rating

    # Return recommendation
    def multiplicative_utilitarian(self):
        return self.get_recommendation(self.get_max_rating_multiplicative())

    def get_max_rating_additive(self):
        # Calculating the sum of each column
        movie_ratings = [sum(rating) for rating in zip(*self.ratings)]
        # Get the highest rated movie
        max_rating = max(movie_ratings)
        return movie_ratings, max_rating

    # Return recommendation
    def additive_utilitarian(self):
        return self.get_recommendation(self.get_max_rating_additive())

    def get_recommendation(self, movie_data):
        movie_ratings, max_rating = movie_data
        sorted_ratings = sorted(enumerate(movie_ratings), key=lambda x: x[1], reverse=True)
        # Check if there are more than one movie with the same highest rating

        dd = defaultdict(list)
        # if len(movie_ratings) != len(set(movie_ratings)):
        for index, value in sorted_ratings:
            dd[value].append(index)
        return [[self.movies[index] for index in d] for k, d, in dd.items()]

        # movie_ratings, max_rating = movie_data
        # sorted_ratings = sorted(enumerate(movie_ratings), key=lambda x: x[1], reverse=True)
        # # Check if there are more than one movie with the same highest rating
        #
        # dd = defaultdict(list)
        # if len(movie_ratings) != len(set(movie_ratings)):
        #     for index, value in sorted_ratings:
        #         dd[value].append(index)
        #     return [[self.movies[index]for index in d] for k, d, in dd.items()]
        # else:
        #     # Get the individual movie by the index of the max rating
        #     return [self.movies[index] for index, rating in sorted_ratings]
