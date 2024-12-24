import numpy as np
import pandas as pd

from typing import List, Dict, Tuple, Optional


class DataClass:
    """
    A class to handle financial data efficiently with caching and query functionality.

    This class is designed to load, filter, and process financial data for backtesting.
    It supports caching for optimized performance and provides methods to calculate
    and retrieve data fields such as price returns, stock IDs, and date ranges.

    Attributes
    ----------
    data_paths : dict
        Dictionary containing the paths to various data files (e.g., daily data).
    cache : dict
        Cached dataframes for faster access.
    daily_data : pd.DataFrame or None
        Processed daily data with calculated returns, if available.
    AStocks : list of str
        List of all available stock IDs.
    DateRange : tuple of int
        The full date range covered by the data in YYYYMMDD format.

    Examples
    --------
    Initialize a `DataClass` instance and generate a cache for a specific stock and date range:
    
    >>> data_paths = {
    ...     "daily": "path_to_daily_data.feather",
    ...     "balance": "path_to_balance_sheet_data.feather",
    ... }
    >>> data = DataClass(data_paths)
    >>> data.generate_cache(stk_id=["000001.SZ"], date_range=(20200101, 20201231))
    >>> print(data.AStocks)
    ['000001.SZ']
    >>> print(data.DateRange)
    (20200101, 20201231)
    """

    def __init__(self, data_paths: Dict[str, str]):
        """ 
        Initialize the DataClass with paths to data files.

        Parameters
        ----------
        data_paths : dict
            A dictionary where keys represent data types (e.g., 'daily') 
            and values are the paths to the corresponding files.
        """
        self.data_paths: Dict[str, str] = {
            key: value for key, value in data_paths.items() if key != "item_map"
        }
        self.cache: Dict[str, pd.DataFrame] = {}
        self.daily_data: Optional[pd.DataFrame] = None
        self.AStocks: List[str] = []  # All stock IDs
        self.DateRange: Tuple[int, int] = (20200101, 20231231)  # Full date range

    def _load_data(self, data_type: str) -> pd.DataFrame:
        ''' 
        Load data from file based on the given data type.

        Parameters
        - data_type (str): The type of data to load (e.g., 'daily', 'annotation').

        Returns
        - pd.DataFrame: Loaded data.
        '''
        if data_type not in self.cache:
            print(f"Loading data: {data_type}")
            self.cache[data_type] = pd.read_feather(self.data_paths[data_type])
            # Ensure column names are lowercase
            self.cache[data_type].columns = self.cache[data_type].columns.str.lower()
            # Ensure the 'date' column is in datetime format
            if 'date' in self.cache[data_type].columns:
                self.cache[data_type]['date'] = pd.to_datetime(self.cache[data_type]['date'])
        return self.cache[data_type]

    def _update_astocks_and_daterange(self) -> None:
        '''
        Update AStocks (all stock IDs) and DateRange (full date range) based on cached data.

        Returns
        - None
        '''
        all_stk_ids = set()
        min_date, max_date = None, None

        for data_type, data in self.cache.items():
            if 'stk_id' in data.columns:
                all_stk_ids.update(data['stk_id'].unique())
            if 'date' in data.columns:
                data_min_date = data['date'].min()
                data_max_date = data['date'].max()
                min_date = data_min_date if min_date is None else min(min_date, data_min_date)
                max_date = data_max_date if max_date is None else max(max_date, data_max_date)

        self.AStocks = sorted(all_stk_ids)
        if min_date is not None and max_date is not None:
            self.DateRange = (int(min_date.strftime('%Y%m%d')), int(max_date.strftime('%Y%m%d')))

    def _calculate_returns(self, daily_data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate various types of returns based on available price fields.

        The following returns are calculated:
        - return: Log return of close prices.
        - open_return: Log return of open prices.
        - high_return: Log return of high prices.
        - low_return: Log return of low prices.
        - open_close_return: Log return between open and close prices for the same day.
        - high_low_return: Log return between high and low prices for the same day.
        """
        daily_data = daily_data.copy()
        
        # Calculate returns
        daily_data['close_return'] = np.log(daily_data['close'] / daily_data['close'].shift(1))
        daily_data['open_return'] = np.log(daily_data['open'] / daily_data['open'].shift(1))
        daily_data['high_return'] = np.log(daily_data['high'] / daily_data['high'].shift(1))
        daily_data['low_return'] = np.log(daily_data['low'] / daily_data['low'].shift(1))
        daily_data['open_close_return'] = np.log(daily_data['close'] / daily_data['open'])
        daily_data['high_low_return'] = np.log(daily_data['high'] / daily_data['low'])
        
        return daily_data

    @staticmethod
    def _log_return(series: pd.Series) -> pd.Series:
        """
        Compute log return for a single series.

        Parameters
        ----------
        series : pd.Series
            A pandas Series containing price data.

        Returns
        -------
        pd.Series
            Log returns as a pandas Series.
        """
        return (series / series.shift(1)).apply(lambda x: pd.np.log(x) if x > 0 else pd.np.nan).fillna(0)

    @staticmethod
    def _log_cross_return(series1: pd.Series, series2: pd.Series) -> pd.Series:
        """
        Compute log return between two price series.

        Parameters
        ----------
        series1 : pd.Series
            The numerator series (e.g., close prices).
        series2 : pd.Series
            The denominator series (e.g., open prices).

        Returns
        -------
        pd.Series
            Log returns as a pandas Series.
        """
        return (series1 / series2).apply(lambda x: pd.np.log(x) if x > 0 else pd.np.nan).fillna(0)

    def generate_cache(self, stk_id: Optional[List[str]] = None, date_range: Optional[Tuple[int, int]] = None) -> None:
        """
        Generate cache for specific stock IDs and date ranges, including calculated returns.

        This method filters the raw data based on the specified stock IDs and date range,
        caches the filtered data, and calculates several types of returns (logarithmic) 
        for the 'daily' data, making these fields available for downstream operations.

        Parameters
        ----------
        stk_id : list of str, optional
            A list of stock IDs to filter, e.g., ["000001.SZ", "000002.SZ"]. 
            If None, all available stock IDs will be included.
        date_range : tuple of int, optional
            A tuple specifying the start and end dates in YYYYMMDD format, 
            e.g., (20200101, 20210101). If None, the full date range will be included.

        Returns
        -------
        None
            Updates the class cache with filtered data and populates the `daily_data` 
            attribute for alignment. Adds return fields such as 'return', 
            'open_return', 'high_return', 'low_return', 'open_close_return', 
            and 'high_low_return' to the `daily_data`.

        Notes
        -----
        - The `daily_data` DataFrame is directly updated to include the calculated returns.
        - Returns are computed as logarithmic changes for robustness against scaling differences.

        Examples
        --------
        
        >>> data.generate_cache(stk_id=["000001.SZ"], date_range=(20200101, 20201231))
        >>> data.AStocks
        ['000001.SZ']
        >>> data.DateRange
        (20200101, 20201231)

        After running:
        
        >>> return_fields = ["return", "open_return", "high_return", "low_return", "open_close_return", "high_low_return"]
        >>> returns_data = data.get_data(fields=return_fields)
        >>> returns_data.head()
        stk_id       date    return  open_return  high_return  low_return  open_close_return  high_low_return
        0  000001.SZ 2020-01-02  0.0012     -0.0008       0.0021     -0.0012             0.0003          0.0017
        """
        for data_type in self.data_paths.keys():
            data = self._load_data(data_type)
            # Check for required columns
            required_columns = ['stk_id', 'date']
            for col in required_columns:
                if col not in data.columns:
                    raise KeyError(f"Column '{col}' not found in {data_type} data.")
            # Filter by stock ID and date range
            if stk_id:
                data = data[data['stk_id'].isin(stk_id)]
            if date_range:
                start_date, end_date = map(lambda x: pd.to_datetime(str(x), format='%Y%m%d'), date_range)
                data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
            # Store filtered data back into cache
            self.cache[data_type] = data
        
        # Cache daily data separately for alignment
        self.daily_data = self.cache.get("daily")
        if self.daily_data is not None:
            # Calculate returns and add to daily_data
            self.daily_data = self._calculate_returns(self.daily_data)
        
        # Update AStocks and DateRange
        self._update_astocks_and_daterange()

    def _ensure_unique_index(self, data: pd.DataFrame, index_cols: List[str]) -> pd.DataFrame:
        '''
        Ensure the DataFrame has a unique index based on specified columns.

        Parameters
        - data (pd.DataFrame): The input DataFrame.
        - index_cols (List[str]): Columns to use for indexing.

        Returns
        - pd.DataFrame: DataFrame with unique index.
        '''
        if not data[index_cols].duplicated().any():
            return data
        return data.sort_values(by=index_cols).drop_duplicates(subset=index_cols, keep='last')

    def get_data(self, fields: List[str], adjust: str = "forward") -> pd.DataFrame:
        """
        Retrieve specific fields from the cached data, aligning them with daily data.
        Optionally apply forward or backward adjustment to price fields.

        Parameters
        ----------
        fields : list of str
            A list of field names to retrieve, e.g., ["open", "close", "balancestatement_9"].
        adjust : str, optional
            The adjustment type for price fields: "none" (no adjustment, default),
            "forward" (apply forward adjustment), or "backward" (apply backward adjustment).

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the requested fields, aligned with `daily_data` by 'stk_id' and 'date'.

        Notes
        -----
        - Adjusts only price-related fields ("open", "high", "low", "close").
        - Requires the "cumadj" field in `daily_data` for adjustment.

        Raises
        ------
        ValueError
            If `daily_data` is not loaded or `adjust` is invalid.
        KeyError
            If a requested field is not found in `daily_data` or any cached dataset.

        Examples
        --------
        Fetch price fields with forward adjustment and align non-daily data:
        
        >>> requested_fields = ["open", "close", "balancestatement_9"]
        >>> adjustment_type = "forward"
        >>> data = data_class.get_data(fields=requested_fields, adjust=adjustment_type)
        >>> display(data.head())
            stk_id       date       open      close  balancestatement_9
        0    000001 2020-01-01  12.345678  13.456789              0.1234
        1    000001 2020-01-02  12.567890  13.678912              0.1235
        2    000001 2020-01-03  12.789012  13.891234              0.1236
        3    000002 2020-01-01   9.876543  10.987654              0.5432
        4    000002 2020-01-02  10.098765  11.209876              0.5433
        """
        if self.daily_data is None:
            raise ValueError("Daily data is not loaded. Please run `generate_cache` first.")
        
        if adjust not in ["none", "forward", "backward"]:
            raise ValueError("Invalid `adjust` option. Choose from 'none', 'forward', or 'backward'.")
        
        # Start with daily data as the base
        merged = self.daily_data[['stk_id', 'date']].copy()
        
        # Iterate through fields to fetch data
        for field in fields:
            if field in self.daily_data.columns:
                # If the field is in daily_data, directly merge it
                field_data = self.daily_data[['stk_id', 'date', field]].copy()
                
                # Apply adjustment if requested and field is a price field
                if adjust != "none" and field in ["open", "high", "low", "close"]:
                    if "cumadj" not in self.daily_data.columns:
                        raise KeyError("`cumadj` field is required for price adjustments.")
                    
                    if adjust == "forward":
                        # Apply forward adjustment
                        field_data[field] = (
                            field_data[field]
                            * self.daily_data["cumadj"]
                            / self.daily_data["cumadj"].iloc[-1]
                        )
                    elif adjust == "backward":
                        # Apply backward adjustment
                        field_data[field] = (
                            field_data[field]
                            * self.daily_data["cumadj"].iloc[0]
                            / self.daily_data["cumadj"]
                        )
                
                merged = pd.merge(merged, field_data, on=['stk_id', 'date'], how='left')
            else:
                # Handle non-daily fields as before
                found = False
                for data_type, data in self.cache.items():
                    if field in data.columns:
                        # Ensure unique index before alignment
                        data = self._ensure_unique_index(data, ['stk_id', 'date'])
                        # Align non-daily data to daily data
                        aligned_data = data[['stk_id', 'date', field]].set_index(['stk_id', 'date'])
                        aligned_data = aligned_data.reindex(
                            index=merged.set_index(['stk_id', 'date']).index, method='ffill'
                        ).reset_index()
                        merged = pd.merge(merged, aligned_data, on=['stk_id', 'date'], how='left')
                        found = True
                        break
                if not found:
                    raise KeyError(f"Field '{field}' not found in any loaded data.")
        return merged