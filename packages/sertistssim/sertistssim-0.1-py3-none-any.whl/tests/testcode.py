import unittest
from sertistssim.sertistssim import (
    make_epoch,
    make_random_uniform_integer,
    make_df,
    make_time_series,
    make_time_series_uids,
)

class Tester(unittest.TestCase):
    def canItRun(self):
        flist = [
            make_epoch,
            make_random_uniform_integer,
            make_df,
            make_time_series,
            make_time_series_uids,
        ]
        for f in flist:
            with self.subTest(func=f):
                self.assertIsNone(func())

if __name__ == '__main__':
    unittest.main()
