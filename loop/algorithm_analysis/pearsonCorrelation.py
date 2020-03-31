import numpy as np
import math
from math import sqrt
import scipy.stats
import scipy.spatial
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


class PearsonCorrelation:
    # number of users in the data set
    users = 50
    # number of movies in the data set
    items = 1084

    # users = 100
    # items = 2084

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

    def get_user_similarity(self, data):
        # form a matrix of length users and height users
        similarity_matrix = np.zeros((self.users, self.users))
        # compare all users with each other
        for user_a in range(self.users):
            for user_b in range(self.users):
                # check if the two users being compared have seen and rated movies
                if np.count_nonzero(data[user_a]) and np.count_nonzero(data[user_b]):
                    try:
                        # check that the similarity score is not NaN
                        if not math.isnan(scipy.stats.pearsonr(data[user_a], data[user_b])[0]):
                            # if not assign that co ordinate in the matrix the similarity score
                            similarity_matrix[user_a][user_b] = scipy.stats.pearsonr(data[user_a], data[user_b])[0]
                        else:
                            # else assign that co ordinate in the matrix zero
                            similarity_matrix[user_a][user_b] = 0
                    except:
                        similarity_matrix[user_a][user_b] = 0
        return similarity_matrix

    def crossValidation(self, data, user_id):
        # initialize the 10 fold cross-validation instance
        k_fold = KFold(n_splits=10)
        # form a matrix of length items and height users
        matrix = np.zeros((self.users, self.items))
        # populate the matrix
        for entry in data:
            # replacing zeros ratings
            matrix[entry[0] - 1][entry[1] - 1] = entry[2]

        user_similarity = self.get_user_similarity(matrix)

        root_mean_squared_error = []
        average = []

        # get all the movies rated for one particular user
        current_user = [index for index in data if index[0] == user_id]
        for train_indices, test_indices in k_fold.split(current_user):
            # split a users data into testing and training
            test = [data[i] for i in test_indices]
            train = [i for i in data if i not in test]

            # training matrix
            training_model = np.zeros((self.users, self.items))
            # populate the matrix
            for entry in train:
                # replacing zeros ratings
                training_model[entry[0] - 1][entry[1] - 1] = entry[2]

            actual = []
            prediction = []

            for entry in test:
                actual.append(entry[2])

                # if movie is not seen by anyone, determine a neutral answer
                outcome = 3.0

                # check if the user has rated movies
                if np.count_nonzero(training_model[entry[0] - 1]):
                    # get the similar users who have seen the movie
                    sim_pearson = user_similarity[entry[0] - 1]
                    # determine users who have seen the movie
                    ind = (training_model[:, entry[1] - 1] > 0)

                    normal_pearson = np.sum(np.absolute(sim_pearson[ind]))

                    if normal_pearson > 0:
                        outcome = np.dot(sim_pearson, training_model[:, entry[1] - 1]) / normal_pearson

                if outcome < 0:
                    outcome = 0

                if outcome > 5:
                    outcome = 5

                prediction.append(outcome)

            root_mean_squared_error.append(sqrt(mean_squared_error(actual, prediction)))
            correct_prediction = []
            # checking for a match
            for p, a in zip(prediction, actual):
                if 4.0 <= p <= 5.0:
                    if 4.0 <= a <= 5.0:
                        correct_prediction.append(p)
                elif 3.0 <= p <= 4.0:
                    if 3.0 <= a <= 4.0:
                        correct_prediction.append(p)
                elif 2.0 <= p <= 3.0:
                    if 2.0 <= a <= 3.0:
                        correct_prediction.append(p)
                elif 1.0 <= p <= 2.0:
                    if 1.0 <= a <= 2.0:
                        correct_prediction.append(p)

            average.append(len(correct_prediction) / len(actual))
        avg_accuracy = sum(average) / float(len(average)) * 100

        print("-------------------------")
        print(str(avg_accuracy))


pearson_correlation = PearsonCorrelation()
recommend_data = pearson_correlation.read_file("movie_lens_data/pearson_data_50.csv")
for user in range(1, 21):
    pearson_correlation.crossValidation(recommend_data, user)
