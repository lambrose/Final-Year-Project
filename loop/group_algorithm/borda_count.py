from loop.group_algorithm.utilitarian_strategies import UtilitarianStrategies


class BordaCount:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_max_rating(self):
        # Sort ratings in ascending order
        sorted_ratings = [sorted(rating) for rating in self.ratings]

        incorrect_ordered_new_ratings = []
        # Calculate the borda ratings values per user for all movie ratings
        for user_ratings in sorted_ratings:
            # The enumerate index will act as the borda rating value
            new_ratings = [rating for rating in enumerate(user_ratings)]
            user = []
            for user_rating in set(user_ratings):
                # Check for duplicate rating values
                if user_ratings.count(user_rating) > 1:
                    calculation = []
                    for new_rating in new_ratings:
                        if new_rating[1] == user_rating:
                            calculation.append(new_rating[0])
                    # Calculating the average borda value for duplicate values
                    calculate_new_rating = sum(calculation)/user_ratings.count(user_rating)
                    # Adding a tuple of the new rating with the original value
                    for new_rating in new_ratings:
                        if new_rating[1] == user_rating:
                            user.append((calculate_new_rating, user_rating))
                else:
                    # There are no duplicates, so just add the enumerated value
                    for new_rating in new_ratings:
                        if new_rating[1] == user_rating:
                            user.append(new_rating)
            # Add a set of user ratings, duplicate values are not needed
            incorrect_ordered_new_ratings.append(set(user))

        ordered_users_ratings = []
        # Comparing the original values with the new values
        for original_rating_order, borda_ratings in zip(self.ratings, incorrect_ordered_new_ratings):
            user = []
            for original_rating in original_rating_order:
                for borda_rating in borda_ratings:
                    # if there is a match, then the new value is assigned in the position of the old value
                    if original_rating == borda_rating[1]:
                        user.append(borda_rating[0])
            ordered_users_ratings.append(user)
        return ordered_users_ratings

    # Using the additive algorithm to determine the recommendation
    def get_recommendation(self):
        additive = UtilitarianStrategies(self.movies, self.get_max_rating())
        return additive.additive_utilitarian()
