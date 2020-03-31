from sklearn.model_selection import KFold
from collections import Counter


class CollaborativeFilter:

    # read in the csv file and format the data
    def read_file(self, filename):
        csv_file = open(filename, "r")
        data = []
        for row in csv_file:
            # convert the string into a list
            values = row.split(',')
            # specify indexes wanted (fourth index is a time stamp, not needed)
            entry = [int(values[0]), int(values[1]), int(values[2])]
            data.append(entry)
        return data

    def filter_user_movies(self, data_set):
        a_dict = {}
        # get rid of entries with a rating score of zero
        # convert the layout from a list to a dict
        # item number as they key and the rating as the value
        for movie in data_set:
            if movie[2] == 1:
                a_dict[movie[1]] = 1
            elif movie[2] == -1:
                a_dict[movie[1]] = -1
        return a_dict

    def get_users(self, current_account, accounts):
        # Determine which movies have been Liked and Disliked
        current_profile = self.filter_user_movies(current_account)

        # Determine which movies have been Liked and Disliked
        users_profiles = []
        for account in accounts:
            users_profile = self.filter_user_movies(account)
            if users_profile:
                users_profiles.append(users_profile)
        return current_profile, users_profiles

    def get_similar_users(self, users):
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
                if match == 1:
                    # determine if both users like the movie
                    if my_vote == match:
                        user_profile.append(1)
                    # determine if the other user likes the movie and the current user dislikes it
                    else:
                        user_profile.append(-1)

                # Vice versa
                elif match == -1:
                    if my_vote == match:
                        user_profile.append(1)
                    else:
                        user_profile.append(-1)

            users_score = (user, sum(user_profile))
            user_profiles.append(users_score)
            user += 1
        user_profiles.sort(key=lambda x: x[1], reverse=True)
        # get the most similar score
        best_score = user_profiles[0][1]
        best_users = []
        for user, score in user_profiles:
            if best_score <= 5:
                # if the best similar user score is very little then only use the top 20% of similar users
                if score > best_score * 0.8:
                    best_users.append(users[1][user])
                    #  use the top 50% of similar users
            elif 5 < best_score <= 30:
                if score > best_score * 0.5:
                    best_users.append(users[1][user])
            else:
                # if the best similar user score is large then use the top 80% of similar users
                if score > best_score * 0.2:
                    best_users.append(users[1][user])
        return best_users

    def cross_validation(self, current_user):
        k_fold = KFold(n_splits=10)
        loop_avg = []

        data_set = self.read_file("movie_lens_data/loop_data_50.csv")
        # Get all the movies in respect to the user logged in
        current_account = [data for data in data_set if data[0] == current_user]
        # Getting all unique users except the current user current logged in
        user_ids = list(set([user[0] for user in data_set if user[0] != current_user]))
        # Querying the database (select statement) for each user
        accounts = [[data for data in data_set if data[0] == user_id] for user_id in user_ids]
        # split the data on a cross-validation score of 10
        for train_indices, test_indices in k_fold.split(current_account):
            # split data into training and testing
            test = [current_account[index] for index in test_indices]
            train = [entry for entry in current_account if entry not in test]
            # get most similar users from training data
            users = self.get_users(train, accounts)
            similar_users_items = self.get_similar_users(users)
            # calculating the majority preference vote so that is none of the similar users have seen the movie
            # that we are predicting for, we can substitute it with the most frequent used preference
            counter = Counter([row[2] for row in train])
            prediction_filler = counter.most_common(2)
            if prediction_filler[0][0] == 0:
                prediction_filler = prediction_filler[1][0]
            else:
                prediction_filler = prediction_filler[0][0]

            predictions = []
            actual_ratings = []

            for entry in test:
                # check for entries that are a 1 or -1
                if entry[2] != 0:
                    # store actual ratings
                    if entry[2] == 1:
                        actual_ratings.append(1)
                    elif entry[2] == -1:
                        actual_ratings.append(-1)

                    all_values = []
                    for item in range(len(similar_users_items)):
                        # check in all similar user entries if it contains the movie that needs a prediction rating
                        result = similar_users_items[item].get(entry[1])
                        if result:
                            # if result found, then store it
                            all_values.append(result)

                    value = None
                    # if multiple users rated a specific movie, then get the majority preference
                    # else use a filler
                    if all_values:
                        counter = Counter(all_values)
                        value = counter.most_common(1)[0][0]

                    if value:
                        predictions.append(value)
                    else:
                        predictions.append(prediction_filler)

            if len(actual_ratings) and len(predictions):
                # calculate the average accuracy
                correct_prediction = [actual for prediction, actual in zip(predictions, actual_ratings) if prediction == actual]
                loop_avg.append(len(correct_prediction) / len(actual_ratings))
        avg_accuracy = sum(loop_avg) / float(len(loop_avg)) * 100
        print("-------------------------")
        print(avg_accuracy)


cf = CollaborativeFilter()
for i in range(1, 21):
    cf.cross_validation(i)
