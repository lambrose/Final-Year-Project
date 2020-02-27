import unittest
from loop.test import test_data
from loop.group_algorithm.utilitarian_strategies import UtilitarianStrategies


class TestUtilitarianStrategies(unittest.TestCase):

    def test_one(self):
        additive = UtilitarianStrategies(test_data.movie_set_1, test_data.data_set_1)
        movie = additive.additive_utilitarian()
        max_score = additive.get_max_rating_additive()
        self.assertEqual(max_score[0], [22, 24, 21])
        self.assertEqual(max_score[1], 24)
        self.assertEqual(movie, "B")

    def test_two(self):
        additive = UtilitarianStrategies(test_data.movie_set_2, test_data.data_set_2)
        movie = additive.additive_utilitarian()
        max_score = additive.get_max_rating_additive()
        self.assertEqual(max_score[0], [9, 9])
        self.assertEqual(max_score[1], 9)
        self.assertEqual(movie, ["A", "B"])

    def test_three(self):
        additive = UtilitarianStrategies(test_data.movie_set_3, test_data.data_set_3)
        movie = additive.additive_utilitarian()
        max_score = additive.get_max_rating_additive()
        self.assertEqual(max_score[0], [3, 3, 3])
        self.assertEqual(max_score[1], 3)
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four(self):
        additive = UtilitarianStrategies(test_data.movie_set_4, test_data.data_set_4)
        movie = additive.additive_utilitarian()
        max_score = additive.get_max_rating_additive()
        self.assertEqual(max_score[0], [30, 25, 24, 22])
        self.assertEqual(max_score[1], 30)
        self.assertEqual(movie, "A")

    def test_five(self):
        additive = UtilitarianStrategies(test_data.movie_set_5_6, test_data.data_set_5)
        movie = additive.additive_utilitarian()
        max_score = additive.get_max_rating_additive()
        self.assertEqual(max_score[0], [20, 21, 21, 25, 26, 28, 22, 15, 14, 23])
        self.assertEqual(max_score[1], 28)
        self.assertEqual(movie, "F")

    def test_six(self):
        additive = UtilitarianStrategies(test_data.movie_set_5_6, test_data.data_set_6)
        movie = additive.additive_utilitarian()
        max_score = additive.get_max_rating_additive()
        self.assertEqual(max_score[0], [21, 18, 13, 22, 26, 26, 17, 23, 20, 22])
        self.assertEqual(max_score[1], 26)
        self.assertEqual(movie, ["E", "F"])

    if __name__ == '__main__':
        unittest.main()
