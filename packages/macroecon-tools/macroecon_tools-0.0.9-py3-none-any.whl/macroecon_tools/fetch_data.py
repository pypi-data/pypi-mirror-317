# Description: A set of fetch methods to get macroeconomic data

# Dependencies
from fredapi import Fred
import pandas as pd
from datetime import datetime

# Get current directory
import sys, os
CWD = os.path.dirname(os.path.dirname(__file__))
sys.path.append(CWD)

# Package imports
import timeseries as mt

def parse_year(year: str) -> datetime:
    '''
    Get year, month, day from %Y.%f
    '''
    year_int = int(year)
    month = int((year % 1) * 12) + 1
    day = int(((year % 1) * 12) % 1 * 30) + 1 
    return datetime(year_int, month, day)

def get_barnichon(filepath, panel, input_var, output_name):
    '''
    Get vacancy rate data from Barnichon.
    '''
    # read data from barnichon file
    data = pd.read_csv(filepath)
    data['year'] = data['year'].apply(parse_year)
    data.set_index('year', inplace=True)
    data = mt.Timeseries(data, name='Barnichon', source_freq='daily', data_source='Barnichon')
    data = data._update(data.ffill())

    match input_var: # construct data
        case 'V_LF':
            if 'JTSJOL' not in panel or 'CLF16OV' not in panel:
                raise ValueError('input panel must contain job openings (JTSJOL) and labor force (CLF16OV) to create Barnichon V_LF') 
            # Create vacancy rate with JOLTS data
            panel[output_name] = 100 * panel['V'] / panel['L']
            # Replace pre-2001 with Barnichon's vacancy rate
            panel.loc[:'2000-12-31', output_name] = data[:'2000-12-31'][input_var]
            # TODO: check that this is still a Timeseries
        case 'V_hwi':
            tr_all = (data.index[0], data.index[-1])
            panel[output_name] = pd.NA
            panel.loc[tr_all[0]: tr_all[1], output_name] = data[input_var]
        case _:
            raise ValueError(f'Unknown input_var: {input_var}')
        
    return panel


def get_fred(data_sources, data_names, date_one="1960-12-31", date_two="2023-12-31", api_key=None):
    '''
    Fetch data from the FRED API
    '''
    # Look for api key 
    if api_key is None: # Load API key
        try:
            with open(f'{os.path.dirname(__file__)}/fred_api_key.txt') as f:
                api_key = f.read().strip()
        except FileNotFoundError as e:
            try: 
                api_key = os.environ['FRED_API_KEY']
            except KeyError as e: # Raise exception if API key not found
                raise Exception('API key not found. TIP: export FRED_API_KEY="your_api_key_here"')
    
    # Create connection to fred 
    fred_connection = Fred(api_key=api_key)
            
    # Get data from FRED
    data = mt.Panel()
    for idx, data_src in enumerate(data_sources):
        raw_data = fred_connection.get_series(data_src, observation_start=date_one, observation_end=date_two)
        data_freq = fred_connection.get_series_info(data_src)['frequency']
        data_name = data_names[idx]
        data[data_name] = mt.Timeseries(raw_data, name=data_name, source_freq=data_freq, data_source="FRED") 
    
    # Save
    # if 'outmat' in F:
        # Save both the data and the index
        # with open(F['outmat'], 'wb') as f:
            # pickle.dump(dataraw, f)
        # print('Raw data saved:', F['outmat'])

    print('NOTE: data is automatically set to year end frequency and reindexed daily.')
    return data

if __name__ == '__main__':
    def test_fred():
        # test fetchfred
        data_sources = ['CPIAUCSL', 'GDPC1', 'UNRATE']
        data_names = ['CPI', 'GDP', 'UNEMP']
        data = get_fred(data_sources, data_names)
        print(data['CPI'])
        print(data['GDP'])
        print(data['UNEMP'])
    test_fred()