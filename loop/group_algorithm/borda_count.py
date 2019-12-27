from loop.group_algorithm.additive_utilitarian import AdditiveUtilitarian


class BordaCount:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_max_rating(self):
        sorted_ratings = [sorted(rating) for rating in self.ratings]

        unordered_users_ratings = []
        for all_user_ratings in sorted_ratings:
            new_ratings = [rating for rating in enumerate(all_user_ratings)]
            user = []
            for rating in set(all_user_ratings):
                if all_user_ratings.count(rating) > 1:
                    calculation = []
                    for rate in new_ratings:
                        if rate[1] == rating:
                            calculation.append(rate[0])
                    calculate_new_rating = sum(calculation)/all_user_ratings.count(rating)
                    for rate in new_ratings:
                        if rate[1] == rating:
                            user.append((calculate_new_rating, rating))
                else:
                    for new_rating in new_ratings:
                        if new_rating[1] == rating:
                            user.append(new_rating)
            unordered_users_ratings.append(user)

        ordered_users_ratings = []
        for original_rating_order, borda_ratings in zip(self.ratings, unordered_users_ratings):
            user = []
            for original_rating in original_rating_order:
                for borda_rating in borda_ratings:
                    if original_rating == borda_rating[1]:
                        user.append(borda_rating[0])
                        break
            ordered_users_ratings.append(user)
        return ordered_users_ratings

    def get_recommendation(self):
        additive = AdditiveUtilitarian(self.movies, self.get_max_rating())
        return additive.get_recommendation()
