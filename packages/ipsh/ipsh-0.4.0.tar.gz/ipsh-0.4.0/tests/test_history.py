# -*- coding: utf-8 -*-

"""
test the ipsh.history module
"""

from unittest import TestCase

from ipsh import history


class History(TestCase):
    """Test the History class"""

    def test_position(self) -> None:
        """Test the position property"""
        hist_obj = history.History()
        with self.subTest("initial"):
            self.assertEqual(hist_obj.position, 1)
        #
        hist_obj.add("abc")
        hist_obj.add("defg")
        with self.subTest("after adding 2 elements"):
            self.assertEqual(hist_obj.position, 3)
        #
        with self.subTest("getting relative entry"):
            self.assertEqual(hist_obj.get_relative(-1), "defg")
        #
        with self.subTest("after getting relative entry"):
            self.assertEqual(hist_obj.position, 2)
        #

    def test_len(self) -> None:
        """Test the len(history_instance) capability"""
        hist_obj = history.History()
        with self.subTest("initial"):
            self.assertEqual(len(hist_obj), 1)
        #
        hist_obj.add("abc")
        hist_obj.add("defg")
        with self.subTest("after adding 2 elements"):
            self.assertEqual(len(hist_obj), 3)
        #

    def test_getitem(self) -> None:
        """Test the history_instance[n] capability"""
        hist_obj = history.History()
        hist_obj.add("abc")
        hist_obj.add("defg")
        for idx, expected_value in ((1, "abc"), (2, "defg")):
            with self.subTest("get item", idx=idx):
                self.assertEqual(hist_obj[idx], expected_value)
            #
        #
        with self.subTest("max"):
            self.assertEqual(hist_obj[3], "")
        #
        for idx in (0, 4, -1):
            with self.subTest("get item", idx=idx):
                self.assertRaisesRegex(
                    history.HistoryError, "^Not available$", hist_obj.__getitem__, idx
                )
            #
        #

    def test_iter_range(self) -> None:
        """Test the history_instance.iter_range() method"""
        hist_obj = history.History()
        hist_obj.add("abc")
        hist_obj.add("defg")
        with self.subTest("defaults"):
            self.assertEqual(list(hist_obj.iter_range()), [(1, "abc"), (2, "defg")])
        #
        with self.subTest("last element only"):
            self.assertEqual(list(hist_obj.iter_range(start=-1)), [(2, "defg")])
        #
        with self.subTest("first element only, ignoring errors"):
            self.assertEqual(list(hist_obj.iter_range(start=0, end=1)), [(1, "abc")])
        #
