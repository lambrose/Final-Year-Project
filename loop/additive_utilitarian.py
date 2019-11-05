class AdditiveUtilitarian:

    ratings = []

    def get_values(self, l, n):
        self.ratings = []
        for i in range(0, len(l), n):
            self.ratings.append(l[i:i + n])

    def get_user_ratings(self):
        movie_ratings = [sum(rating) for rating in zip(*self.ratings)]
        print(movie_ratings)
        movie_with_max_rating = max(movie_ratings)
        check_for_max_value_occurrences = movie_ratings.count(movie_with_max_rating)
        if check_for_max_value_occurrences > 1:
            res_list = [index for index, rating in enumerate(movie_ratings) if rating == movie_with_max_rating]
            print(res_list)
        else:
            print(max(movie_ratings))
            print(movie_ratings.index(max(movie_ratings)))
