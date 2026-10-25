import unittest

from py_disjoint_interval_set import DisjointIntervalSet


class TestInsertAndMerge(unittest.TestCase):
    def test_empty_set(self):
        ds = DisjointIntervalSet()
        self.assertEqual(ds.intervals(), [])
        self.assertEqual(len(ds), 0)

    def test_single_insert(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertEqual(ds.intervals(), [(1, 5)])
        self.assertEqual(len(ds), 1)

    def test_insert_empty_range_is_noop(self):
        ds = DisjointIntervalSet()
        ds.insert(3, 3)
        self.assertEqual(ds.intervals(), [])

    def test_insert_start_greater_than_end_raises(self):
        ds = DisjointIntervalSet()
        with self.assertRaises(ValueError):
            ds.insert(5, 1)

    def test_insert_adjacent_merges(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        ds.insert(5, 10)
        self.assertEqual(ds.intervals(), [(1, 10)])

    def test_insert_overlapping_merges(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 10)
        ds.insert(5, 15)
        self.assertEqual(ds.intervals(), [(1, 15)])

    def test_insert_bridge_across_gap(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        ds.insert(10, 20)
        ds.insert(4, 12)
        self.assertEqual(ds.intervals(), [(1, 20)])

    def test_insert_inside_existing_is_absorbed(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 20)
        ds.insert(5, 10)
        self.assertEqual(ds.intervals(), [(1, 20)])

    def test_insert_before_all(self):
        ds = DisjointIntervalSet()
        ds.insert(10, 20)
        ds.insert(1, 5)
        self.assertEqual(ds.intervals(), [(1, 5), (10, 20)])

    def test_insert_after_all(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        ds.insert(10, 20)
        self.assertEqual(ds.intervals(), [(1, 5), (10, 20)])


class TestDelete(unittest.TestCase):
    def test_delete_middle_splits(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 20)
        ds.delete(8, 12)
        self.assertEqual(ds.intervals(), [(1, 8), (12, 20)])

    def test_delete_exact_match_removes(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        ds.delete(1, 5)
        self.assertEqual(ds.intervals(), [])

    def test_delete_no_overlap_unchanged(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        ds.delete(10, 20)
        self.assertEqual(ds.intervals(), [(1, 5)])

    def test_delete_left_edge(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 10)
        ds.delete(1, 4)
        self.assertEqual(ds.intervals(), [(4, 10)])

    def test_delete_right_edge(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 10)
        ds.delete(7, 10)
        self.assertEqual(ds.intervals(), [(1, 7)])

    def test_delete_across_multiple(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        ds.insert(10, 20)
        ds.delete(3, 15)
        self.assertEqual(ds.intervals(), [(1, 3), (15, 20)])

    def test_delete_empty_range_is_noop(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 10)
        ds.delete(5, 5)
        self.assertEqual(ds.intervals(), [(1, 10)])

    def test_delete_start_greater_than_end_raises(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 10)
        with self.assertRaises(ValueError):
            ds.delete(8, 4)


class TestOverlaps(unittest.TestCase):
    def test_overlaps_true(self):
        ds = DisjointIntervalSet()
        ds.insert(10, 20)
        self.assertTrue(ds.overlaps(15, 25))

    def test_overlaps_false_disjoint(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertFalse(ds.overlaps(5, 10))

    def test_overlaps_false_far_apart(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertFalse(ds.overlaps(100, 200))

    def test_overlaps_empty_range_false(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertFalse(ds.overlaps(3, 3))

    def test_overlaps_start_greater_than_end_raises(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        with self.assertRaises(ValueError):
            ds.overlaps(5, 1)

    def test_overlaps_point_contact_closed_side_true(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        # [4, 5) overlaps [1, 5) because 4 < 5 and 1 < 5
        self.assertTrue(ds.overlaps(4, 5))


class TestContains(unittest.TestCase):
    def test_contains_inside(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertIn(3, ds)

    def test_contains_at_start_inclusive(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertIn(1, ds)

    def test_contains_at_end_exclusive(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertNotIn(5, ds)

    def test_contains_outside(self):
        ds = DisjointIntervalSet()
        ds.insert(1, 5)
        self.assertNotIn(10, ds)

    def test_contains_empty_set(self):
        ds = DisjointIntervalSet()
        self.assertNotIn(0, ds)


class TestComplexSequence(unittest.TestCase):
    def test_realistic_sequence(self):
        ds = DisjointIntervalSet()
        ds.insert(0, 10)
        ds.insert(20, 30)
        ds.insert(5, 25)
        self.assertEqual(ds.intervals(), [(0, 30)])
        ds.delete(10, 20)
        self.assertEqual(ds.intervals(), [(0, 10), (20, 30)])
        self.assertTrue(ds.overlaps(9, 11))
        self.assertFalse(ds.overlaps(10, 20))
        ds.insert(8, 22)
        self.assertEqual(ds.intervals(), [(0, 30)])


if __name__ == "__main__":
    unittest.main()
