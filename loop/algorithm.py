from loop.group_algorithm.utilitarian_strategies import UtilitarianStrategies
from loop.group_algorithm.borda_count import BordaCount
from loop.group_algorithm.copeland_rule import CopelandRule
from loop.group_algorithm.plurality_voting import PluralityVoting
from loop.group_algorithm.approval_voting import ApprovalVoting
from loop.group_algorithm.strategies import Strategies
from itertools import groupby


class Algorithms:

    def __init__(self, data):
        self.data = data

    def process_data(self):
        ratings_data = []
        ratings = self.data.index("User 1:")
        # getting all the movie names
        movies = [movie for movie in self.data[1: ratings]]
        # iterating through the nested list
        for value in self.data[ratings:]:
            try:
                # Checking each value in the list to see if its an int or string
                if 0 < int(value) < 11:
                    # If it is an int, then it is added to a list
                    ratings_data.append(int(value))
            # Else if it is not an int the error is caught as a string cannot be casted as a float
            except ValueError:
                pass
        # Separate individual user ratings
        ratings = [ratings_data[index:index + len(movies)] for index in range(0, len(ratings_data), len(movies))]
        return movies, ratings

    def additive(self):
        data = self.process_data()
        additive = UtilitarianStrategies(data[0], data[1])
        return additive.multiplicative_utilitarian()

    def multiplicative(self):
        data = self.process_data()
        multiplicative = UtilitarianStrategies(data[0], data[1])
        return multiplicative.additive_utilitarian()

    def borda(self):
        data = self.process_data()
        additive = BordaCount(data[0], data[1])
        return additive.get_recommendation()

    def copeland(self):
        data = self.process_data()
        additive = CopelandRule(data[0], data[1])
        return additive.get_recommendation()

    def plurality_voting(self):
        data = self.process_data()
        plurality_voting = PluralityVoting(data[0], data[1])
        return plurality_voting.get_recommendation()

    def approval(self):
        data = self.process_data()
        approval_voting = ApprovalVoting(data[0], data[1])
        return approval_voting.get_recommendation()

    def least_misery(self):
        data = self.process_data()
        strategies = Strategies(data[0], data[1])
        return strategies.least_misery()

    def most_pleasure(self):
        data = self.process_data()
        strategies = Strategies(data[0], data[1])
        return strategies.most_pleasure()

    def average_without_misery(self):
        data = self.process_data()
        strategies = Strategies(data[0], data[1])
        return strategies.average_without_misery()

    def run(self):
        # Adding all movie results to a list dynamically
        movies = []
        algorithms = [self.additive(), self.multiplicative(), self.borda(), self.copeland(), self.plurality_voting(),
                      self.approval(), self.least_misery(), self.most_pleasure(), self.average_without_misery()]

        for algorithm in algorithms:
            if type(algorithm) == list:
                for movie in algorithm:
                    movies.append(movie)
            else:
                movies.append(algorithm)

        # Group the same movies
        group_movies = [list(movie_group) for movie, movie_group in groupby(sorted(movies))]
        # Get the movie and count the occurrence of each movie
        rank_movies = [{"movie": movies[0], "score": len(movies)} for movies in group_movies]
        # Sort the movies based on their score
        sort_ranked_movies = sorted(rank_movies, key=lambda k: k['score'], reverse=True)
        return sort_ranked_movies
