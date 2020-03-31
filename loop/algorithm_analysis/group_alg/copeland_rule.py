from loop.algorithm_analysis.group_alg.utilitarian_strategies import UtilitarianStrategies


class CopelandRule:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def copeland_table(self):
        # Separating the users ratings into ratings based on a specific movie
        ratings_separated_by_column = [rating for rating in zip(*self.ratings)]

        all_comparisons = []
        # Compare one movie ratings with all other movie ratings
        for column_ratings in ratings_separated_by_column:
            row_comparison = []
            for compare_column_ratings in ratings_separated_by_column:
                comparison = []
                # Compare itself with its neighbour
                for rating, compare_rating in zip(column_ratings, compare_column_ratings):
                    if rating > compare_rating:
                        comparison.append(-1)
                    elif rating == compare_rating:
                        comparison.append(0)
                    else:
                        comparison.append(1)
                # Calculate the sum of results from the comparison
                sum_of_comparison = sum(comparison)
                # Then assign a score with respect to the movie compared to
                if sum_of_comparison > 0:
                    row_comparison.append(1)
                elif sum_of_comparison == 0:
                    row_comparison.append(0)
                else:
                    row_comparison.append(-1)
            all_comparisons.append(row_comparison)
        return all_comparisons

    # Using the additive algorithm to determine the recommendation
    def get_recommendation(self):
        additive = UtilitarianStrategies(self.movies, self.copeland_table())
        return additive.additive_utilitarian()
