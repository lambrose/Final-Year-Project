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
            user_profiles.sort(key=lambda x: x[1], reverse=True)
            best_score = user_profiles[0][1]
            best_users = []
            for user, score, unseen_movies in user_profiles:
                if best_score <= 5:
                    if score > best_score * 0.8:
                        best_users.append(unseen_movies)
                elif 5 < best_score <= 30:
                    if score > best_score * 0.5:
                        best_users.append(unseen_movies)
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
        result = {}
        for key, value in dd.items():
            # get the majority voting
            if len(set(value)) > 1:
                counter = Counter(value)
                result[key] = counter.most_common(1)[0][0]
            # get the only vote
            else:
                result[key] = value[0]
        return result

    def get_recommendation(self):
        users = self.get_users()
        similar_users = self.get_similar_users(users)
        similar_users_data = self.get_similar_user_data(similar_users)
        movies = self.get_avg_vote(similar_users_data)
        if movies:
            msg_1 = "Our system has determined that you will "
            msg_2 = " this movie."
            # Query the db, to get the entry and attach the like or dislike voting recommendation
            movies = [(list(Movies.query.filter_by(title=movie)), msg_1 + vote + msg_2) for movie, vote in movies.items()]
            return {'Recommended': movies}
        else:
            return None

