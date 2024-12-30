# import libraries
import unittest
import pandas as pd
from pandas.testing import assert_series_equal

# get Timeseries class
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..', 'src', 'macroecon_tools'))
from timeseries import Timeseries, Panel

# get fetch data
import fetch_data as fd

class TestTimeseries(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.sample_data = pd.Series([i for i in range(24)], index=pd.date_range("2020-01-01", periods=24, freq="ME"))
        self.ts = Timeseries(self.sample_data, name="Sample", freq="monthly")

    def test_copy(self):
        ts_copy = self.ts.copy()
        # Assert that the copied instance is not the same as the original
        self.assertIsNot(ts_copy, self.ts)
        # Assert that the data and attributes of the copied instance are equal to the original
        self.assertTrue(ts_copy.equals(self.ts))
        self.assertEqual(ts_copy.name, self.ts.name)
        self.assertEqual(ts_copy.get_freqstr(), self.ts.get_freqstr())
        self.assertEqual(ts_copy.transformations, self.ts.transformations)

def test_print():
    sample_data = pd.Series([1, 2, 3, 4], index=pd.date_range("2020-01-01", periods=4, freq="ME"))
    ts = Timeseries(sample_data, name="Sample", source_freq="monthly")
    print(ts)
    large_sample_data = pd.Series([i for i in range(24)], index=pd.date_range("2020-01-01", periods=24, freq="ME"))
    ts = Timeseries(large_sample_data, name="Sample", source_freq="monthly")
    print(ts)

def test_agg():
    index = pd.date_range(start="2020-01-01", periods=36, freq="ME")
    data = Timeseries(pd.Series([i for i in range(36)], index=index), name="test")
    # print(data)
    data = data.agg('yearly', 'mean')
    print(f"{data}")

def test_pd_agg():
    index = pd.date_range(start="2020-01-01", periods=36, freq="ME")
    data = pd.Series([i for i in range(36)], index=index)
    data = data.resample('Y').mean()
    print(data)

def test_weekly():
    index = pd.date_range(start="2020-01-01", periods=36, freq="W")
    data = pd.Series([i for i in range(36)], index=index)
    print(Timeseries(data, name='test').agg('weekly', 'mean'))

def test_getdata():
    # Test get_fred
    data_sources = ['GDPC1', 'CPIAUCSL']
    data_names = ['GDP', 'CPI']
    data = fd.get_fred(data_sources, data_names)
    print(data)
    data.save(f'{script_dir}/test_data')

def test_load_data():
    # Load data
    data = Panel().load(f'{script_dir}/test_data')
    print(f"{data}")

def test_dropna():
    index = pd.date_range(start="2020-01-01", periods=36, freq="ME")
    data = Timeseries(pd.Series([i for i in range(36)], index=index), name='test')
    data = data.dropna()
    print(data)

def test_panel():
    index = pd.date_range(start="2020-01-01", periods=36, freq="ME")
    data = Timeseries(pd.Series([i for i in range(36)], index=index), name='test').agg('monthly', 'mean')
    panel = Panel()
    panel['test'] = data
    print(panel)

def test_pane_multi():
    PERIODS=12
    idx_one = pd.date_range(start="2010-01-01", periods=PERIODS, freq="ME")
    data_one = Timeseries(pd.Series([i for i in range(PERIODS)], index=idx_one), name='test_one').agg('monthly', 'mean')
    idx_two = pd.date_range(start="2010-01-01", periods=PERIODS, freq="ME")
    data_two = Timeseries(pd.Series([i*i for i in range(PERIODS)], index=idx_two), name='test_two').agg('monthly', 'mean')
    panel = Panel({
        'test_one': data_one,
        'test_two': data_two
    })
    idx_three = pd.date_range(start="2010-01-01", periods=PERIODS, freq="W-SUN")
    for idx in range(3):
        panel[f"test_{idx}"] = Timeseries(pd.Series([i*i*i for i in range(PERIODS)], index=idx_three), name=f'test_{idx}').agg('weekly', 'mean')
    print(f"{panel}")
    print(f"{panel.corr()}")

if __name__ == '__main__':
    # test_agg()
    # test_pd_agg()
    # test_print()
    # unittest.main()
    # test_load_data()
    # test_load_data()
    # test_weekly()
    # test_dropna()
    # test_getdata()
    # test_panel()
    test_pane_multi()