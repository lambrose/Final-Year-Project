from loop.group_algorithm.utilitarian_strategies import UtilitarianStrategies


class BordaCount:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def unordered_new_ratings(self):
        # Sort ratings in ascending order
        sorted_ratings = [sorted(rating) for rating in self.ratings]

        incorrect_ordered_new_ratings = []
        # Calculate the borda ratings values per user for all movie ratings
        for sorted_user_ratings in sorted_ratings:
            # The enumerate index will act as the borda rating value
            new_ratings = [rating for rating in enumerate(sorted_user_ratings)]
            user = []
            for user_rating in set(sorted_user_ratings):
                # Check for duplicate rating values
                if sorted_user_ratings.count(user_rating) > 1:
                    calculation = [new_rating[0] for new_rating in new_ratings if new_rating[1] == user_rating]
                    # Calculating the average borda value for duplicate values
                    average_score = sum(calculation)/len(calculation)
                    # Adding a tuple of the new rating with the original value
                    for new_rating in new_ratings:
                        if new_rating[1] == user_rating:
                            user.append((average_score, user_rating))
                else:
                    # There are no duplicates, so just add the enumerated value
                    for new_rating in new_ratings:
                        if new_rating[1] == user_rating:
                            user.append(new_rating)
            # Add a set of user ratings, duplicate values are not needed
            incorrect_ordered_new_ratings.append(set(user))
        return incorrect_ordered_new_ratings

    def position_new_ratings(self):
        ordered_users_ratings = []
        # Comparing the original values with the new values
        for ordered_ratings, unordered_ratings in zip(self.ratings, self.unordered_new_ratings()):
            # if there is a match, then the new value is assigned in the position of the old value
            user = [unordered[0] for ordered in ordered_ratings for unordered in unordered_ratings if ordered == unordered[1]]
            ordered_users_ratings.append(user)
        return ordered_users_ratings

    # Using the additive algorithm to determine the recommendation
    def get_recommendation(self):
        additive = UtilitarianStrategies(self.movies, self.position_new_ratings())
        return additive.additive_utilitarian()
