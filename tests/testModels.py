import unittest
import numpy as np
from catbars import Bars



class TestModels(unittest.TestCase):
    def setUp(self):        
        self.args = [[4, 1, 3, 2]]
        self.kwargs = {
            'left_labels' : ['d', 'a', 'c', 'b'],
            'right_labels' : ['D', 'A', 'C', 'B'],
            'colors' : ['DD', 'AA', 'CC', 'BB']}
        self.features = ['numbers',
                         'left_labels',
                         'right_labels',
                         'colors']
    
    def check_features(self, bars, expected_values):
        for i, att_name in enumerate(self.features):
            with self.subTest(feature = att_name):
                att = getattr(bars.data, att_name)
                self.assertEqual(att, expected_values[i])

    def test_sort_option(self):
        bars = Bars(*self.args,
                    **self.kwargs,
                    sort = True)
        expected_values = [[1, 2, 3, 4],
                           ['a', 'b', 'c', 'd'],
                           ['A', 'B', 'C', 'D'],
                           ['AA', 'BB', 'CC', 'DD']]
        self.check_features(bars, expected_values)

    def test_slice_option(self):
        bars = Bars(*self.args,
                    **self.kwargs,
                    slice = (2, 4))
        expected_values = [[ 2, 3, 1],
                           ['b', 'c', 'a'],
                           ['B','C', 'A'],
                           ['BB', 'CC', 'AA']]
        self.check_features(bars, expected_values)

    def test_slice_and_sort_options(self):
        bars = Bars(*self.args,
                    **self.kwargs,
                    slice = (2, 4),
                    sort = True)
        expected_values = [[ 1, 2, 3],
                           ['a', 'b', 'c'],
                           ['A','B', 'C'],
                           ['AA', 'BB', 'CC']]
        self.check_features(bars, expected_values)

if __name__ == '__main__':
    unittest.main()
