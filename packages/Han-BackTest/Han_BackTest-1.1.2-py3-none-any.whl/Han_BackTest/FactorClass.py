import pandas as pd

from typing import Callable, List, Dict, Optional

from Han_BackTest.DataClass import DataClass
from pathos.multiprocessing import Pool, cpu_count


class FactorClass:
    """
    Represents a single financial factor with its calculation logic and data dependencies.

    Attributes
    ----------
    name : str
        The name of the factor (e.g., "Momentum").
    description : str
        A brief description of the factor.
    calculation_fn : Callable[[pd.DataFrame], pd.Series]
        A function that defines how to calculate the factor.
        It takes a DataFrame as input and returns a Series.
    required_fields : list
        A list of column names required for the calculation 
        (e.g., ["close", "volume"]).
    """

    def __init__(self, 
                 name: str, 
                 description: str, 
                 calculation_fn: Callable[[pd.DataFrame], pd.Series], 
                 required_fields: list):
        """
        Initialize a factor.

        Parameters
        ----------
        name : str
            The name of the factor, e.g., "Momentum".
        description : str
            A brief description of the factor.
        calculation_fn : callable
            A function that defines how to calculate the factor.
            Should take a DataFrame as input and return a Series as output.
        required_fields : list
            A list of field names (column names) required for the calculation, 
            e.g., ["close", "volume"].

        Examples
        --------
        >>> def momentum(data):
        ...     return data['close'].pct_change(5)
        >>> factor = FactorClass(
        ...     name="Momentum",
        ...     description="5-day momentum factor",
        ...     calculation_fn=momentum,
        ...     required_fields=["close"]
        ... )
        """
        self.name = name
        self.description = description
        self.calculation_fn = calculation_fn
        self.required_fields = required_fields

    def fetch_data(self, data_class) -> pd.DataFrame:
        """
        Fetch required data using DataClass.

        Parameters
        ----------
        data_class : DataClass
            An instance of DataClass to fetch data.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the required fields for factor calculation.

        Examples
        --------
        
        >>> factor = FactorClass(
        >>>     name="Momentum",
        >>>     description="5-day momentum",
        >>>     calculation_fn=lambda data: data['close'].pct_change(5),
        >>>     required_fields=["close"]
        >>> )
        >>> factor.fetch_data(data_class)
        """
        return data_class.get_data(fields=self.required_fields)

    @staticmethod
    def calculate_for_stock(args):
        """
        Static method to calculate factor values for a single stock.

        Parameters
        ----------
        args : tuple
            A tuple containing stock ID, stock data, calculation function, and factor name.

        Returns
        -------
        pd.DataFrame
            A DataFrame with calculated factor values for the given stock.

        Examples
        --------
        
        >>> args = ("000001.SZ", stock_data, lambda df: df['close'].pct_change(5), "Momentum")
        >>> FactorClass.calculate_for_stock(args)
        """
        stk_id, group, calculation_fn, factor_name = args
        factor_series = calculation_fn(group)
        return pd.DataFrame({
            'stk_id': stk_id,
            'date': group['date'].values,
            factor_name: factor_series.values
        })

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate the factor values for each stock on each day using multiprocessing.

        Parameters
        ----------
        data : pd.DataFrame
            The input data required for factor calculation, including 'stk_id' and 'date'.

        Returns
        -------
        pd.DataFrame
            A DataFrame with 'stk_id', 'date', and the calculated factor values.

        Examples
        --------
        
        >>> data = pd.DataFrame({
        >>>     'stk_id': ['000001.SZ'] * 10,
        >>>     'date': pd.date_range("2023-01-01", periods=10),
        >>>     'close': [10, 11, 12, 13, 14, 15, 14, 13, 12, 11]
        >>> })
        >>> factor = FactorClass(
        >>>     name="Momentum",
        >>>     description="5-day momentum",
        >>>     calculation_fn=lambda df: df['close'].pct_change(5),
        >>>     required_fields=["close"]
        >>> )
        >>> factor.calculate(data)
        """
        # Ensure data is sorted by 'stk_id' and 'date'
        data = data.sort_values(by=['stk_id', 'date'])

        # Prepare arguments for each stock group
        grouped_data = [
            (stk_id, group, self.calculation_fn, self.name)
            for stk_id, group in data.groupby('stk_id')
        ]

        # Use pathos Pool to process each group
        with Pool(cpu_count()) as pool:
            results = pool.map(FactorClass.calculate_for_stock, grouped_data)

        # Combine results
        result = pd.concat(results, ignore_index=True)
        result = result[['stk_id', 'date', self.name]]
        return result

    def __repr__(self):
        """
        Representation of the factor for easy identification.
        """
        return f"FactorClass(name={self.name}, description={self.description})"


class FactorLibrary:
    """
    Manages a collection of financial factors for calculation and analysis.

    Attributes
    ----------
    factors : dict
        A dictionary mapping factor names to FactorClass instances.
    nan_proportions : dict
        A dictionary mapping factor names to their NaN proportions.
    """

    def __init__(self):
        """
        Initialize an empty FactorLibrary instance.

        Examples
        --------
        
        >>> library = FactorLibrary()
        """
        self.factors: Dict[str, FactorClass] = {}
        self.nan_proportions: Dict[str, float] = {}

    def register_factors(self, factors: List[FactorClass]):
        """
        Register a list of factors to the library.

        This method allows batch registration of multiple factors at once.
        Each factor must have a unique name; duplicate names will raise an error.

        Parameters
        ----------
        factors : list of FactorClass
            A list of FactorClass instances to register.

        Returns
        -------
        None
            Adds the factors to the library for future calculations.

        Raises
        ------
        ValueError
            If a factor with the same name is already registered in the library.

        Examples
        --------
        >>> factor1 = FactorClass(
        ...     name="Momentum",
        ...     description="5-day momentum factor",
        ...     calculation_fn=lambda df: df['close'].pct_change(5),
        ...     required_fields=["close"]
        ... )
        >>> factor2 = FactorClass(
        ...     name="Volatility",
        ...     description="21-day rolling volatility",
        ...     calculation_fn=lambda df: df['close'].rolling(21).std(),
        ...     required_fields=["close"]
        ... )
        >>> library.register_factors([factor1, factor2])
        Registered Momentum
        Registered Volatility
        """
        for factor in factors:
            if factor.name in self.factors:
                raise ValueError(f"Factor '{factor.name}' is already registered.")
            self.factors[factor.name] = factor
            print(f"Registered {factor.name}")

    def calculate(self, data_class: DataClass, factors: Optional[List[FactorClass]] = None, nan_threshold: float = 0.2):
        """
        Calculate registered factors and update their NaN proportions.

        This method calculates the values for registered factors. If a factor's NaN 
        proportion exceeds the specified threshold, it is skipped, and its values 
        are not included in the final output.

        Parameters
        ----------
        data_class : DataClass
            An instance of DataClass to fetch and provide data for calculations.
        factors : list of FactorClass, optional
            A subset of factors to calculate. If None, calculates all registered factors.
        nan_threshold : float, optional
            The maximum allowed proportion of NaN values for a factor to be included 
            in the final output (default is 0.2).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing all calculated factors with 'stk_id' and 'date' columns.

        Raises
        ------
        KeyError
            If the required fields for a factor are missing in the provided data.

        Examples
        --------
        
        >>> library.calculate(data_class)
        Calculated Momentum: NaN proportion 1.23%
        Calculated Volatility: NaN proportion 0.87%
        >>> library.calculate(data_class, factors=[factor1], nan_threshold=0.1)
        Skipped Momentum: NaN proportion 1.23%
        """
        results = []
        factors_to_calculate = factors or list(self.factors.values())

        for factor in factors_to_calculate:
            try:
                # Fetch data for the factor
                data_for_factor = factor.fetch_data(data_class)
                # Calculate the factor
                factor_values = factor.calculate(data_for_factor)
                # Compute NaN proportion
                nan_proportion = factor_values[factor.name].isna().mean()

                # Update NaN proportions if within threshold
                if nan_proportion <= nan_threshold:
                    self.nan_proportions[factor.name] = nan_proportion
                    results.append(factor_values.set_index(['stk_id', 'date']))
                    print(f"Calculated {factor.name}: NaN proportion {nan_proportion:.2%}")
                else:
                    print(f"Skipped {factor.name}: NaN proportion {nan_proportion:.2%}")
            except KeyError as e:
                print(f"Skipped {factor.name}: Missing required fields {e}")

        # Combine all calculated factors into a single DataFrame
        if results:
            combined = pd.concat(results, axis=1).reset_index()
            return combined
        else:
            print("No factors were calculated due to NaN threshold.")
            return pd.DataFrame()

    def remove_factor(self, name: str):
        """
        Remove a factor from the library by its name.

        This method deletes a registered factor from the library. It also removes 
        any associated NaN proportion records.

        Parameters
        ----------
        name : str
            The name of the factor to remove.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the specified factor name does not exist in the library.

        Examples
        --------
        
        >>> library.remove_factor("Momentum")
        Removed factor 'Momentum' from the library.
        """
        if name not in self.factors:
            raise KeyError(f"Factor '{name}' not found in the library.")
        del self.factors[name]
        self.nan_proportions.pop(name, None)
        print(f"Removed factor '{name}' from the library.")

    def list_factors(self) -> pd.DataFrame:
        """
        List all registered factors, their details, and NaN proportions.

        This method provides an overview of all registered factors, including their 
        names, descriptions, required fields, and the proportion of NaN values 
        encountered during their calculation.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing details of all registered factors:
            - Name: Name of the factor
            - Description: Description of the factor
            - Required Fields: Fields required for the factor's calculation
            - NaN Proportion: The proportion of NaN values encountered

        Examples
        --------
        
        >>> library.list_factors()
            Name            Description              Required Fields NaN Proportion
        0   Momentum  5-day momentum factor              ['close']      1.23%
        1  Volatility  21-day rolling volatility         ['close']      0.87%
        """
        factor_data = [
            {
                "Name": factor.name,
                "Description": factor.description,
                "Required Fields": factor.required_fields,
                "NaN Proportion": f"{self.nan_proportions.get(factor.name, 'N/A'):.2%}"
                if factor.name in self.nan_proportions else "N/A",
            }
            for factor in self.factors.values()
        ]
        return pd.DataFrame(factor_data)

    def __repr__(self):
        """
        Representation of the factor library.
        """
        return f"FactorLibrary({list(self.factors.keys())})"