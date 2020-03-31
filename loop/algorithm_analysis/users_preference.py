from collections import defaultdict
from loop.algorithm_analysis.algs import Algorithms


def run():
    alg = Algorithms(entry)
    # Adding all movie results to a list dynamically
    movies, rates = alg.process_data()
    users = []
    for user_rating in rates:
        # sort an individual user  ratings in descending order
        sorted_ratings = sorted(enumerate(user_rating), key=lambda x: x[1], reverse=True)
        default_dict = defaultdict(list)
        for index, value in sorted_ratings:
            # save the rating as the key and the movie positions at the value
            # this groups all movie positions together with the same rating
            default_dict[value].append(index)
        user_grouped_movies = [movies[movie_index] for movie_index in default_dict[list(default_dict.keys())[0]]]
        users.append(user_grouped_movies)
    algorithms_names = ["Additive Utilitarian Strategy", "Multiplicative Utilitarian Strategy", "Borda Count",
                        "Copeland Rule", "Plurality Voting", "Approval Voting", "Least Misery Strategy",
                        "Most Pleasure Strategy", "Average Without Misery Strategy"]
    algorithms_results = [alg.additive()[0], alg.multiplicative()[0], alg.borda()[0], alg.copeland()[0],
                          alg.plurality_voting()[0], alg.approval()[0], alg.least_misery()[0],
                          alg.most_pleasure()[0], alg.average_without_misery()[0]]

    algorithms_performances = []
    for algorithm_results in algorithms_results:
        users_matches = []
        for user in users:
            accuracy = 0
            # if the there is a perfect match
            if algorithm_results == user:
                accuracy = 1
            # if there are multiple movies in first place for either the user or algorithm
            # check for an intersection
            elif list(set(algorithm_results) & set(user)):
                # divide the amount of movies found in the intersection by the universe of both lists
                ratio = len(list(set(algorithm_results) & set(user))) / len(set(algorithm_results + user))
                accuracy = ratio
            # add all user matches to a list
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
