from loop.group_algorithm.additive_utilitarian import AdditiveUtilitarian
from loop.group_algorithm.multiplicative_utilitarian import MultiplicativeUtilitarian


class Algorithms:

    def __init__(self, data):
        self.data = data

    def process_data(self):
        ratings_data = []
        movie_title = None
        ratings = []
        # iterating through the nested list
        for value in self.data:
            try:
                # Checking each value in the list to see if its an int or string
                if 0 < int(value) < 11:
                    # If it is an int, then it is added to a list
                    ratings_data.append(int(value))
            # Else if it is not an int the error is caught as a string cannot be casted as a float
            except ValueError:
                # Adding a list of strings once then breaking out of the for loop
                movie_title = value.split("\r\n")
        # Separate individual user ratings
        for index in range(0, len(ratings_data), len(movie_title)):
            ratings.append(ratings_data[index:index + len(movie_title)])
        return movie_title, ratings

    def additive(self):
        data = self.process_data()
        additive = AdditiveUtilitarian(data[0], data[1])
        return additive.get_user_ratings()

    def multiplicative(self):
        data = self.process_data()
        multiplicative = MultiplicativeUtilitarian(data[0], data[1])
        return multiplicative.get_user_ratings()

    def run(self):
        return ["Additive: ", self.additive(), "Multiplicative: ", self.multiplicative()]
