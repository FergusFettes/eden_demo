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
    make_universe, neighbor_coords, neighbor_truth, eden,
)

debug = True


class NeighborTestCase(unittest.TestCase):

    def setUp(self):
        self.uni = make_universe(size=10, edge_ratio=1, init='none')
        self.uni.data[1:3, 1:3] = 1
        self.uni.back = self.uni.data

    def test_moore_neighbors_sum(self):
        self.assertEqual(moore_neighbors_sum([1,1], self.uni), 3)

    def test_moore_neighbors_same(self):
        self.assertEqual(moore_neighbors_same([1,1], self.uni), 3)
        self.assertEqual(moore_neighbors_same([0,0], self.uni), 7)

    def test_neumann_neighbors_sum(self):
        self.assertEqual(neumann_neighbors_sum([1,1], self.uni), 2)

    def test_neumann_neighbors_same(self):
        self.assertEqual(neumann_neighbors_same([1,1], self.uni), 2)
        self.assertEqual(neumann_neighbors_same([0,0], self.uni), 4)

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
        uni = make_universe(size=5, edge_ratio=1, init='none')
        uni.data[0:3,0:3] = 1
        arr2 = uni.back.copy()
        conway(uni)

        arr2[:,:] = 0
        arr2[0,0] = 1; arr2[2,0] = 1; arr2[2,2] = 1; arr2[0,2] = 1
        arr2[1,3:5] = 1; arr2[3:5, 1] = 1

        testing.assert_array_equal(arr2, uni.data)

    def test_conway_neumann_versus_old(self):
        uni = make_universe(size=100, edge_ratio=1, init='random')
        uni2 = make_universe(size=100, edge_ratio=1, init='random')
        uni2.data = uni.data.copy()
        uni2.back = uni2.data.copy()
        testing.assert_array_equal(uni.data, uni2.data)

        conway(uni)
        testing.assert_equal(np.any(np.not_equal(uni.data, uni2.data)), True)
        conway_old(uni2)
        testing.assert_array_equal(uni.data, uni2.data)

class EdenTestCase(unittest.TestCase):

    def setUp(self):
        self.uni = make_universe(size=100, edge_ratio=1, init='none')
        self.uni.data[1:4,1:4] = 1
        self.uni.back = self.uni.data.copy()

    def test_neighbor_coords(self):
        coords = neighbor_coords([1,1], self.uni)
        target = [[2, 1], [1, 2], [1, 0], [0, 1]]
        testing.assert_array_equal(coords, target)

    def test_neighbor_truth(self):
        coords = neighbor_truth([1,1], self.uni)
        target = [True, True, False, False]
        testing.assert_array_equal(coords, target)

    def test_choose_neumann_neighbor_two_and_two(self):
        neighbors = []
        for i in range(100):
            neighbors.append(tuple(choose_neumann_neighbor([1,1], self.uni)))
        self.assertEqual(len(set(neighbors)), 2)

    def test_eden_has_space_popped(self):
        self.uni.has_space = [np.asarray([1, 2])]
        eden(self.uni)
        testing.assert_array_equal(self.uni.has_space, [np.asarray([0, 2])])


if __name__=="__main__":
    unittest.main(verbosity=2 if debug is True else 1)
