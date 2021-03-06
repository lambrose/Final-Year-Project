class PluralityVoting:

    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    counter = 1
    ordered_movie_indexes = []

    def enumerate_movie_ratings(self):
        # reset global values
        self.counter = 1
        self.ordered_movie_indexes = []
        # Separating the users ratings into ratings based on a specific movie
        # Also finding the indexes so it can be used to remove movies, later on
        return [[rating for rating in enumerate(ratings)] for ratings in self.ratings]

    def calculate_plurality_voting(self, is_match, movie_ratings):
        highest_rated_movies = []
        if is_match:
            for ratings in movie_ratings:
                # Getting th all the movies indexes that correspond to the highest rating for each user
                movies = [rating[0] for rating in ratings if max(ratings, key=lambda item: item[1])[1] == rating[1]]
                highest_rated_movies.append(movies)
        else:
            # No previous match was found
            sorted_ratings = [sorted(ratings, key=lambda item: item[1], reverse=True) for ratings in movie_ratings]
            for ratings in sorted_ratings:
                rating_values = []
                for rating in ratings:
                    # Getting a specific amount of unique movie max ratings
                    if len(set(rating_values)) < self.counter:
                        rating_values.append(rating[1])
                # For each max rating, get the associated movie, there may be many movies with the same rating
                rating_index = [rating[0] for rating_value in rating_values for rating in ratings if
                                rating[1] == rating_value]
                highest_rated_movies.append(rating_index)

        intersection_values = []
        # Check if there are any common movies in all users top movies
        if list(set.intersection(*map(set, highest_rated_movies))):
            for value in list(set.intersection(*map(set, highest_rated_movies))):
                intersection_values.append(value)
        else:
            # If not, check if there are common movies in some of the users top movies
            index = 1
            # Compare each users movies without comparing themselves
            for rating_index in highest_rated_movies[:-1]:
                for rating_index_comparison in highest_rated_movies[index:]:
                    # Check for common movies
                    if list(set(rating_index) & set(rating_index_comparison)):
                        for value in list(set(rating_index) & set(rating_index_comparison)):
                            if value not in intersection_values:
                                intersection_values.append(value)
                index += 1
        # If a common movie was found between users, then remove it from remaining movies
        if intersection_values:
            for value in intersection_values:
                for ratings in movie_ratings:
                    for rating in ratings:
                        if rating[0] == value:
                            ratings.pop(ratings.index(rating))

            if intersection_values:
                self.ordered_movie_indexes.append(intersection_values)
            # If there are still remaining movies to be ranked, use recursion
            if movie_ratings[0]:
                self.calculate_plurality_voting(True, movie_ratings)
        # If there was no matches found between movies
        else:
            # Use recursion to try again and set the "is_match" boolean to false so more values can be considered
            # The counter value is used to determine how many diff. max values should be taken next
            self.counter += 1
            self.calculate_plurality_voting(False, movie_ratings)

    # Get the recommended movie or movies
    def get_recommendation(self):
        self.calculate_plurality_voting(True, self.enumerate_movie_ratings())
        movies = []
        for rating in self.ordered_movie_indexes:
            category = []
            for index in rating:
                category.append(self.movies[index])
            movies.append(category)
        return movies
