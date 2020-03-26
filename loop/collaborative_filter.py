from loop.models import Users, Preferences, Movies
from flask_login import current_user
from collections import defaultdict, Counter


class CollaborativeFilter:

    def filter_user_movies(self, data_set):
        a_dict = {}
        for movie in data_set:
            if movie.like == 1:
                a_dict[movie.movie] = "like"
            else:
                a_dict[movie.movie] = "dislike"
        return a_dict

    def get_users(self):
        # Get all the movies in respect to the user logged in
        current_account = Preferences.query.filter_by(user_id=current_user.id)
        # Determine which movies have been Liked and Disliked
        current_profile = self.filter_user_movies(current_account)
        # Selecting all users
        users = Users.query.all()
        # Getting all unique users except the current user current logged in
        user_ids = [user.id for user in users if user.id != current_user.id]
        # Querying the database (select statement) for each user
        accounts = [Preferences.query.filter_by(user_id=user_id) for user_id in user_ids]
        # Determine which movies have been Liked and Disliked
        users_profiles = []
        for account in accounts:
            users_profile = self.filter_user_movies(account)
            if users_profile:
                users_profiles.append(users_profile)
        return current_profile, users_profiles

    def get_similar_users(self, users):
        if users[0]:
            user_profiles = []
            user = 0
            # iterate through all the users voted movies
            for other_user in users[1]:
                user_profile = []
                # iterate through the current user logged in
                for my_movie, my_vote in users[0].items():
                    # check if the movie is een by the other user
                    match = other_user.get(my_movie)
                    # determine if the other user liked the movie if it was found
                    if match == "like":
                        # determine if both users like the movie
                        if my_vote == match:
                            user_profile.append(1)
                        # determine if the other user likes the movie and the current user dislikes it
                        else:
                            user_profile.append(-1)

                    # Vice versa
                    elif match == "dislike":
                        if my_vote == match:
                            user_profile.append(1)
                        else:
                            user_profile.append(-1)

                # Get the movies that the other users have seen that the logged in user has not
                movies_not_seen = {movie: other_user[movie] for movie in other_user if movie not in users[0]}

                users_score = (user, sum(user_profile), movies_not_seen)
                user_profiles.append(users_score)
                user += 1
            return user_profiles
        else:
            return None

    def get_similar_user_data(self, user_profiles):
        if user_profiles:
            # sort the user profiles in descending order
            user_profiles.sort(key=lambda x: x[1], reverse=True)
            best_score = user_profiles[0][1]
            best_users = []
            for user, score, unseen_movies in user_profiles:
                # if the best user profile score is very low, then we only want the top 80% for higher accuracy
                if best_score <= 5:
                    if score > best_score * 0.8:
                        best_users.append(unseen_movies)
                # if the best user profile score is average, then we only want the top 50% for higher accuracy
                elif 5 < best_score <= 30:
                    if score > best_score * 0.5:
                        best_users.append(unseen_movies)
                # if the best user profile score is high, then we only want the top 20% for higher accuracy
                else:
                    if score > best_score * 0.2:
                        best_users.append(unseen_movies)
            return best_users
        else:
            return None

    def get_avg_vote(self, data):
        dd = defaultdict(list)
        if data:
            # If there are more than one best user profile then, users might have intersecting movies with different
            # types of votes, so we need to categorize votes based on movies
            for user in data:
                for key, value in user.items():
                    dd[key].append(value)
        result = []
        for key, value in dd.items():
            # get the majority voting
            if len(set(value)) > 1:
                counter = Counter(value)
                if counter.most_common(1)[0][0] == 'like':
                    result.append(key)
            # get the only vote
            else:
                if value[0] == 'like':
                    result.append(key)
        return result

    def get_recommendation(self):
        users = self.get_users()
        similar_users = self.get_similar_users(users)
        similar_users_data = self.get_similar_user_data(similar_users)
        movies = self.get_avg_vote(similar_users_data)
        genres = {'action': ' Action', 'adventure': 'Adventure', 'animation': 'Animation', 'comedy': 'Comedy',
                  'crime': 'Crime', 'documentary': 'Documentary', 'drama': 'Drama', 'family': 'Family',
                  'fantasy': 'Fantasy', 'history': 'History', 'horror': 'Horror', 'music': 'Music',
                  'mystery': 'Mystery', 'romance': 'Romance', 'science_fiction': 'Science Fiction',
                  'thriller': 'Thriller', 'tv_movie': 'TV Movie', 'war': 'War', 'western': 'Western'}
        if movies:
            # Query the db, to get the entry and it's details
            # movies = [list(Movies.query.filter_by(title=movie)) for movie in movies]
            movie_matches = []
            for movie in movies:
                movie_object = list(Movies.query.filter_by(title=movie))
                genre_string = ""
                if movie_object:
                    movie = movie_object[0]
                    for genre_key, genre_value in genres.items():
                        if getattr(movie, genre_key) == 1:
                            genre_string += genre_value + ", "
                    entry = (movie.title, movie.overview, movie.image, movie.popularity, movie.release_date.date(), genre_string[:-2])
                    movie_matches.append(entry)

            return {'Recommended': movie_matches}
        else:
            return None

