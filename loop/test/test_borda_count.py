import unittest
from loop.test import test_data
from loop.group_algorithm.borda_count import BordaCount


class TestBordaCount(unittest.TestCase):

    def test_one(self):
        additive = BordaCount(test_data.movie_set_1, test_data.data_set_1)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score, [[1, 2, 0], [1, 2, 0], [0.5, 0.5, 2]])
        self.assertEqual(movie, "B")

    def test_two(self):
        additive = BordaCount(test_data.movie_set_2, test_data.data_set_2)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score, [[0, 1], [1, 0]])
        self.assertEqual(movie, ["A", "B"])

    def test_three(self):
        additive = BordaCount(test_data.movie_set_3, test_data.data_set_3)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score, [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four(self):
        additive = BordaCount(test_data.movie_set_4, test_data.data_set_4)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score, [[0.5, 2.5, 0.5, 2.5], [2.5, 1, 2.5, 0], [3, 1.5, 1.5, 0], [3, 1.5, 1.5, 0]])
        self.assertEqual(movie, "A")

    def test_five(self):
        additive = BordaCount(test_data.movie_set_5_6, test_data.data_set_5)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score, [[4.5, 8.0, 3, 8.0, 6, 4.5, 8.0, 1.5, 0, 1.5],
                                     [3.5, 8.5, 2, 6.5, 5, 8.5, 6.5, 0.5, 0.5, 3.5],
                                     [2.5, 0, 6, 4, 7, 8.5, 1, 2.5, 5, 8.5]])
        self.assertEqual(movie, "F")

    def test_six(self):
        additive = BordaCount(test_data.movie_set_5_6, test_data.data_set_6)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score, [[8, 1, 0, 2.5, 8, 6, 2.5, 4.5, 8, 4.5], [0, 7.5, 4.5, 7.5, 3, 7.5, 2, 7.5, 1, 4.5],
                                     [9, 1.5, 0, 5.5, 8, 7, 1.5, 3.5, 5.5, 3.5]])
        self.assertEqual(movie, "F")

    if __name__ == '__main__':
        unittest.main()
