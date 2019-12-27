from loop.group_algorithm.additive_utilitarian import AdditiveUtilitarian


class ApprovalVoting:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_max_rating(self):
        threshold = 5
        approvals_ratings = [[1 if user_rating > threshold else 0 for user_rating in user] for user in self.ratings]
        return approvals_ratings

    def get_recommendation(self):
        additive = AdditiveUtilitarian(self.movies, self.get_max_rating())
        return additive.get_recommendation()

