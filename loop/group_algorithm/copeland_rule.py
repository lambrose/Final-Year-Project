from loop.group_algorithm.additive_utilitarian import AdditiveUtilitarian


class CopelandRule:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def get_max_rating(self):
        all_ratings = [rating for rating in zip(*self.ratings)]

        all_comparisons = []
        for ratings in all_ratings:
            row_comparison = []
            for compare_ratings in all_ratings:
                one_comparison = []
                for rating, compare_rating in zip(ratings, compare_ratings):
                    if rating > compare_rating:
                        one_comparison.append(-1)
                    elif rating == compare_rating:
                        one_comparison.append(0)
                    else:
                        one_comparison.append(1)
                sum_of_one_comparison = sum(one_comparison)
                if sum_of_one_comparison > 0:
                    row_comparison.append(1)
                elif sum_of_one_comparison == 0:
                    row_comparison.append(0)
                else:
                    row_comparison.append(-1)
            all_comparisons.append(row_comparison)
        return all_comparisons

    def get_recommendation(self):
        additive = AdditiveUtilitarian(self.movies, self.get_max_rating())
        return additive.get_recommendation()
