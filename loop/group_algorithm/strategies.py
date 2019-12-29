class Strategies:
    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_recommendation(self, ratings):
        # Get the biggest value
        max_rating = max(ratings)
        # Checking for duplicates
        check_for_max_value_occurrences = ratings.count(max_rating)
        if check_for_max_value_occurrences > 1:
            # If they are movies with the same max value, then they are all returned
            res_list = [self.movies[index] for index, rating in enumerate(ratings) if rating == max_rating]
            return res_list
        else:
            # Else return the individual movie
            movie_index = ratings.index(max(ratings))
            return self.movies[movie_index]

    def minimum_value(self):
        # Get the smallest value in each column
        return [min(ratings) for ratings in zip(*self.ratings)]

    # Return recommendation
    def least_misery(self):
        return self.get_recommendation(self.minimum_value())

    def maximum_value(self):
        # Get the biggest value in each column
        return [max(ratings) for ratings in zip(*self.ratings)]

    # Return recommendation
    def most_pleasure(self):
        return self.get_recommendation(self.maximum_value())

    def average_value(self):
        # Separating the users ratings into ratings based on a specific movie
        movie_ratings = [rating for rating in zip(*self.ratings)]
        # Set a threshold, for valid movies
        threshold = 3
        # Compare each movies ratings with the threshold value
        compared_ratings = [[rating for rating in ratings if rating > threshold] for ratings in movie_ratings]
        # If one or more rating for a movie is less then the threshold, then the that movie is assigned an overall
        # score of zero, else the sum off all the other movies ratings are calculated
        amount_of_users = len(self.ratings)
        return [sum(ratings) if len(ratings) == amount_of_users else 0 for ratings in compared_ratings]

    # Return recommendation
    def average_without_misery(self):
        return self.get_recommendation(self.average_value())
