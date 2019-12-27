import unittest
from loop.test import test_data
from loop.group_algorithm.multiplicative_utilitarian import MultiplicativeUtilitarian


class TestMultiplicativeUtilitarian(unittest.TestCase):

    def test_one(self):
        additive = MultiplicativeUtilitarian(test_data.movie_set_1, test_data.data_set_1)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score[0], [360, 450, 280])
        self.assertEqual(max_score[1], 450)
        self.assertEqual(movie, "B")

    def test_two(self):
        additive = MultiplicativeUtilitarian(test_data.movie_set_2, test_data.data_set_2)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score[0], [14, 20])
        self.assertEqual(max_score[1], 20)
        self.assertEqual(movie, "B")

    def test_three(self):
        additive = MultiplicativeUtilitarian(test_data.movie_set_3, test_data.data_set_3)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score[0], [1, 1, 1])
        self.assertEqual(max_score[1], 1)
        self.assertEqual(movie, ["A", "B", "C"])

    def test_four(self):
        additive = MultiplicativeUtilitarian(test_data.movie_set_4, test_data.data_set_4)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score[0], [900, 1176, 441, 756])
        self.assertEqual(max_score[1], 1176)
        self.assertEqual(movie, "B")

    def test_five(self):
        additive = MultiplicativeUtilitarian(test_data.movie_set_5_6, test_data.data_set_5)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score[0], [280, 100, 336, 540, 648, 800, 270, 120, 84, 420])
        self.assertEqual(max_score[1], 800)
        self.assertEqual(movie, "F")

    def test_six(self):
        additive = MultiplicativeUtilitarian(test_data.movie_set_5_6, test_data.data_set_6)
        movie = additive.get_recommendation()
        max_score = additive.get_max_rating()
        self.assertEqual(max_score[0], [100, 180, 48, 378, 630, 648, 180, 432, 210, 384])
        self.assertEqual(max_score[1], 648)
        self.assertEqual(movie, "F")

    if __name__ == '__main__':
        unittest.main()
