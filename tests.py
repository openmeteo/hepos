#!/usr/bin/python

import unittest

from pyhepos import (htrs07_to_egsa87_3d, htrs07_to_egsa87_en_temp)


class TestTransformations(unittest.TestCase):
    
    def test_htrs07_to_ggrs87_3d(self):
        result = htrs07_to_egsa87_3d(
                4382064.771,
                2023782.319,
                4155326.131)
        self.assertAlmostEqual(result[0], 4382266.647, delta=0.001)
        self.assertAlmostEqual(result[1], 2023708.046, delta=0.001)
        self.assertAlmostEqual(result[2], 4155081.709, delta=0.001)

    def test_htrs07_to_egsa87_en_temp(self):
        result = htrs07_to_egsa87_en_temp(
                4382064.771,
                2023782.319,
                4155326.131)
        self.assertAlmostEqual(result[0], 566296.660, delta=0.001)
        self.assertAlmostEqual(result[1], 4529332.491, delta=0.001)


if __name__ == '__main__':
    unittest.main()
