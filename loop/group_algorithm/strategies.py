class Strategies:
    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_recommendation(self, a_list):
        max_rating = max(a_list)
        check_for_max_value_occurrences = a_list.count(max_rating)
        if check_for_max_value_occurrences > 1:
            res_list = [self.movies[index] for index, rating in enumerate(a_list) if rating == max_rating]
            return res_list
        else:
            movie_index = a_list.index(max(a_list))
            return self.movies[movie_index]

    def minimum_value(self):
        return [min(ratings) for ratings in zip(*self.ratings)]

    def least_misery(self):
        return self.get_recommendation(self.minimum_value())

    def maximum_value(self):
        return [max(ratings) for ratings in zip(*self.ratings)]

    def most_pleasure(self):
        return self.get_recommendation(self.maximum_value())

    def average_value(self):
        all_ratings = [rating for rating in zip(*self.ratings)]
        threshold = 3
        compared_ratings = [[rating for rating in ratings if rating > threshold] for ratings in all_ratings]
        amount_of_users = len(self.ratings)
        return [sum(ratings) if len(ratings) == amount_of_users else 0 for ratings in compared_ratings]

    def average_without_misery(self):
        return self.get_recommendation(self.average_value())
