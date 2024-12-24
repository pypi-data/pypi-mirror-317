import pandas as pd

from typing import List, Optional

from Han_BackTest.DataClass import DataClass
from Han_BackTest.FactorClass import FactorClass, FactorLibrary


class StrategyClass:
    """
    Base class for implementing investment strategies.

    This class provides a general framework for developing investment strategies.
    Users can extend this class to implement specific strategies by leveraging
    predefined factors and customizing portfolio construction rules.

    Attributes
    ----------
    name : str
        The name of the strategy.
    factor_library : FactorLibrary
        A library containing the factors required by the strategy.
    stock_universe : list of str, optional
        List of stock IDs to include in the strategy. If None, all available stocks are included.
    start_date : int
        The start date for the strategy in YYYYMMDD format. Default is 20200101.
    end_date : int
        The end date for the strategy in YYYYMMDD format. Default is 20231231.
    positions : pd.DataFrame or None
        A DataFrame storing the portfolio positions (weights) for each stock on each date.
    data : pd.DataFrame or None
        A DataFrame containing the factor data used in the strategy.
    """

    def __init__(
        self,
        name: str,
        factor_library: FactorLibrary,
        stock_universe: Optional[List[str]] = None,
        start_date: int = 20200101,
        end_date: int = 20231231,
    ):
        """
        Initialize the strategy.

        Parameters
        ----------
        name : str
            Name of the strategy.
        factor_library : FactorLibrary
            A library containing the factors required by the strategy.
        stock_universe : list of str, optional
            List of stock IDs to include in the strategy. If None, all available stocks are included.
        start_date : int, optional
            Start date for the strategy in YYYYMMDD format. Default is 20200101.
        end_date : int, optional
            End date for the strategy in YYYYMMDD format. Default is 20231231.

        Examples
        --------
        
        >>> from Han_BackTest.FactorClass import FactorLibrary
        >>> factor_library = FactorLibrary()
        >>> strategy = StrategyClass(
        >>>     name="Momentum Strategy",
        >>>     factor_library=factor_library,
        >>>     stock_universe=["000001.SZ", "000002.SZ"],
        >>>     start_date=20220101,
        >>>     end_date=20221231,
        >>> )
        >>> print(strategy)
        StrategyClass(name=Momentum Strategy, start_date=20220101, end_date=20221231, stock_universe=['000001.SZ', '000002.SZ'])
        """
        self.name = name
        self.factor_library = factor_library
        self.stock_universe = stock_universe
        self.start_date = start_date
        self.end_date = end_date
        self.positions = None
        self.data = None

    def fetch_data(self, data_class: DataClass, required_factors: List[str]):
        """
        Fetch and calculate required factors for the strategy.

        This method fetches data for the specified factors from the `FactorLibrary`.
        It filters the data based on the stock universe and the strategy's date range.

        Parameters
        ----------
        data_class : DataClass
            The data handler class for fetching raw data.
        required_factors : list of str
            The names of the factors required for the strategy.

        Returns
        -------
        None
            Updates the `self.data` attribute with the calculated factors.

        Raises
        ------
        ValueError
            If any of the required factors are not found in the `FactorLibrary`.

        Examples
        --------
        
        >>> factor_library = FactorLibrary()
        >>> strategy = StrategyClass("Momentum Strategy", factor_library)
        >>> strategy.fetch_data(data_class, required_factors=["Momentum", "Volatility"])
        >>> print(strategy.data.head())
        """
        print(f"Fetching data for strategy: {self.name}")
        
        # Convert factor names to FactorClass objects
        factor_objects = []
        for factor_name in required_factors:
            if factor_name not in self.factor_library.factors:
                raise ValueError(f"Factor '{factor_name}' not found in the FactorLibrary. Ensure it is registered.")
            factor_objects.append(self.factor_library.factors[factor_name])

        # Calculate the required factors
        self.data = self.factor_library.calculate(data_class, factors=factor_objects)
        
        # Filter by stock universe if provided
        if self.stock_universe:
            self.data = self.data[self.data["stk_id"].isin(self.stock_universe)]
        
        # Filter by date range
        self.data = self.data[
            (self.data["date"] >= pd.to_datetime(str(self.start_date), format="%Y%m%d")) &
            (self.data["date"] <= pd.to_datetime(str(self.end_date), format="%Y%m%d"))
        ]

    def normalize_positions(self, signals: pd.DataFrame, long_short: bool) -> pd.DataFrame:
        """
        Normalize signals to generate portfolio weights.

        This method normalizes raw signals into portfolio weights for each stock,
        ensuring that the weights sum to 1 (or -1 for short positions) on each date.

        Parameters
        ----------
        signals : pd.DataFrame
            A DataFrame containing 'stk_id', 'date', and 'signal'.
        long_short : bool
            Whether the strategy allows short positions.

        Returns
        -------
        pd.DataFrame
            A DataFrame with normalized portfolio weights, including 'stk_id', 'date', and 'weight'.

        Raises
        ------
        ValueError
            If the input `signals` DataFrame is empty.

        Examples
        --------
        
        >>> signals = pd.DataFrame({
        >>>     "stk_id": ["000001.SZ", "000002.SZ"],
        >>>     "date": ["2023-01-01", "2023-01-01"],
        >>>     "signal": [1.5, -1.0],
        >>> })
        >>> normalized = strategy.normalize_positions(signals, long_short=True)
        >>> print(normalized)
        """
        if signals is None or signals.empty:
            raise ValueError("Signals are empty. Ensure signals are generated before normalization.")

        def normalize_long_short(group):
            """
            Normalize signals into portfolio weights using the long-short split method.
            
            Parameters
            ----------
            group : pd.Series
                A Series of signals for a specific date.
                
            Returns
            -------
            pd.Series
                A Series of normalized portfolio weights, where long and short positions 
                are scaled separately to ensure balance.
            """
            # Separate positive (long) and negative (short) signals
            long_signals = group[group > 0]
            short_signals = group[group < 0]

            # Normalize long signals
            if not long_signals.empty:
                long_weights = long_signals / long_signals.sum()
            else:
                long_weights = pd.Series(index=group.index, dtype=float)

            # Normalize short signals
            if not short_signals.empty:
                short_weights = short_signals / short_signals.abs().sum()
            else:
                short_weights = pd.Series(index=group.index, dtype=float)

            # Combine normalized long and short weights
            normalized_weights = pd.concat([long_weights, short_weights]).reindex(group.index).fillna(0)

            return normalized_weights

        def normalize_long_only(group):
            positive_signals = group.clip(lower=0)
            return positive_signals / positive_signals.sum()

        if long_short:
            signals["weight"] = signals.groupby("date")["signal"].transform(normalize_long_short)
        else:
            signals["weight"] = signals.groupby("date")["signal"].transform(normalize_long_only)

        return signals[["stk_id", "date", "weight"]]

    def get_positions(self) -> pd.DataFrame:
        """
        Retrieve portfolio positions as a wide-format DataFrame.

        This method converts the internal `positions` DataFrame to a wide-format
        DataFrame where rows are dates, columns are stock IDs, and values are weights.

        Returns
        -------
        pd.DataFrame
            A wide-format DataFrame with portfolio positions.

        Raises
        ------
        ValueError
            If no positions have been generated yet.

        Examples
        --------
        
        >>> strategy.positions = pd.DataFrame({
        >>>     "stk_id": ["000001.SZ", "000002.SZ"],
        >>>     "date": ["2023-01-01", "2023-01-01"],
        >>>     "weight": [0.6, 0.4],
        >>> })
        >>> wide_positions = strategy.get_positions()
        >>> print(wide_positions.head())
        """
        if self.positions is None:
            raise ValueError("No positions have been generated. Please run `generate_positions` first.")
        
        wide_positions = self.positions.pivot(index="date", columns="stk_id", values="weight")
        wide_positions = wide_positions.fillna(0)
        return wide_positions

    def __repr__(self):
        """
        String representation of the strategy.

        Returns
        -------
        str
            A string summarizing the strategy's basic information.

        Examples
        --------
        
        >>> print(strategy)
        StrategyClass(name=Momentum Strategy, start_date=20220101, end_date=20221231, stock_universe=None)
        """
        return (
            f"StrategyClass(name={self.name}, start_date={self.start_date}, "
            f"end_date={self.end_date}, stock_universe={self.stock_universe})"
        )