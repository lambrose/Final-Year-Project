import numpy


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

    def get_recommendation(self, movie_max_rating):
        movie_ratings, max_rating = movie_max_rating
        # Check if there are more than one movie with the same highest rating
        check_for_max_value_occurrences = movie_ratings.count(max_rating)
        if check_for_max_value_occurrences > 1:
            # Getting all movies that have the same rating by using the enumerator to find the index of the movie
            movies = [self.movies[index] for index, rating in enumerate(movie_ratings) if rating == max_rating]
            return movies
        else:
            # Get the individual movie by the index of the max rating
            movie_index = movie_ratings.index(max(movie_ratings))
            return self.movies[movie_index]
