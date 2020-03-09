from flask_login import current_user

from loop import db
from loop.group_algorithm.utilitarian_strategies import UtilitarianStrategies
from loop.group_algorithm.borda_count import BordaCount
from loop.group_algorithm.copeland_rule import CopelandRule
from loop.group_algorithm.plurality_voting import PluralityVoting
from loop.group_algorithm.approval_voting import ApprovalVoting
from loop.group_algorithm.strategies import Strategies
from itertools import groupby
from loop.models import GroupResults


class Algorithms:

    def __init__(self, data):
        self.data = data

    def process_data(self):
        if "User 1:" in self.data:
            ratings_data = []
            ratings = self.data.index("User 1:")
            # getting all the movie names
            movies = [movie for movie in self.data[1: ratings]]
            # iterating the list from the point of user 1 first rating
            for value in self.data[ratings:]:
                try:
                    # Checking each value in the list to see if its an int or string
                    if 0 < int(value) < 11:
                        # If it is an int, then it is added to a list
                        ratings_data.append(int(value))
                # Else if it is not an int the error is caught as a string cannot be casted as a int
                except ValueError:
                    pass
            # Separate individual user ratings
            ratings = [ratings_data[index:index + len(movies)] for index in range(0, len(ratings_data), len(movies))]
            return movies, ratings
        else:
            movies = []
            ratings = []
            for y in self.data:
                try:
                    # Checking each value in the list to see if its an int or string
                    if 0 < int(y) < 11:
                        # If it is an int, then it is added to a list
                        ratings.append(int(y))
                # Else if it is not an int the error is caught as a string cannot be casted as a int
                except ValueError:
                    if y not in movies:
                        movies.append(y)
            # Separate individual user ratings
            ratings = [ratings[index:index + len(movies)] for index in range(0, len(ratings), len(movies))]
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

        # adding all the recommended movies from the algorithms to a list for counting occurrences
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

        # specify the most recommended movie as the winner
        results = []
        winner = sort_ranked_movies[0]['movie']
        for algorithm in algorithms:
            # if the algorithm returned multiple movies containing the winner
            if type(algorithm) == list:
                if winner in algorithm:
                    results.append(1)
            else:
                # if the algorithm returned the winner
                if winner == algorithm:
                    results.append(2)
                # if the algorithm did not returned the winner
                else:
                    results.append(0)

        # add this entry to the database
        group = GroupResults(winner=sort_ranked_movies[0]['movie'], additive=results[0], multiplicative=results[1],
                             borda=results[2], copeland=results[3], plurality_voting=results[4], approval=results[5],
                             least_misery=results[6], most_pleasure=results[7], average_without_misery=results[8],
                             author=current_user)
        db.session.add(group)
        db.session.commit()
        return sort_ranked_movies
