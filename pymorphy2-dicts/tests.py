# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
import os

class TestInstall(unittest.TestCase):

    def test_dict_exists(self):
        import pymorphy2_dicts
        path = pymorphy2_dicts.get_path()

        # path exists
        self.assertTrue(os.path.isdir(path))

        # and has some files
        self.assertTrue(os.listdir(path))


if __name__ == '__main__':
    unittest.main()