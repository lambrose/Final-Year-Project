import unittest
from loop.algorithm import Algorithms


class TestAlgorithm(unittest.TestCase):

    def test_one(self):
        values = ['User 1', '1', 'User 2', '3', 'User 3', '3', 'Users:,movie_1']
        additive = Algorithms(values)
        data = additive.process_data()
        result = ['movie_1'], [[1], [3], [3]]
        self.assertEqual(data, result)

    def test_two(self):
        values = ['User 1', '1', '2', 'User 2', '3', '9', 'User 3', '3', '5', 'Users:,movie_1,movie_2']
        additive = Algorithms(values)
        data = additive.process_data()
        result = ['movie_1', 'movie_2'], [[1, 2], [3, 9], [3, 5]]
        self.assertEqual(data, result)

    def test_three(self):
        values = ['User 1', '1', '2', '3', 'User 2', '3', '9', '4', 'User 3', '3', '5', '6',
                  'Users:,movie_1,movie_2, movie_3']
        additive = Algorithms(values)
        data = additive.process_data()
        result = ['movie_1', 'movie_2', ' movie_3'], [[1, 2, 3], [3, 9, 4], [3, 5, 6]]
        self.assertEqual(data, result)

    if __name__ == '__main__':
        unittest.main()
