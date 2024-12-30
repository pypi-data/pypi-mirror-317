# Description: A class used to represent a timeseries object.

# Import libraries
import pandas as pd
import numpy as np
from scipy.signal import detrend
from datetime import datetime
from dateutil.relativedelta import relativedelta
import quantecon as qe
import pickle

# Add path to constants
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import constants
from constants import Constants

class Timeseries(pd.Series):
    """
    A class used to represent a timeseries object.

    Attributes
    ----------
    data : pd.Series
        a single variable in a time table
    is_copy : bool
        a flag to indicate if the data is a copy (avoid reindexing to daily)
    name : str
        the name of the variable
    source_freq : str (optional)
        the frequency of the data source of the variable
    data_source : str (optional)
        the source of the data
    transformations : list[str]
        a list of transformations applied to the data

    Methods
    -------
    trans(form, lags=None)
        Transforms the data using the specified form (e.g., 'logdiff', 'diff', 'log', '100log').
        Must provide number of lags for 'logdiff' and 'diff'.
    agg(timestep, method)
        Aggregates the data using the specified method (e.g., 'quarterly', 'monthly', 'yearly').
        Must provide method (e.g., lastvalue, mean, sum).
    filter(method, date_one, date_two, p=None, h=None)
        Filters the data using the specified method (e.g., 'linear' or 'hamilton').
        Must provide start date (date_one) and end date (date_two).
        For 'hamilton', must also provide lag length (p) and lead length (h).
    """
    _metadata = ['name', 'source_freq', 'data_source', 'transformations']

    def __init__(self, data, is_copy = False, name: str = None, source_freq: str = "unknown", data_source : str = "unknown", transformations: list[str] = [], *args, **kwargs):
        """
        Initializes a Timeseries object.

        Parameters
        ----------
        data : pd.Series or array-like
            A single variable in a time table.
        is_copy : bool, optional
            If True, the data is treated as a copy and not reindexed to daily frequency. Default is False.
        name : str, optional
            The name of the variable. Default is None.
        source_freq : str, optional
            The frequency of the source data (e.g., 'quarterly', 'monthly', 'yearly'). Default is "unknown".
        data_source : str, optional
            The source of the data. Default is "unknown".
        transformations : list of str, optional
            A list of transformations applied to the data. Default is an empty list.
        *args : 
            Additional positional arguments passed to the pd.Series constructor.
        **kwargs : 
            Additional keyword arguments passed to the pd.Series constructor.

        Raises
        ------
        ValueError
            If the index is not a datetime index.
        ValueError
            If the variable name is not provided.
        ValueError
            If the frequency is not provided.

        Notes
        -----
        - The data is converted to float64 type.
        - If `is_copy` is False, the data is reindexed to daily frequency and 'reindex_daily' is added to transformations.
        - The index is converted to a datetime index and its frequency is inferred.
        """
        # convert data to float64
        data = pd.Series(data).astype('float64')
        # reindex the data to daily if not a copy
        if not is_copy:
            data = data.asfreq('D')
        # Call pd.Series constructor
        super().__init__(data, *args, **kwargs)

        # Metadata
        self.transformations = [val for val in transformations]
        if not is_copy:
            self.transformations.append('reindex_daily')
        self.source_freq = source_freq
        self.data_source = data_source

        # Ensure the index is a datetime index
        try:
            self.index = pd.to_datetime(self.index)
            # infer the frequency
            self.index.freq = pd.infer_freq(self.index)
        except:
            raise ValueError('Timeseries Class: Index must be a datetime index')
        
        # Check if need to rename
        if name:
            self.name = name
        if not self.name:
            raise ValueError('Timeseries Class: Variable name not provided')

        # Check for frequency
        if not self.index.freq or not self.index.freqstr:
            raise ValueError('Timeseries Class: Frequency not provided')

    # copy constructor
    def _update(self, data: pd.Series, transformation: str = None):
        """
        Updates the current Timeseries object with new data.

        Parameters
        ----------
        data : pd.Series
            The new data to update the Timeseries object with.
        transformation : str, optional
            A transformation applied to the new data. If provided, it is added to the list of transformations.

        Returns
        -------
        Timeseries
            A new Timeseries object with the updated data and transformations.
        """
        if transformation:
            self.transformations.append(transformation)
        return Timeseries(data, is_copy=True, name=self.name, source_freq=self.source_freq, data_source=self.data_source, transformations=self.transformations)

    def __finalize__(self, other, method=None, **kwargs):
        """
        Propagate metadata from another Timeseries object to the current instance.

        Parameters
        ----------
        other : Timeseries
            The Timeseries object from which to propagate metadata.
        method : str, optional
            The method used for propagation. Default is None.
        **kwargs : 
            Additional keyword arguments.

        Returns
        -------
        self : Timeseries
            The Timeseries object with propagated metadata.
        """
        if isinstance(other, Timeseries):
            self.name = getattr(other, 'name', None)
            self.source_freq = getattr(other, 'source_freq', None)
            self.data_source = getattr(other, 'data_source', None)
            self.transformations = getattr(other, 'transformations', [])
        return self
    
    # getters
    def get_freqstr(self):
        """
        Returns the frequency of the timeseries.

        Returns
        -------
        str
            The frequency of the timeseries.
        """
        return self.index.freqstr
    
    # override string representation
    def __repr__(self):
        """
        Returns a string representation of the Timeseries object.

        Returns
        -------
        str
            A string representation of the Timeseries object.
        """
        # create data display
        data = ""
        if len(self) == 0:
            data = "Empty Timeseries\n"
        elif len(self) <= 10:
            for i in range(len(self)):
                data += f"{self.index[i].strftime('%Y-%m-%d')}    {self.iloc[i]}\n"
        else:
            n = 5
            # get the first 5 rows without the header
            for i in range(n):
                data += f"{self.index[i].strftime('%Y-%m-%d')}    {self.iloc[i]}\n"
            data += f"\t...\n"
            # get the last 5 rows
            for i in range(len(self) - n, len(self)):
                data += f"{self.index[i].strftime('%Y-%m-%d')}    {self.iloc[i]}\n"

        # build metadata
        metadata = f"Name: {self.name}, Freq: {self.get_freqstr()}"
        if self.source_freq:
            metadata += f", Source Freq: {self.source_freq}"
        if self.data_source:
            metadata += f", Data Source: {self.data_source}"
        metadata += "\n"
        
        # return string
        return (f"{data}"
                f"...\n"
                f"{metadata}"
                f"Transformations: {self.transformations}\n")  

    # save and load
    def save(self, file_path: str):
        '''
        Saves the timeseries to a file.

        Parameters
        ----------
        file_path : str
            The file path to save the timeseries to.
        '''
        # check if file path has pkl extension
        if 'pkl' not in file_path:
            if '.' in file_path:
                file_path = file_path.split('.')[0] + '.pkl'
            else:
                file_path += '.pkl'
        # save the timeseries to a file
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    def load(self, file_path):
        '''
        Loads the timeseries from a file.

        Parameters
        ----------
        file_path : str
            The file path to load the timeseries from.
        '''
        # check if file path has pkl extension
        if 'pkl' not in file_path:
            if '.' in file_path:
                file_path = file_path.split('.')[0] + '.pkl'
            else:
                file_path += '.pkl'
        # load the timeseries from a file
        with open(file_path, 'rb') as f:
            self = pickle.load(f) 
        return self
 
    # Transform data
    def logdiff(self, nlag: int, freq: str = None):
        """
        Transforms the data using the log difference method.

        Parameters
        ----------
        nlag : int
            The lag length for the transformation.
        freq : str, optional
            Frequency of original data. Default is None.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        trans_freq = self.get_freqstr() if not freq else freq
        annpp = Constants.ANNSCALE_MAP[trans_freq] / nlag
        return self._update(annpp * np.log(self / self.shift(nlag)), f'logdiff_{nlag}_{trans_freq}')
    
    def diff(self, nlag: int):
        """
        Transforms the data using the difference method.

        Parameters
        ----------
        nlag : int
            The lag length for the transformation.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        return self._update(self - self.shift(nlag), f'diff_{nlag}')
    
    def log(self):
        """
        Transforms the data using the log method.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        return self._update(np.log(self), 'log')
    
    def log100(self):
        """
        Transforms the data using the 100 times log method.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        return self._update(100 * np.log(self), 'log100')
    
    # Aggregation
    def agg(self, timestep: str, method: str):
        """
        Aggregates the data using the specified method.

        Parameters
        ----------
        timestep : str
            The timestep to aggregate the data (e.g., 'quarterly', 'monthly', 'yearly').
        method : str
            The aggregation method to use (e.g., 'lastvalue', 'mean', 'sum').

        Returns
        -------
        Timeseries
            A new Timeseries object with the aggregated data.
        """
        # Perform aggregation using super().resample and the specified aggregation method
        aggregated = pd.Series(getattr(super().resample(Constants.freq_map[timestep]), Constants.agg_map[method])()).dropna()
        # Update the current Timeseries object with the aggregated data
        if aggregated.index.freq is None:
            aggregated = aggregated.asfreq(Constants.freq_map[timestep])
        # aggregated.index.freq = Constants.freq_map[timestep]
        return self._update(aggregated, f'agg_{timestep}_{method}')

    # Trunctate
    def trunc(self, date_one: str, date_two: str):
        """
        Truncates the data between the specified dates.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.

        Returns
        -------
        Timeseries
            A new Timeseries object with the truncated data.
        """
        # update self data
        return self._update(self[date_one: date_two], f'trunc_{date_one}_{date_two}')
    
    # Dropna
    def dropna(self):
        """
        Drops missing values from the data.

        Returns
        -------
        Timeseries
            A new Timeseries object with the missing values dropped.
        """
        return self._update(super().dropna(), 'dropna')

    # filters
    def linear_filter(self, date_one: str, date_two: str):
        """
        Filters the data using the linear method.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.

        Returns
        -------
        Timeseries
            A new Timeseries object with the filtered data.
        """
        date_one = datetime.strptime(date_one, '%d-%b-%Y')
        date_two = datetime.strptime(date_two, '%d-%b-%Y')

        # Time range
        self = self.trunc(date_one, date_two)
        return self._update(detrend(self, axis=0, type='linear'), f'linear_filter_{date_one}_{date_two}')
    
    def hamilton_filter(self, date_one: str, date_two: str, lag_len: int = None, lead_len: int = None):
        """
        Filters the data using the Hamilton method.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.
        lagLength : int, optional
            The lag length for the 'hamilton' filter. Default is None.
        leadLength : int, optional
            The lead length for the 'hamilton' filter. Default is None.

        Returns
        -------
        Timeseries
            A new Timeseries object with the filtered data.

        Raises
        ------
        ValueError
            If the frequency is not supported for the 'hamilton' filter.
        """
        date_one = datetime.strptime(date_one, '%d-%b-%Y')
        date_two = datetime.strptime(date_two, '%d-%b-%Y')

        # get default lag and lead lengths
        if self.get_freqstr() in Constants.year_like:
            lag_len = 1
            lead_len = 2
        elif self.get_freqstr() in Constants.quarter_like:
            lag_len = 4
            lead_len = 8
        elif self.get_freqstr() == Constants.month_like:
            lag_len = 12
            lead_len = 24
        else:
            raise ValueError(f'{self.get_freqstr()} frequency not supported for Hamilton filter')
        
        # get the tstart 
        if self.get_freqstr() in Constants.year_like:
            tstart = date_one - relativedelta(years=(lag_len + lead_len - 1))
        elif self.get_freqstr() in Constants.quarter_like:
            tstart = date_one - relativedelta(months=3*(lag_len + lead_len - 1))
        elif self.get_freqstr() in Constants.month_like:
            tstart = date_one - relativedelta(months=(lag_len + lead_len - 1))
        trham = self.trunc(tstart, date_two)
        # Get cyclical component 
        cycle, trend = qe._filter.hamilton_filter(trham, lead_len, lag_len)
        cycle_series = pd.Series(cycle.flatten(), index=trham.index).dropna()
        return self._update(cycle_series, f'hamilton_filter_{date_one}_{date_two}_{lag_len}_{lead_len}')

