class PluralityVoting:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def index_movies(self):
        return [[rating for rating in enumerate(ratings)] for ratings in self.ratings]

    counter = 1
    ordered_movie_indexes = []

    def calculate_plurality_voting(self, is_match, movie_ratings):
        highest_rating_index_list = []
        if is_match:
            for ratings in movie_ratings:
                rating_index = [rating[0] for rating in ratings if
                                max(ratings, key=lambda item: item[1])[1] == rating[1]]
                highest_rating_index_list.append(rating_index)
        else:
            a_list = [sorted(ratings, key=lambda item: item[1], reverse=True) for ratings in movie_ratings]
            for ratings in a_list:
                rating_values = []
                rating_index = []
                for rating in ratings:
                    if len(set(rating_values)) < self.counter:
                        rating_values.append(rating[1])
                for rating_value in rating_values:
                    for rating in ratings:
                        if rating[1] == rating_value:
                            rating_index.append(rating[0])
                highest_rating_index_list.append(rating_index)

        intersection_values = []
        if list(set.intersection(*map(set, highest_rating_index_list))):
            for value in list(set.intersection(*map(set, highest_rating_index_list))):
                intersection_values.append(value)
        else:
            index = 1
            for highest_rating_index in highest_rating_index_list[:-1]:
                for highest_rating_index_2 in highest_rating_index_list[index:]:
                    if list(set(highest_rating_index) & set(highest_rating_index_2)):
                        for value in list(set(highest_rating_index) & set(highest_rating_index_2)):
                            if value not in intersection_values:
                                intersection_values.append(value)
                index += 1
        if intersection_values:
            for rates in intersection_values:
                for ratings in movie_ratings:
                    for rating in ratings:
                        if rating[0] == rates:
                            ratings.pop(ratings.index(rating))

            if intersection_values:
                self.ordered_movie_indexes.append(intersection_values)
            if movie_ratings[0]:
                self.calculate_plurality_voting(True, movie_ratings)
        else:
            self.counter += 1
            self.calculate_plurality_voting(False, movie_ratings)

    def get_recommendation(self):
        self.calculate_plurality_voting(True, self.index_movies())
        movies_result = [self.movies[index] for index in self.ordered_movie_indexes[0]]
        if len(movies_result) > 1:
            return movies_result
        else:
            return movies_result[0]
