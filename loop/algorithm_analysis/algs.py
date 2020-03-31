from loop.algorithm_analysis.group_alg.approval_voting import ApprovalVoting
from loop.algorithm_analysis.group_alg.borda_count import BordaCount
from loop.algorithm_analysis.group_alg.copeland_rule import CopelandRule
from loop.algorithm_analysis.group_alg.plurality_voting import PluralityVoting
from loop.algorithm_analysis.group_alg.strategies import Strategies
from loop.algorithm_analysis.group_alg.utilitarian_strategies import UtilitarianStrategies


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