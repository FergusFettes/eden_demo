import sys, os
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
import random as ra
import array
import numpy as np
from numpy import testing
import unittest
import unittest.mock

from main import (
    choose_neumann_neighbor, neumann_neighbors_sum, neumann_neighbors_same,
    moore_neighbors_sum, moore_neighbors_same, ising, conway, conway_old,
    make_universe,
)

debug = True


class NeighborTestCase(unittest.TestCase):

    def setUp(self):
        self.uni = make_universe(size=10, edge_ratio=1, init='none')
        self.uni.data[1:3, 1:3] = 1
        self.uni.back = uni.data

    def test_moore_neighbors_sum(self):
        testing.assertEqual(moore_neighbors_sum([1,1], self.uni), 3)

    def test_moore_neighbors_same(self):
        testing.assertEqual(moore_neighbors_same([1,1], self.uni), 3)
        testing.assertEqual(moore_neighbors_same([0,0], self.uni), 7)

    def test_neumann_neighbors_sum(self):
        testing.assertEqual(neumann_neighbors_sum([1,1], self.uni), 2)

    def test_neumann_neighbors_same(self):
        testing.assertEqual(neumann_neighbors_same([1,1], self.uni), 2)
        testing.assertEqual(neumann_neighbors_same([0,0], self.uni), 4)

class IsingTestCase(unittest.TestCase):

    def setUp(self):
        self.uni = make_universe(size=100, edge_ratio=1, init='random')

    def test_ising_process_off(self):
        self.uni.beta = 1/8
        self.uni.back = self.uni.data.copy()
        ising(0, self.uni)
        testing.assert_array_equal(self.uni.back, self.uni.data)


class ConwayTestCase(unittest.TestCase):

    def setUp(self):
        self.uni = make_universe(size=100, edge_ratio=1, init='none')

    def test_conway_wraps(self):
        self.uni.data[0:3,0:3] = 1
        conway(self.uni)

        arr2 = uni.back
        arr2[:,:] = 0
        arr2[0,0] = 1; arr2[2,0] = 1; arr2[2,2] = 1; arr2[0,2] = 1
        arr2[1,3:5] = 1; arr2[3:5, 1] = 1

        testing.assert_array_equal(arr2, self.uni.data)

    def test_conway_neumann_versus_old(self):
        uni = make_universe(size=100, edge_ratio=1, init='random')
        uni2 = uni
        testing.assert_array_equal(uni.data, uni2.data)

        conway(self.uni)
        testing.assert_equal(np.any(np.not_equal(uni.data, uni2.data)), True)
        conway_old(self.rule, tst_dimL(), arr2)
        testing.assert_array_equal(uni.data, uni2.data)

if __name__=="__main__":
    unittest.main(verbosity=2 if debug is True else 1)
