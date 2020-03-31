from collections import defaultdict
from loop.algorithm_analysis.algs import Algorithms


def run():
    alg = Algorithms(entry)
    # Adding all movie results to a list dynamically
    movies, rates = alg.process_data()
    users_results = []
    for user_rating in rates:
        # sort an individual user  ratings in descending order
        sorted_ratings = sorted(enumerate(user_rating), key=lambda x: x[1], reverse=True)
        default_dict = defaultdict(list)
        for index, value in sorted_ratings:
            # save the rating as the key and the movie positions at the value
            # this groups all movie positions together with the same rating
            default_dict[value].append(index)
        user_grouped_movies = [[movies[index] for index in value] for key, value, in default_dict.items()]
        users_results.append(user_grouped_movies)
    algorithms_names = ["Additive Utilitarian Strategy", "Multiplicative Utilitarian Strategy", "Borda Count",
                        "Copeland Rule", "Plurality Voting", "Approval Voting", "Least Misery Strategy",
                        "Most Pleasure Strategy", "Average Without Misery Strategy"]
    algorithms_results = [alg.additive(), alg.multiplicative(), alg.borda(), alg.copeland(), alg.plurality_voting(),
                          alg.approval(), alg.least_misery(), alg.most_pleasure(), alg.average_without_misery()]

    algorithms_performances = []
    for algorithm_results in algorithms_results:
        users_matches = []
        # for a particular algorithm compare it with all user ratings
        for user_results in users_results:
            user_matches = []
            for algorithm_result, user_result in zip(algorithm_results, user_results):
                # if the user and algorithm have the same movie in that position
                if algorithm_result == user_result:
                    user_matches.append(1)
                # check for an intersection
                elif list(set(algorithm_result) & set(user_result)):
                    # divide the amount of movies found in the intersection by the universe of both lists
                    ratio = len(list(set(algorithm_result) & set(user_result))) / len(set(algorithm_result+user_result))
                    user_matches.append(ratio)
            accuracy = sum(user_matches) / len(user_results)
            users_matches.append(accuracy)
            # add all users data in relation to that algorithm
        algorithms_performances.append(users_matches)

    for algorithm_performances, algorithm_name in zip(algorithms_performances, algorithms_names):
        print(algorithm_name + ":")
        accuracy = sum(algorithm_performances) / len(algorithm_performances)
        # user = 1
        # for algorithm_performance in algorithm_performances:
        #     print("user", user, " preference:", algorithm_performance)
        #     user += 1
        print("Total Users preference accuracy:", accuracy)
        print("\n")


# entry = ['User:', 'M_A', 'M_B', 'M_C', 'M_D',
#          'User 1:', '2', '2', '2', '2',
#          'User 2:', '2', '2', '2', '2',
#          'User 3:', '2', '2', '2', '2']

# entry = ['User:', 'M_A', 'M_B', 'M_C', 'M_D',
#          'User 1:', '2', '5', '1', '4',
#          'User 2:', '4', '3', '2', '4',
#          'User 3:', '3', '3', '1', '5']

entry = ['User:', 'M_A', 'M_B', 'M_C', 'M_D', 'M_E', 'M_F',
         'User 1:', '7', '7', '7', '5', '9', '7',
         'User 2:', '9', '7', '2', '5', '8', '2',
         'User 3:', '7', '10', '9', '4', '6', '3',
         'User 4:', '4', '9', '6', '9', '5', '8',
         'User 5:', '6', '8', '10', '2', '10', '4',
         'User 6:', '3', '9', '8', '8', '2', '6',
         'User 7:', '5', '7', '4', '6', '9', '3',
         'User 8:', '5', '2', '4', '10', '8', '1',
         'User 9:', '5', '8', '4', '10', '9', '6',
         'User 10:', '6', '8', '5', '8', '10', '6']

if __name__ == '__main__':
    run()
