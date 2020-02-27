from loop.group_algorithm.utilitarian_strategies import UtilitarianStrategies


class Strategies:
    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def minimum_values(self):
        # Get the smallest value in each column
        return [min(ratings) for ratings in zip(*self.ratings)]

    # Return recommendation
    def least_misery(self):
        ratings = self.minimum_values()
        # Using the additive algorithm to determine the recommendation
        additive = UtilitarianStrategies(self.movies, ratings)
        return additive.get_recommendation((ratings, max(ratings)))

    def maximum_values(self):
        # Get the biggest value in each column
        return [max(ratings) for ratings in zip(*self.ratings)]

    # Return recommendation
    def most_pleasure(self):
        ratings = self.maximum_values()
        # Using the additive algorithm to determine the recommendation
        additive = UtilitarianStrategies(self.movies, ratings)
        return additive.get_recommendation((ratings, max(ratings)))

    def average_values(self):
        # Set a threshold, for valid movies
        threshold = 3
        # Separating the users ratings into ratings based on a specific movie
        # Compare each movies ratings with the threshold value
        compared_ratings = [[rating for rating in ratings if rating > threshold] for ratings in zip(*self.ratings)]
        # If one or more rating for a movie is less then the threshold, then the that movie is assigned an overall
        # score of zero, else the sum off all the other movies ratings are calculated
        return [sum(ratings) if len(ratings) == len(self.ratings) else 0 for ratings in compared_ratings]

    # Return recommendation
    def average_without_misery(self):
        ratings = self.average_values()
        # Using the additive algorithm to determine the recommendation
        additive = UtilitarianStrategies(self.movies, ratings)
        return additive.get_recommendation((ratings, max(ratings)))
