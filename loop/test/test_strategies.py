import unittest
from loop.test import test_data
from loop.group_algorithm.strategies import Strategies


class TestStrategies(unittest.TestCase):

    def test_one_least_misery(self):
        additive = Strategies(test_data.movie_set_1, test_data.data_set_1)
        movie = additive.least_misery()
        max_score = additive.minimum_value()
        self.assertEqual(max_score, [5, 5, 4])
        self.assertEqual(movie, ['A', 'B'])

    def test_two_least_misery(self):
        additive = Strategies(test_data.movie_set_2, test_data.data_set_2)
        movie = additive.least_misery()
        max_score = additive.minimum_value()
        self.assertEqual(max_score, [2, 4])
        self.assertEqual(movie, "B")

    def test_three_least_misery(self):
        additive = Strategies(test_data.movie_set_3, test_data.data_set_3)
        movie = additive.least_misery()
        max_score = additive.minimum_value()
        self.assertEqual(max_score, [1, 1, 1])
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four_least_misery(self):
        additive = Strategies(test_data.movie_set_4, test_data.data_set_4)
        movie = additive.least_misery()
        max_score = additive.minimum_value()
        self.assertEqual(max_score, [1, 3, 1, 3])
        self.assertEqual(movie, ['B', 'D'])

    def test_five_least_misery(self):
        additive = Strategies(test_data.movie_set_5_6, test_data.data_set_5)
        movie = additive.least_misery()
        max_score = additive.minimum_value()
        self.assertEqual(max_score, [5, 1, 6, 6, 8, 8, 3, 4, 3, 6])
        self.assertEqual(movie, ['E', 'F'])

    def test_six_least_misery(self):
        additive = Strategies(test_data.movie_set_5_6, test_data.data_set_6)
        movie = additive.least_misery()
        max_score = additive.minimum_value()
        self.assertEqual(max_score, [1, 4, 2, 6, 7, 8, 5, 6, 3, 6])
        self.assertEqual(movie, "F")

    def test_one_most_pleasure(self):
        additive = Strategies(test_data.movie_set_1, test_data.data_set_1)
        movie = additive.most_pleasure()
        max_score = additive.maximum_value()
        self.assertEqual(max_score, [9, 10, 10])
        self.assertEqual(movie, ['B', 'C'])

    def test_two_most_pleasure(self):
        additive = Strategies(test_data.movie_set_2, test_data.data_set_2)
        movie = additive.most_pleasure()
        max_score = additive.maximum_value()
        self.assertEqual(max_score, [7, 5])
        self.assertEqual(movie, "A")

    def test_three_most_pleasure(self):
        additive = Strategies(test_data.movie_set_3, test_data.data_set_3)
        movie = additive.most_pleasure()
        max_score = additive.maximum_value()
        self.assertEqual(max_score, [1, 1, 1])
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four_most_pleasure(self):
        additive = Strategies(test_data.movie_set_4, test_data.data_set_4)
        movie = additive.most_pleasure()
        max_score = additive.maximum_value()
        self.assertEqual(max_score, [10, 8, 9, 7])
        self.assertEqual(movie, 'A')

    def test_five_most_pleasure(self):
        additive = Strategies(test_data.movie_set_5_6, test_data.data_set_5)
        movie = additive.most_pleasure()
        max_score = additive.maximum_value()
        self.assertEqual(max_score, [8, 10, 8, 10, 9, 10, 10, 6, 7, 10])
        self.assertEqual(movie, ['B', 'D', 'F', 'G', 'J'])

    def test_six_most_pleasure(self):
        additive = Strategies(test_data.movie_set_5_6, test_data.data_set_6)
        movie = additive.most_pleasure()
        max_score = additive.maximum_value()
        self.assertEqual(max_score, [10, 9, 8, 9, 10, 9, 6, 9, 10, 8])
        self.assertEqual(movie, ['A', 'E', 'I'])

    def test_one_average_without_misery(self):
        additive = Strategies(test_data.movie_set_1, test_data.data_set_1)
        movie = additive.average_without_misery()
        max_score = additive.average_value()
        self.assertEqual(max_score, [22, 24, 21])
        self.assertEqual(movie, 'B')

    def test_two_average_without_misery(self):
        additive = Strategies(test_data.movie_set_2, test_data.data_set_2)
        movie = additive.average_without_misery()
        max_score = additive.average_value()
        self.assertEqual(max_score, [0, 9])
        self.assertEqual(movie, "B")

    def test_three_average_without_misery(self):
        additive = Strategies(test_data.movie_set_3, test_data.data_set_3)
        movie = additive.average_without_misery()
        max_score = additive.average_value()
        self.assertEqual(max_score, [0, 0, 0])
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four_average_without_misery(self):
        additive = Strategies(test_data.movie_set_4, test_data.data_set_4)
        movie = additive.average_without_misery()
        max_score = additive.average_value()
        self.assertEqual(max_score, [0, 0, 0, 0])
        self.assertEqual(movie, ["A", "B", "C", "D"])

    def test_five_average_without_misery(self):
        additive = Strategies(test_data.movie_set_5_6, test_data.data_set_5)
        movie = additive.average_without_misery()
        max_score = additive.average_value()
        self.assertEqual(max_score, [20, 0, 21, 25, 26, 28, 0, 15, 0, 23])
        self.assertEqual(movie, 'F')

    def test_six_average_without_misery(self):
        additive = Strategies(test_data.movie_set_5_6, test_data.data_set_6)
        movie = additive.average_without_misery()
        max_score = additive.average_value()
        self.assertEqual(max_score, [0, 18, 0, 22, 26, 26, 17, 23, 0, 22])
        self.assertEqual(movie, ['E', 'F'])

    if __name__ == '__main__':
        unittest.main()
