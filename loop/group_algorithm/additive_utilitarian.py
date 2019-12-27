class AdditiveUtilitarian:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_max_rating(self):
        movie_ratings = [sum(rating) for rating in zip(*self.ratings)]
        max_rating = max(movie_ratings)
        return movie_ratings, max_rating

    def get_recommendation(self):
        movie_ratings, max_rating = self.get_max_rating()
        check_for_max_value_occurrences = movie_ratings.count(max_rating)
        if check_for_max_value_occurrences > 1:
            res_list = [self.movies[index] for index, rating in enumerate(movie_ratings) if rating == max_rating]
            return res_list
        else:
            movie_index = movie_ratings.index(max(movie_ratings))
            return self.movies[movie_index]
