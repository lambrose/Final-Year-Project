import unittest
from loop.algorithm import Algorithms


class TestAlgorithm(unittest.TestCase):

    def test_one(self):
        values = ['User:', 'Jumanji: The Next Level', 'User 1:', '5', 'User 2:', '4', 'User 3:', '8']
        algorithm = Algorithms(values)
        data = algorithm.process_data()
        result = ['Jumanji: The Next Level'], [[5], [4], [8]]
        self.assertEqual(data, result)

    def test_two(self):
        values = ['User:', 'Jumanji: The Next Level', 'Seberg', 'User 1:', '5', '3', 'User 2:', '4', '9',
                  'User 3:', '8', '3']
        algorithm = Algorithms(values)
        data = algorithm.process_data()
        result = ['Jumanji: The Next Level', 'Seberg'], [[5, 3], [4, 9], [8, 3]]
        self.assertEqual(data, result)

    def test_three(self):
        values = ['User:', 'Jumanji: The Next Level', 'Seberg', '1917', 'User 1:', '5', '8', '3', 'User 2:', '4',
                  '4', '9', 'User 3:', '8', '3', '8']
        algorithm = Algorithms(values)
        data = algorithm.process_data()
        result = ['Jumanji: The Next Level', 'Seberg', '1917'], [[5, 8, 3], [4, 4, 9], [8, 3, 8]]
        self.assertEqual(data, result)

    if __name__ == '__main__':
        unittest.main()
