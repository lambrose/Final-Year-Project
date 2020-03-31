from loop.algorithm_analysis.group_alg.utilitarian_strategies import UtilitarianStrategies


class ApprovalVoting:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def approval_voted_table(self):
        # Set the threshold for ratings
        threshold = 5
        # if ratings are above the threshold, then they are assigned a 1
        # Else if they are equal or below they are assigned a 0
        approvals_ratings = [[1 if user_rating > threshold else 0 for user_rating in user] for user in self.ratings]
        return approvals_ratings

    # Using the additive algorithm to determine the recommendation
    def get_recommendation(self):
        additive = UtilitarianStrategies(self.movies, self.approval_voted_table())
        return additive.additive_utilitarian()
