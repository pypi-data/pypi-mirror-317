import unittest
import pandas as pd
from sertistssim.sertistssim import (
    make_epoch,
    make_random_uniform_integer,
    make_df,
    make_time_series,
    make_time_series_uids,
    make_lag,
)

class Tester(unittest.TestCase):

    def _test_make_lag(self):
        epoch = make_epoch()
        value = make_random_uniform_integer(N = len(epoch))
        df = pd.DataFrame({'a': epoch, 'b': value})
        df = df.sort_values(by = 'a', ascending = False) # make it to decreasing order        
        df = make_lag(df, 'a', 'b', 1, 'int')
    
    def canItRun(self):
        flist = [
            make_epoch,
            make_random_uniform_integer,
            make_df,
            make_time_series,
            make_time_series_uids,
            make_lag,
        ]
        for f in flist:
            if f == make_lag:
                with self.subTest(func=_test_make_lag):
                    self.assertIsNone(func())
            else:
                with self.subTest(func=f):
                    self.assertIsNone(func())
                
if __name__ == '__main__':
    unittest.main()
