import unittest
import pytest
import sys

sys.path.append('src')
from pyudbf.UDBFFileReader import UDBFFileReader


class TestFileReader(unittest.TestCase):
    def test_simple_read(self):
        udbf_data = UDBFFileReader('./tests/example.udbf')
        self.assertEqual(udbf_data.n_points, 5999)
        self.assertEqual(udbf_data.runlength, 59.98)
        self.assertEqual(udbf_data.n_channels, 25)
