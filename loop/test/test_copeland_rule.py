import unittest
from loop.test import test_data
from loop.group_algorithm.copeland_rule import CopelandRule


class TestCopelandRule(unittest.TestCase):

    def test_one(self):
        additive = CopelandRule(test_data.movie_set_1, test_data.data_set_1)
        movie = additive.get_recommendation()
        max_score = additive.copeland_table()
        self.assertEqual(max_score, [[0, 1, -1], [-1, 0, -1], [1, 1, 0]])
        self.assertEqual(movie, "B")

    def test_two(self):
        additive = CopelandRule(test_data.movie_set_2, test_data.data_set_2)
        movie = additive.get_recommendation()
        max_score = additive.copeland_table()
        self.assertEqual(max_score, [[0, 0], [0, 0]])
        self.assertEqual(movie, ["A", "B"])

    def test_three(self):
        additive = CopelandRule(test_data.movie_set_3, test_data.data_set_3)
        movie = additive.get_recommendation()
        max_score = additive.copeland_table()
        self.assertEqual(max_score, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four(self):
        additive = CopelandRule(test_data.movie_set_4, test_data.data_set_4)
        movie = additive.get_recommendation()
        max_score = additive.copeland_table()
        self.assertEqual(max_score, [[0, -1, -1, -1], [1, 0, 0, -1], [1, 0, 0, -1], [1, 1, 1, 0]])
        self.assertEqual(movie, "A")

    def test_five(self):
        additive = CopelandRule(test_data.movie_set_5_6, test_data.data_set_5)
        movie = additive.get_recommendation()
        max_score = additive.copeland_table()
        self.assertEqual(max_score, [[0, 1, -1, 1, 1, 1, 1, -1, -1, 0], [-1, 0, -1, 0, -1, 0, 0, -1, -1, -1],
                                     [1, 1, 0, 1, 1, 1, 1, -1, -1, 1], [-1, 0, -1, 0, -1, 1, -1, -1, -1, -1],
                                     [-1, 1, -1, 1, 0, 1, 1, -1, -1, -1], [-1, 0, -1, -1, -1, 0, -1, -1, -1, -1],
                                     [-1, 0, -1, 1, -1, 1, 0, -1, -1, -1], [1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                                     [1, 1, 1, 1, 1, 1, 1, 0, 0, 1], [0, 1, -1, 1, 1, 1, 1, -1, -1, 0]])
        self.assertEqual(movie, "F")

    def test_six(self):
        additive = CopelandRule(test_data.movie_set_5_6, test_data.data_set_6)
        movie = additive.get_recommendation()
        max_score = additive.copeland_table()
        self.assertEqual(max_score, [[0, -1, -1, -1, 0, -1, -1, -1, 0, -1], [1, 0, -1, 1, 1, 1, 0, 1, 1, 1],
                                     [1, 1, 0, 1, 1, 1, 1, 1, 1, 1], [1, -1, -1, 0, 1, 1, -1, 0, 0, -1],
                                     [0, -1, -1, -1, 0, -1, -1, -1, -1, -1], [1, -1, -1, -1, 1, 0, -1, -1, -1, -1],
                                     [1, 0, -1, 1, 1, 1, 0, 1, 1, 1], [1, -1, -1, 0, 1, 1, -1, 0, 1, -1],
                                     [0, -1, -1, 0, 1, 1, -1, -1, 0, -1], [1, -1, -1, 1, 1, 1, -1, 1, 1, 0]])
        self.assertEqual(movie, "E")

    if __name__ == '__main__':
        unittest.main()
