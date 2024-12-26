import unittest
from pattern_sort.sort import Sort

class TestSort(unittest.TestCase):
    def setUp(self):
        self.sort = Sort()

    def test_bubble_sort(self):
        self.assertEqual(self.sort.bubble_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.bubble_sort([]), [])
        self.assertEqual(self.sort.bubble_sort([1]), [1])

    def test_selection_sort(self):
        self.assertEqual(self.sort.selection_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.selection_sort([]), [])
        self.assertEqual(self.sort.selection_sort([1]), [1])

    def test_insertion_sort(self):
        self.assertEqual(self.sort.insertion_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.insertion_sort([]), [])
        self.assertEqual(self.sort.insertion_sort([1]), [1])

    def test_merge_sort(self):
        self.assertEqual(self.sort.merge_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.merge_sort([]), [])
        self.assertEqual(self.sort.merge_sort([1]), [1])

    def test_quick_sort(self):
        self.assertEqual(self.sort.quick_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.quick_sort([]), [])
        self.assertEqual(self.sort.quick_sort([1]), [1])

    def test_heap_sort(self):
        self.assertEqual(self.sort.heap_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.heap_sort([]), [])
        self.assertEqual(self.sort.heap_sort([1]), [1])

    def test_shell_sort(self):
        self.assertEqual(self.sort.shell_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.shell_sort([]), [])
        self.assertEqual(self.sort.shell_sort([1]), [1])

    def test_counting_sort(self):
        self.assertEqual(self.sort.counting_sort([3, 2, 1]), [1, 2, 3])
        self.assertEqual(self.sort.counting_sort([]), [])
        self.assertEqual(self.sort.counting_sort([1]), [1])

    def test_radix_sort(self):
        self.assertEqual(self.sort.radix_sort([170, 45, 75, 90, 802, 24, 2, 66]), [2, 24, 45, 66, 75, 90, 170, 802])

    def test_bucket_sort(self):
        self.assertEqual(self.sort.bucket_sort([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]),
                         [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94])

if __name__ == "__main__":
    unittest.main()