class Panel(dict):
    """
    A custom Panel that maintains a pd.DataFrame and a dictionary with Timeseries objects.
    """

    def __init__(self, data: dict = {},*args, **kwargs):
        """
        Initializes the Panel. Ensures columns are Timeseries instances.

        Parameters
        ----------
        data : dict, optional
            A dictionary where keys are column names and values are Timeseries instances. Default is an empty dictionary.
        """
        super().__init__(data, *args, **kwargs)
        for key in self:
            print(f"{key} {self[key]}")

    # Build DataFrame
    @property
    def df(self):
        """
        Returns the Panel as a DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame representation of the Panel.
        """
        # Reindex all columns to daily frequency
        return pd.concat({key: val.asfreq('D') for key, val in self.items()}, axis=1)

    def __repr__(self):
        """
        Returns a string representation of the Panel object.
        """
        return f"{self.df.dropna(how='all')}"

    # truncate method
    def trunc(self, date_one: str, date_two: str):
        """
        Truncates the data between the specified dates.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.

        Returns
        -------
        Panel
            A new Panel object with the truncated data.
        """
        # update self data
        return Panel({key: val.trunc(date_one, date_two) for key, val in self.items()})

    # dropna method
    def dropna(self):
        """
        Drops missing values from the data.

        Returns
        -------
        Panel
            A new Panel object with the missing values dropped.
        """
        return Panel({key: val.dropna() for key, val in self.items()})
    
    # correlation
    def corr(self):
        """
        Returns the correlation matrix of the data.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the correlation matrix.
        """
        return self.df.corr()
    
    # save and load
    def save(self, file_path):
        '''
        Saves the panel to a file.

        Parameters
        ----------
        file_path : str
            The file path to save the panel to.
        '''
        # check if file path has pkl extension
        if 'pkl' not in file_path:
            if '.' in file_path:
                file_path = file_path.split('.')[0] + '.pkl'
            else:
                file_path += '.pkl'
        # save the panel to a file
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    def load(self, file_path):
        '''
        Loads the panel from a file.

        Parameters
        ----------
        file_path : str
            The file path to load the panel from.
        '''
        # check if file path has pkl extension
        if 'pkl' not in file_path:
            if '.' in file_path:
                file_path = file_path.split('.')[0] + '.pkl'
            else:
                file_path += '.pkl'
        # load the panel from a file
        with open(file_path, 'rb') as f:
            self = pickle.load(f)
        return self
    