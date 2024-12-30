import pandas as pd
import numpy as np
import random

'''
Functions to simulate time-series (ts) dataset:
 - make_epoch() to make an array of epochs
 - make_random_uniform_integer() to generate an array of integers randomly drawn from a uniform distribution
 - make_df()
 - make_time_series()
 - make_time_series_uids()
'''

def make_epoch(startdate = '1985-04-10', enddate = '1985-04-20', freq = 'D', dtype = 'datetime64[ns]'):
    return pd.date_range(start = startdate, end = enddate, freq = freq).to_numpy(dtype = dtype)

def make_random_uniform_integer(start = 0, end = 10, N = 4):
    return [random.randint(start, end) for _ in range(N)]

def make_df(unique_id = '123456', epoch_array = np.arange(10), demand_array = np.arange(10)):
    dictdf = {'unique_id': [unique_id for _ in range(len(epoch_array))], 'epoch': epoch_array, 'demand': demand_array}
    return pd.DataFrame(dictdf)

def make_time_series(unique_id = '123456', startdate = '1985-04-10', enddate = '1985-04-20', freq = 'D', dtype = 'datetime64[ns]', demand_lower_bound = 0, demand_upper_bound = 100):
    e = make_epoch(startdate, enddate, freq, dtype)
    d = make_random_uniform_integer(demand_lower_bound, demand_upper_bound, len(e))
    return make_df(unique_id, e, d)

def make_time_series_uids(unique_ids = ['123456', 'abc'], startdate = '1985-04-10', enddate = '1985-04-20', freq = 'D', dtype = 'datetime64[ns]', demand_lower_bound = 0, demand_upper_bound = 100):
    t = [pd.DataFrame(make_time_series(uid, startdate, enddate, freq, dtype, demand_lower_bound, demand_upper_bound)) for uid in unique_ids]
    return pd.concat(t[0:], ignore_index=True)