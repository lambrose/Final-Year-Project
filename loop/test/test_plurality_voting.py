import unittest
from loop.test import test_data
from loop.group_algorithm.plurality_voting import PluralityVoting


class TestPluralityVoting(unittest.TestCase):

    def test_one(self):
        plurality_voting = PluralityVoting(test_data.movie_set_1, test_data.data_set_1)
        movie = plurality_voting.get_recommendation()
        self.assertEqual(plurality_voting.ordered_movie_indexes, [[1], [0], [2]])
        self.assertEqual(movie, "B")

    def test_two(self):
        plurality_voting = PluralityVoting(test_data.movie_set_2, test_data.data_set_2)
        movie = plurality_voting.get_recommendation()
        self.assertEqual(plurality_voting.ordered_movie_indexes, [[0, 1]])
        self.assertEqual(movie, ['A', 'B'])

    def test_three(self):
        plurality_voting = PluralityVoting(test_data.movie_set_3, test_data.data_set_3)
        movie = plurality_voting.get_recommendation()
        self.assertEqual(plurality_voting.ordered_movie_indexes, [[0, 1, 2]])
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four(self):
        plurality_voting = PluralityVoting(test_data.movie_set_4, test_data.data_set_4)
        movie = plurality_voting.get_recommendation()
        self.assertEqual(plurality_voting.ordered_movie_indexes, [[0], [1, 2], [3]])
        self.assertEqual(movie, "A")

    def test_five(self):
        plurality_voting = PluralityVoting(test_data.movie_set_5_6, test_data.data_set_5)
        movie = plurality_voting.get_recommendation()
        self.assertEqual(plurality_voting.ordered_movie_indexes, [[1, 5], [3, 6], [4], [0, 9], [2], [7, 8]])
        self.assertEqual(movie, ['B', 'F'])

    def test_six(self):
        plurality_voting = PluralityVoting(test_data.movie_set_5_6, test_data.data_set_6)
        movie = plurality_voting.get_recommendation()
        self.assertEqual(plurality_voting.ordered_movie_indexes, [[0], [4], [5], [8, 3], [7], [9], [6, 1], [2]])
        self.assertEqual(movie, "A")

    def test_seven(self):
        movie_set_7 = ["A", "B", "C"]
        data_set_7 = [[1, 2, 3], [6, 5, 4], [7, 8, 7]]
        plurality_voting = PluralityVoting(movie_set_7, data_set_7)
        movie = plurality_voting.get_recommendation()
        self.assertEqual(plurality_voting.ordered_movie_indexes, [[1], [2, 0]])
        self.assertEqual(movie, "B")

    if __name__ == '__main__':
        unittest.main()
