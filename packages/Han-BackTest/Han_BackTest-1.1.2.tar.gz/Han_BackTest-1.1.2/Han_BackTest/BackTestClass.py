import numpy as np
import pandas as pd
import seaborn as sns
import ipywidgets as widgets
import matplotlib.pyplot as plt

from IPython.display import display, clear_output

from typing import List, Optional
from Han_BackTest.DataClass import DataClass
from Han_BackTest.FactorClass import FactorClass, FactorLibrary
from Han_BackTest.StrategyClass import StrategyClass


class BackTestClass:
    """
    A class to conduct backtests on investment strategies with memory optimizations.

    This class provides a framework for conducting backtests on investment strategies. 
    It integrates with `StrategyClass` to generate positions, calculate returns, and evaluate 
    portfolio performance against a benchmark. Additionally, it includes tools for visualizing 
    results and comparing strategies.

    Features
    --------
    - **Integration with StrategyClass**: Automatically handles position generation and data fetching.
    - **Performance Metrics**: Includes methods for calculating NAV, returns, Sharpe ratio, 
      drawdowns, and volatility.
    - **Benchmark Comparison**: Supports evaluation of strategy performance relative to a benchmark.
    - **Visualization Tools**: Provides various plotting methods for NAV, excess returns, 
      and position weight matrices.
    - **Interactive Analysis**: Includes widgets for interactive strategy comparison and analysis.
    """
    
    def __init__(
        self,
        strategy: StrategyClass,
        data_class: DataClass,
        start_date: int,
        end_date: int,
        initial_capital: float = 1.0,
        lag: int = 2,
        benchmark: Optional[str] = None,
        limits: bool = True,  # Add limits parameter
    ):
        """
        Initialize the backtest class and handle data, factor, and strategy setup.

        Parameters
        ----------
        strategy : StrategyClass
            The trading strategy being tested.
        data_class : DataClass
            The data handler providing market data.
        start_date : int
            Start date for the backtest (YYYYMMDD format).
        end_date : int
            End date for the backtest (YYYYMMDD format).
        initial_capital : float, optional
            Starting capital for the backtest. Default is 1.0.
        lag : int, optional
            Lag in days between position signal and return realization. Default is 2.
        benchmark : str, optional
            Ticker symbol for the benchmark. Default is None, implying a dynamically computed benchmark.
        limits : bool, optional
            If True, mask returns >= 10% or <= -10% (e.g., limit up/down). Default is True.
        """
        self.strategy = strategy
        self.data_class = data_class
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.lag = lag
        self.benchmark = benchmark
        self.limits = limits  # Store the `limits` parameter as an instance attribute
        self.positions = None
        self.symbol_returns = None
        self.nav = None
        self.returns = None
        self.benchmark_returns = None
        self.excess_returns = None

        # Step 1: Generate data cache for the given date range
        print(f"Generating data cache for {self.start_date} to {self.end_date}...")
        attempts = 0
        while attempts < 30:
            try:
                self.data_class.generate_cache(date_range=(self.start_date, self.end_date))
                break
            except Exception as e:
                print(f"Data cache generation failed: {e}")
                self.end_date -= 1  # Move end_date one day earlier
                attempts += 1
                if attempts >= 30:
                    raise ValueError("Exceeded maximum attempts to generate data cache.")

        # Step 2: Update strategy's date range
        print(f"Setting strategy date range to {self.start_date} - {self.end_date}...")
        self.strategy.start_date = self.start_date
        self.strategy.end_date = self.end_date

        # Step 3: Fetch required data for the strategy
        print("Fetching data for the strategy...")
        self.strategy.fetch_data(data_class=self.data_class, required_factors=self.strategy._factor_library.factors)

        # Step 4: Generate positions for the strategy
        print("Generating positions for the strategy...")
        self.strategy.generate_positions()

        print("BackTestClass initialized successfully.")

    def calculate_returns(self):
        """
        Calculate daily portfolio returns using lagged positions and store individual stock returns.

        This method computes the portfolio's daily returns based on the strategy's positions
        and the stock-level log returns. If the `limits` attribute is set to `True`, extreme
        stock-level returns (greater than or equal to 10% or less than or equal to -10%) are masked
        to 0 before calculating portfolio returns.

        Returns
        -------
        pd.Series
            A Pandas Series of daily portfolio returns indexed by date.

        Notes
        -----
        - Daily returns for individual stocks are stored in `self.symbol_returns` for reuse.
        - Portfolio returns are computed as the weighted sum of daily stock returns.
        - Positions are shifted by `self.lag` days to simulate execution delays.
        - If `limits` is enabled, extreme returns are masked to avoid distortions in portfolio performance.

        Raises
        ------
        ValueError
            If no positions are available. Ensure `strategy.generate_positions()` is called 
            before invoking this method.

        Examples
        --------
        
        >>> # Initialize BackTestClass
        >>> backtest = BackTestClass(
        ...     strategy=my_strategy,
        ...     data_class=data,
        ...     start_date=20200101,
        ...     end_date=20231231,
        ...     lag=2,
        ...     limits=True
        ... )
        
        >>> # Calculate returns
        >>> returns = backtest.calculate_returns()
        ... Calculating strategy returns...
        ... Applying limits: masking returns >= 10% or <= -10%...
        >>> returns.head()
        ... date
        ... 2020-01-03    0.0025
        ... 2020-01-06   -0.0017
        ... 2020-01-07    0.0031
        ... 2020-01-08   -0.0028
        ... 2020-01-09    0.0012
        dtype: float64
        """
        print("Calculating strategy returns...")

        # Validate positions
        if self.strategy.positions is None or self.strategy.positions.empty:
            raise ValueError("No positions available. Ensure `strategy.generate_positions()` has been called.")

        # Fetch daily close prices and calculate log returns
        daily_prices = self.data_class.get_data(fields=["close"])  # Retrieve close prices
        daily_prices_pivot = daily_prices.pivot(index="date", columns="stk_id", values="close")

        # Calculate and store symbol returns
        self.symbol_returns = np.log(daily_prices_pivot / daily_prices_pivot.shift(1))  # Log returns

        # Apply limits if enabled
        if self.limits:
            print("Applying limits: masking returns >= 10% or <= -10%...")
            self.symbol_returns = self.symbol_returns.mask(
                (self.symbol_returns >= 0.10) | (self.symbol_returns <= -0.10), 0
            )

        # Align positions with returns and apply lag
        wide_positions = self.strategy.get_positions()
        wide_positions = wide_positions.reindex(index=self.symbol_returns.index, columns=self.symbol_returns.columns).fillna(0)
        lagged_positions = wide_positions.shift(self.lag).fillna(0)  # Shift positions by lag days

        # Calculate portfolio returns as the weighted sum of daily returns
        self.returns = (lagged_positions * self.symbol_returns).sum(axis=1)

        # Return the calculated portfolio returns
        return self.returns

    def calculate_nav(self):
        """
        Calculate the net asset value (NAV) of the portfolio.

        NAV is computed as the cumulative sum of portfolio returns, 
        starting from the initial capital.

        Returns
        -------
        pd.Series
            A Pandas Series representing the NAV indexed by date.

        Raises
        ------
        ValueError
            If no returns are available and cannot be computed.

        Notes
        -----
        - The method assumes portfolio returns have been computed prior to calculating NAV.
        - The initial NAV is set to 1 (or the starting capital).
        - If no returns are available, the method will call `calculate_returns()`.

        Examples
        --------
        
        >>> backtest.calculate_returns()  # Ensure returns are calculated
        ... Calculating strategy returns...
        >>> nav = backtest.calculate_nav()
        ... Calculating net asset value (NAV)...
        >>> nav.head()
        ... date
        ... 2020-01-03    1.0000
        ... 2020-01-06    1.0025
        ... 2020-01-07    1.0008
        ... 2020-01-08    1.0039
        ... 2020-01-09    1.0011
        ... dtype: float64
        """
        print("Calculating net asset value (NAV)...")

        # Ensure returns are available before computing NAV
        if self.returns is None:
            print("Portfolio returns not found. Calculating returns first...")
            self.calculate_returns()

        # Compute NAV by adding cumulative sum of log returns to initial NAV
        self.nav = 1 + self.returns.cumsum()

        # Return the NAV series
        return self.nav

    def calculate_benchmark_returns(self):
        """
        Calculate volume-weighted benchmark log returns.

        The benchmark is computed as the volume-weighted average of daily 
        closing prices across all stocks. Log returns are then calculated 
        based on the benchmark's price changes.

        Returns
        -------
        pd.Series
            A Pandas Series of benchmark log returns indexed by date.

        Raises
        ------
        ValueError
            If data for `close` or `volume` fields is missing.

        Notes
        -----
        - This method calculates a dynamic benchmark based on the weighted 
        average price of all stocks, adjusted for trading volume.
        - Logarithmic returns are used for stability and easier cumulative 
        computations in backtesting.

        Examples
        --------
        After initializing the backtest:
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2)
        >>> benchmark_returns = backtest.calculate_benchmark_returns()
        ... Calculating benchmark log returns...
        >>> benchmark_returns.head()
        ... date
        ... 2020-01-03    0.0008
        ... 2020-01-06    0.0012
        ... 2020-01-07   -0.0005
        ... 2020-01-08    0.0009
        ... 2020-01-09   -0.0002
        ... dtype: float64
        """
        print("Calculating benchmark log returns...")

        # Fetch daily close prices and volumes
        close_prices = self.data_class.get_data(fields=["close"], adjust="forward").pivot(index="date", columns="stk_id", values="close")
        volume_data = self.data_class.get_data(fields=["volume"]).pivot(index="date", columns="stk_id", values="volume")

        # Ensure alignment of close prices and volumes
        close_prices, volume_data = close_prices.align(volume_data, axis=0)

        # Compute volume-weighted average close price for each date
        weighted_close = np.nansum(close_prices.values * volume_data.values, axis=1)
        volume_sum = np.nansum(volume_data.values, axis=1)
        daily_benchmark = weighted_close / volume_sum

        # Calculate log returns for the benchmark
        self.benchmark_returns = pd.Series(
            np.log(daily_benchmark[1:] / daily_benchmark[:-1]),
            index=close_prices.index[1:]
        )
        return self.benchmark_returns

    def calculate_daily_excess_returns(self):
        """
        Calculate daily excess returns relative to the benchmark.

        Excess returns measure the difference between the strategy's daily 
        portfolio returns and the benchmark's daily returns. These are key 
        metrics for assessing whether the strategy outperforms the benchmark 
        on a day-to-day basis.

        Returns
        -------
        pd.Series
            A Pandas Series of daily excess returns indexed by date.

        Raises
        ------
        ValueError
            If strategy returns are unavailable or benchmark returns have 
            not been calculated.

        Notes
        -----
        - Excess returns are calculated as:
        `Excess Returns = Strategy Returns - Benchmark Returns`
        - This method assumes that both strategy returns and benchmark 
        returns have already been calculated.

        Examples
        --------
        Calculate daily excess returns after initializing the backtest:
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2)
        >>> backtest.calculate_returns()  # Ensure strategy returns are computed
        ... Calculating strategy returns...
        >>> backtest.calculate_benchmark_returns()  # Ensure benchmark returns are computed
        ... Calculating benchmark log returns...
        >>> excess_returns = backtest.calculate_daily_excess_returns()
        ... Calculating daily excess returns...
        >>> excess_returns.head()
        ... date
        ... 2020-01-03    0.0004
        ... 2020-01-06   -0.0003
        ... 2020-01-07    0.0006
        ... 2020-01-08   -0.0001
        ... 2020-01-09    0.0002
        ... dtype: float64
        """
        print("Calculating daily excess returns...")

        if self.returns is None:
            raise ValueError("Strategy returns not available. Run calculate_returns() first.")

        if self.benchmark_returns is None:
            self.calculate_benchmark_returns()

        # Excess returns: strategy log returns minus benchmark log returns
        self.excess_returns = self.returns[1:] - self.benchmark_returns
        return self.excess_returns

    def calculate_cumulative_excess_returns(self):
        """
        Calculate cumulative excess returns as the difference between the 
        cumulative strategy returns and cumulative benchmark returns.

        Cumulative excess returns provide a measure of the total 
        outperformance or underperformance of the strategy compared to 
        the benchmark over time.

        Returns
        -------
        pd.Series
            A Pandas Series of cumulative excess returns indexed by date.

        Raises
        ------
        ValueError
            If strategy returns or benchmark returns are unavailable.

        Notes
        -----
        - Cumulative returns are calculated by summing up daily log returns.
        - Cumulative excess returns are then derived as:
        `Cumulative Excess Returns = Cumulative Strategy Returns - Cumulative Benchmark Returns`
        - The method ensures both strategy and benchmark returns are available 
        before computation.

        Examples
        --------
        Compute cumulative excess returns after backtest initialization:
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2)
        >>> backtest.calculate_returns()  # Compute strategy returns
        ... Calculating strategy returns...
        >>> backtest.calculate_benchmark_returns()  # Compute benchmark returns
        ... Calculating benchmark log returns...
        >>> cumulative_excess_returns = backtest.calculate_cumulative_excess_returns()
        ... Calculating cumulative excess returns...
        >>> cumulative_excess_returns.head()
        ... date
        ... 2020-01-03    0.0003
        ... 2020-01-06   -0.0002
        ... 2020-01-07    0.0005
        ... 2020-01-08   -0.0001
        ... 2020-01-09    0.0002
        ... dtype: float64
        """
        print("Calculating cumulative excess returns...")

        if self.returns is None:
            raise ValueError("Strategy returns not available. Run calculate_returns() first.")

        if self.benchmark_returns is None:
            self.calculate_benchmark_returns()

        # Calculate cumulative log returns for strategy and benchmark
        cumulative_strategy_returns = self.returns.cumsum()
        cumulative_benchmark_returns = pd.Series(
            np.cumsum(self.benchmark_returns.values),
            index=self.benchmark_returns.index
        )

        # Compute cumulative excess returns
        cumulative_excess_returns = cumulative_strategy_returns[1:] - cumulative_benchmark_returns
        return cumulative_excess_returns

    def calculate_annualized_return(self):
        """
        Calculate the annualized return for the strategy over time.

        Annualized return measures the compounded growth rate of the portfolio
        over the entire backtesting period. It accounts for the length of 
        the backtest and provides a standardized performance metric.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the annualized return indexed by date. The column
            "Annualized Return" represents the calculated annualized return.

        Raises
        ------
        ValueError
            If `calculate_nav` has not been run prior to calling this function.

        Notes
        -----
        - Annualized return is calculated using the formula:
        `Annualized Return = ((1 + Cumulative Return) ** (252 / Days)) - 1`
        where `252` is the average number of trading days in a year.
        - The function assumes that the cumulative return is compounded daily.

        Examples
        --------
        Calculate annualized returns after running the backtest:
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2)
        >>> backtest.calculate_nav()  # Compute NAV
        ... Calculating net asset value (NAV)...
        >>> annualized_returns = backtest.calculate_annualized_return()
        ... Final Annualized Return: 15.24%
        >>> annualized_returns.tail()
        ...             Annualized Return
        ... date                            
        ... 2023-12-27               0.1492
        ... 2023-12-28               0.1500
        ... 2023-12-29               0.1510
        ... 2023-12-30               0.1524
        ... 2023-12-31               0.1524
        """
        print("Calculating annualized return...")

        if self.nav is None:
            self.calculate_nav()

        # Calculate daily returns from NAV
        daily_returns = self.nav.pct_change()

        # Calculate cumulative return and annualized return
        cumulative_return = (1 + daily_returns).cumprod() - 1  # Cumulative returns
        days = (self.nav.index - self.nav.index[0]).days       # Days since start
        annualized_return = (1 + cumulative_return) ** (252 / days) - 1

        # Format the result into a DataFrame
        result = pd.DataFrame({"Annualized Return": annualized_return}, index=self.nav.index)

        # Print the final annualized return
        print(f"Final Annualized Return: {result.iloc[-1, 0]:.2%}")

        return result

    def calculate_annualized_volatility(self):
        """
        Calculate the annualized volatility for the strategy over time.

        Annualized volatility measures the standard deviation of portfolio returns
        scaled to an annual basis. It reflects the risk or variability of returns
        and is a key component of portfolio performance evaluation.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the annualized volatility indexed by date. The column
            "Annualized Volatility" represents the calculated volatility.

        Raises
        ------
        ValueError
            If `calculate_returns` has not been run prior to calling this function.

        Notes
        -----
        - Annualized volatility is calculated as:
        `Annualized Volatility = Daily Volatility × √252`
        where `252` is the average number of trading days in a year.
        - The rolling window for daily volatility calculation is set to 252 days.

        Examples
        --------
        Calculate annualized volatility after running the backtest:
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2)
        >>> backtest.calculate_returns()  # Compute daily returns
        ... Calculating strategy returns...
        >>> annualized_volatility = backtest.calculate_annualized_volatility()
        ... Final Annualized Volatility: 20.35%
        >>> annualized_volatility.tail()
        ...             Annualized Volatility
        ... date                               
        ... 2023-12-27                   0.2012
        ... 2023-12-28                   0.2020
        ... 2023-12-29                   0.2030
        ... 2023-12-30                   0.2035
        ... 2023-12-31                   0.2035
        """
        print("Calculating annualized volatility...")

        if self.returns is None:
            self.calculate_returns()

        # Calculate rolling standard deviation of daily returns (252-day window)
        rolling_volatility = self.returns.rolling(window=252).std()

        # Annualize the volatility
        annualized_volatility = rolling_volatility * (252 ** 0.5)

        # Format the result into a DataFrame
        result = pd.DataFrame({"Annualized Volatility": annualized_volatility}, index=self.returns.index)

        # Print the final annualized volatility
        print(f"Final Annualized Volatility: {result.iloc[-1, 0]:.2%}")

        return result

    def calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """
        Calculate the Sharpe ratio of the strategy relative to both a benchmark and a risk-free rate.

        The Sharpe ratio measures the risk-adjusted return of a portfolio. It is defined as the
        ratio of excess return (over a benchmark or a risk-free rate) to the standard deviation of returns.

        Parameters
        ----------
        risk_free_rate : float, optional
            The annualized risk-free rate (e.g., 0.02 for 2%). Default is 0.02.

        Returns
        -------
        pd.DataFrame
            A DataFrame with two columns:
            - 'Sharpe (Benchmark)': Sharpe ratio relative to the benchmark
            - 'Sharpe (Risk-Free)': Sharpe ratio relative to the risk-free rate

        Raises
        ------
        ValueError
            If `calculate_returns` or `calculate_benchmark_returns` has not been run prior to calling this function.

        Notes
        -----
        - The Sharpe ratio is calculated as:
        `Sharpe Ratio = Annualized Excess Return / Annualized Volatility`
        - Annualized excess return is computed from cumulative excess returns over time.
        - Annualized volatility is the standard deviation of daily returns scaled to an annual basis.

        Examples
        --------
        Calculate Sharpe ratios after running the backtest:
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2, benchmark="000300.SH")
        >>> backtest.calculate_returns()  # Compute daily returns
        ... Calculating strategy returns...
        >>> backtest.calculate_benchmark_returns()  # Compute benchmark returns
        ... Calculating benchmark log returns...
        >>> sharpe_ratios = backtest.calculate_sharpe_ratio(risk_free_rate=0.03)
        ... Final Sharpe Ratio (Benchmark): 1.50
        ... Final Sharpe Ratio (Risk-Free): 1.80
        >>> sharpe_ratios.tail()
        ...             Sharpe (Benchmark)  Sharpe (Risk-Free)
        ... date                                               
        ... 2023-12-27                 1.48                1.79
        ... 2023-12-28                 1.49                1.80
        ... 2023-12-29                 1.50                1.80
        ... 2023-12-30                 1.50                1.80
        ... 2023-12-31                 1.50                1.80
        """
        print("Calculating Sharpe ratios...")

        if self.returns is None:
            self.calculate_returns()

        if self.benchmark_returns is None:
            self.calculate_benchmark_returns()

        # Align strategy returns and benchmark returns
        aligned_benchmark_returns = self.benchmark_returns.reindex(self.returns.index)

        # Calculate cumulative excess returns over the benchmark
        cumulative_excess_benchmark = (self.returns - aligned_benchmark_returns).cumsum()

        # Calculate cumulative excess returns over the risk-free rate
        daily_risk_free_rate = risk_free_rate / 252
        cumulative_excess_rf = (self.returns - daily_risk_free_rate).cumsum()

        # Calculate Sharpe ratios
        def sharpe_ratio(cum_excess_returns):
            """Helper function to calculate Sharpe ratio."""
            days = np.arange(1, len(cum_excess_returns) + 1)
            annualized_excess = cum_excess_returns / (days / 252)
            annualized_volatility = self.returns.expanding().std() * (252 ** 0.5)
            return annualized_excess / annualized_volatility

        sharpe_benchmark = sharpe_ratio(cumulative_excess_benchmark)
        sharpe_rf = sharpe_ratio(cumulative_excess_rf)

        # Combine results into a DataFrame
        result = pd.DataFrame(
            {
                "Sharpe (Benchmark)": sharpe_benchmark,
                "Sharpe (Risk-Free)": sharpe_rf,
            },
            index=self.returns.index
        )

        # Print final Sharpe ratios
        print(f"Final Sharpe Ratio (Benchmark): {result['Sharpe (Benchmark)'].iloc[-1]:.2f}")
        print(f"Final Sharpe Ratio (Risk-Free): {result['Sharpe (Risk-Free)'].iloc[-1]:.2f}")

        return result

    def calculate_max_drawdown(self):
        """
        Calculate the maximum drawdown (MDD) of the portfolio.

        The maximum drawdown is the largest peak-to-trough decline in the portfolio's value over time.
        It is a key metric for assessing risk, as it indicates the worst-case loss experienced
        during the backtest period.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the maximum drawdown (MDD) values indexed by date.

            Columns:
            - "Max Drawdown": Cumulative minimum of the drawdowns.

        Raises
        ------
        ValueError
            If NAV has not been calculated prior to calling this function.

        Notes
        -----
        - The drawdown for a given day is calculated as:
        `Drawdown = (NAV / Running Maximum NAV) - 1`
        - The maximum drawdown up to a given day is the cumulative minimum of drawdowns.

        Examples
        --------
        Calculate and analyze the maximum drawdown:

        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2, benchmark="000300.SH")
        >>> backtest.calculate_returns()  # Ensure returns are computed
        ... Calculating strategy returns...
        >>> backtest.calculate_nav()  # Ensure NAV is computed
        ... Calculating net asset value (NAV)...
        >>> max_drawdown = backtest.calculate_max_drawdown()
        ... Final Maximum Drawdown: -12.35%
        >>> max_drawdown.tail()
        ...             Max Drawdown
        ... date                     
        ... 2023-12-27        -0.1123
        ... 2023-12-28        -0.1205
        ... 2023-12-29        -0.1235
        ... 2023-12-30        -0.1235
        ... 2023-12-31        -0.1235
        """
        print("Calculating maximum drawdown...")

        if self.nav is None:
            self.calculate_nav()

        # Calculate running maximum NAV
        running_max = self.nav.cummax()

        # Calculate drawdowns
        drawdowns = (self.nav / running_max) - 1

        # Calculate maximum drawdown
        max_drawdown = drawdowns.cummin()

        # Create a DataFrame for the results
        result = pd.DataFrame({"Max Drawdown": max_drawdown}, index=self.nav.index)

        # Print the final maximum drawdown
        print(f"Final Maximum Drawdown: {result.iloc[-1, 0]:.2%}")
        return result

    def plot_nav(self, include_benchmark=True, ax=None, width: int = 12, height: int = 6) -> plt.Axes:
        """
        Plot the strategy Net Asset Value (NAV) and optionally the benchmark cumulative return.

        This function visualizes the performance of the strategy's NAV over time. If requested,
        it can also plot the cumulative return of the benchmark for comparison.

        Parameters
        ----------
        include_benchmark : bool, optional
            If True, includes the benchmark cumulative return in the plot. Default is True.
        ax : matplotlib.axes._axes.Axes, optional
            A matplotlib axis to draw on. If None, a new figure and axis will be created.
        width : int, optional
            Width of the plot in inches. Default is 12.
        height : int, optional
            Height of the plot in inches. Default is 6.

        Returns
        -------
        matplotlib.axes._axes.Axes
            The matplotlib axis object containing the plot.

        Raises
        ------
        ValueError
            If the NAV or benchmark returns have not been calculated prior to calling the function.

        Examples
        --------
        Visualizing the NAV and benchmark:

        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2, benchmark="000300.SH")
        >>> backtest.calculate_returns()  # Ensure returns are computed
        ... Calculating strategy returns...
        >>> backtest.calculate_nav()  # Compute NAV
        ... Calculating net asset value (NAV)...
        >>> ax = backtest.plot_nav(include_benchmark=True)

        Customizing the plot further:
        
        >>> ax.set_xlim(pd.Timestamp("2020-01-01"), pd.Timestamp("2023-12-31"))
        >>> ax.set_ylim(0.8, 2.0)
        >>> plt.show()
        """
        print("Plotting NAV and benchmark performance...")

        if self.nav is None:
            self.calculate_nav()

        # Calculate benchmark cumulative returns if required
        if include_benchmark and self.benchmark_returns is None:
            self.calculate_benchmark_returns()
        benchmark_cumulative_returns = None
        if include_benchmark:
            benchmark_cumulative_returns = 1 + self.benchmark_returns.cumsum()

        # Set visualization style
        sns.set_theme(style="whitegrid")

        # Create a new axis if one isn't provided
        if ax is None:
            fig, ax = plt.subplots(figsize=(width, height))

        # Plot benchmark cumulative returns if included
        if include_benchmark:
            ax.plot(
                benchmark_cumulative_returns.index,
                benchmark_cumulative_returns,
                label="Benchmark",
                linestyle="-",
                color=sns.color_palette("deep")[1],
                linewidth=2.5,
            )

        # Plot strategy NAV
        ax.plot(
            self.nav.index,
            self.nav,
            label="Strategy NAV",
            color=sns.color_palette("deep")[0],
            linewidth=2.5,
        )

        # Customize axis labels and legend
        ax.set_xlabel("Date", fontsize=14)
        ax.set_ylabel("Cumulative Return", fontsize=14)
        ax.legend(fontsize=12, loc="upper left", frameon=True, shadow=True)
        ax.grid(alpha=0.5)

        # Automatically format dates on the x-axis
        if ax.get_figure():
            ax.get_figure().autofmt_xdate()

        # Set plot title and x-axis limits
        ax.set_xlim(
            pd.Timestamp(str(self.strategy.start_date)),
            pd.Timestamp(str(self.strategy.end_date)),
        )
        ax.set_title("Strategy vs Benchmark Performance", fontsize=16)

        return ax

    def plot_excess_returns(self, ax=None, width: int = 12, height: int = 6) -> plt.Axes:
        """
        Plot the cumulative excess returns relative to the benchmark.

        This function visualizes the strategy's cumulative excess returns over time, 
        allowing users to assess the strategy's outperformance compared to the benchmark.

        Parameters
        ----------
        ax : matplotlib.axes._axes.Axes, optional
            An existing matplotlib axis to draw on. If None, a new figure and axis will be created.
        width : int, optional
            The width of the plot in inches. Default is 12.
        height : int, optional
            The height of the plot in inches. Default is 6.

        Returns
        -------
        matplotlib.axes._axes.Axes
            The axis object containing the plot.

        Raises
        ------
        ValueError
            If the cumulative excess returns cannot be calculated due to missing data.

        Examples
        --------
        Basic usage:
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, lag=2, benchmark="000300.SH")
        >>> backtest.calculate_daily_excess_returns()  # Ensure daily excess returns are calculated
        >>> ax = backtest.plot_excess_returns()
        ... Plotting cumulative excess returns...
        ... Cumulative excess return over the backtesting period: 12.34%

        Customizing the plot:
        
        >>> ax = backtest.plot_excess_returns(width=16, height=6)
        >>> ax.set_title("Customized Cumulative Excess Returns", fontsize=18)
        >>> ax.set_xlim(pd.Timestamp("2020-01-01"), pd.Timestamp("2023-12-31"))
        >>> plt.show()
        """
        print("Plotting cumulative excess returns...")

        # Ensure cumulative excess returns are calculated
        if self.excess_returns is None:
            self.calculate_daily_excess_returns()
        cumulative_excess_returns = self.excess_returns.cumsum()

        # Calculate final cumulative excess return
        total_excess_return = cumulative_excess_returns.iloc[-1]
        print(
            f"Cumulative excess return over the backtesting period: {total_excess_return:.2%}"
        )

        # Set Seaborn style for better visuals
        sns.set_theme(style="whitegrid")

        # Create a new figure and axis if not provided
        if ax is None:
            fig, ax = plt.subplots(figsize=(width, height))

        # Plot cumulative excess returns
        ax.plot(
            cumulative_excess_returns.index,
            cumulative_excess_returns,
            label="Cumulative Excess Returns",
            color=sns.color_palette("deep")[2],
            linewidth=2.5,
        )

        # Customize the plot
        ax.set_xlabel("Date", fontsize=14)
        ax.set_ylabel("Cumulative Excess Return", fontsize=14)
        ax.set_title("Cumulative Excess Returns", fontsize=16)
        ax.legend(loc="upper left", fontsize=12, frameon=True, shadow=True)
        ax.tick_params(axis="both", which="major", labelsize=12)

        # Add grid lines for better readability
        ax.grid(color="gray", linestyle="-", linewidth=0.5, alpha=0.7)

        # Improve date formatting on the x-axis
        if ax.get_figure():
            ax.get_figure().autofmt_xdate()

        # If a new figure was created, apply tight layout
        if ax is None:
            plt.tight_layout()
            plt.show()

        return ax

    def plot_binplot(
        self,
        num_bins: int = 10,
        swap_axes: bool = False,
        width: int = 12,
        height: int = 6,
        ax=None,
    ) -> plt.Axes:
        """
        Create a bin plot to visualize the relationship between positions and lagged returns.

        Parameters
        ----------
        num_bins : int, optional
            The number of bins to divide the data into. Default is 10.
        swap_axes : bool, optional
            If True, swaps x and y axes (positions as y and returns as x). Default is False.
        width : int, optional
            The width of the plot in inches. Default is 12.
        height : int, optional
            The height of the plot in inches. Default is 6.
        ax : matplotlib.axes._axes.Axes, optional
            Existing matplotlib axis to draw on. Creates a new one if None.

        Returns
        -------
        matplotlib.axes._axes.Axes
            The axis object containing the bin plot.

        Examples
        --------
        
        >>> ax = backtest.plot_binplot(num_bins=15, swap_axes=True)
        >>> ax.set_title("Bin Plot of Lagged Returns and Positions")
        """
        print("Generating bin plot...")

        # Ensure symbol returns and positions are calculated
        if self.symbol_returns is None:
            self.calculate_returns()
        if self.strategy.positions is None or self.strategy.positions.empty:
            raise ValueError("No positions available. Ensure strategy.generate_positions() has been called.")

        # Align positions with lagged returns
        returns = self.symbol_returns
        wide_positions = self.strategy.get_positions().shift(self.lag).fillna(0)
        
        # Align indices of positions and returns to their intersection
        common_index = wide_positions.index.intersection(returns.index)
        wide_positions = wide_positions.loc[common_index]
        returns = returns.loc[common_index]
        positions, returns = wide_positions.align(returns, join="inner", axis=1)

        # Flatten positions and returns for plotting
        x_data = positions.to_numpy().flatten()
        y_data = returns.to_numpy().flatten()

        # Remove NaNs
        mask = ~np.isnan(x_data) & ~np.isnan(y_data)
        x_data = x_data[mask]
        y_data = y_data[mask]

        # Decide the axes
        x_col, y_col = (x_data, y_data) if not swap_axes else (y_data, x_data)

        # Bin data
        bins = pd.cut(x_col, bins=num_bins)
        grouped = pd.DataFrame({"x": x_col, "y": y_col}).groupby(bins)

        # Calculate means and standard deviations for each bin
        bin_centers = grouped["x"].mean()
        y_means = grouped["y"].mean()
        x_stds = grouped["x"].std()
        y_stds = grouped["y"].std()

        # Calculate regression statistics
        corr = np.corrcoef(x_col, y_col)[0, 1]
        slope, intercept = np.polyfit(x_col, y_col, 1)
        t_stat = slope / (np.std(y_col - (slope * x_col + intercept)) / np.sqrt(len(x_col)))

        # Print regression statistics
        # print(f"Correlation: {corr:.4f}")
        # print(f"Slope: {slope:.4f}")
        # print(f"Intercept: {intercept:.4f}")
        # print(f"t-statistic: {t_stat:.4f}")

        # Plot
        sns.set_theme(style="whitegrid")
        palette = sns.color_palette("deep")
        dot_color = palette[0]

        created_new_figure = ax is None
        if ax is None:
            fig, ax = plt.subplots(figsize=(width, height))

        # Plot bin dots
        ax.scatter(bin_centers, y_means, color=dot_color, label="Bin Means", zorder=3)

        # Plot cross-like markers for bin points
        for x, y, x_err, y_err in zip(bin_centers, y_means, x_stds, y_stds):
            ax.plot([x - x_err, x + x_err], [y, y], color=dot_color, linewidth=1.5, zorder=2)  # Horizontal line
            ax.plot([x, x], [y - y_err, y + y_err], color=dot_color, linewidth=1.5, zorder=2)  # Vertical line

        # Add regression line
        regression_line = slope * x_col + intercept
        ax.plot(x_col, regression_line, color=palette[1], label=f"y = {slope:.4f}x + {intercept:.4f}", zorder=4)

        # Add regression stats to the plot
        textstr = (
            f"Corr: {corr:.4f}\n"
            f"Slope: {slope:.4f}\n"
            f"Intercept: {intercept:.4f}\n"
            f"t-stat: {t_stat:.4f}"
        )
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))

        # Customize plot
        ax.set_xlabel("Positions" if not swap_axes else "Lagged Returns", fontsize=14)
        ax.set_ylabel("Lagged Returns" if not swap_axes else "Positions", fontsize=14)
        ax.set_title("Bin Plot of Positions and Lagged Returns", fontsize=16)
        ax.grid(alpha=0.5)
        ax.legend(fontsize=12, loc=1, frameon=True, shadow=True)

        # Tight layout and return
        plt.tight_layout()
        return ax

    def matshow(self, ax=None, width: int = 12, height: int = 6):
        """
        Visualize the weight matrix as a heatmap using `seaborn.heatmap`.

        Parameters
        ----------
        ax : matplotlib.axes._axes.Axes, optional
            An existing matplotlib axis to draw on. If None, a new figure and axis will be created.
        width : int, optional
            The width of the heatmap figure in inches. Default is 12.
        height : int, optional
            The height of the heatmap figure in inches. Default is 6.

        Returns
        -------
        matplotlib.axes._axes.Axes
            The axis object containing the heatmap.

        Raises
        ------
        ValueError
            If no positions are available or the positions matrix is empty.
        """
        print("Generating weight matrix visualization...")

        # Ensure positions are generated
        if self.strategy.positions is None or self.strategy.positions.empty:
            raise ValueError("No positions available. Ensure `strategy.generate_positions()` has been called.")

        # Convert positions to a g × d matrix
        positions_matrix = self.strategy.get_positions().T.to_numpy()

        # Calculate mean and standard deviation for normalization
        mean = np.nanmean(positions_matrix)
        std = np.nanstd(positions_matrix)

        # Define color limits
        if self.strategy.long_short:
            vmin = mean - 2 * std
            vmax = mean + 2 * std
        else:
            vmin = 0
            vmax = mean + 2 * std

        # Use provided axis or create a new one
        created_new_figure = ax is None
        if ax is None:
            fig, ax = plt.subplots(figsize=(width, height))

        sns.heatmap(
            positions_matrix,
            cmap="coolwarm",
            cbar_kws={"label": "Weight"},
            xticklabels=False,  # Hide x-axis labels
            yticklabels=False,  # Hide y-axis labels
            square=False,       # Allow non-square cells
            vmin=vmin,          # Minimum color value
            vmax=vmax,          # Maximum color value
            ax=ax               # Use the provided axis
        )
        ax.set_title(f"Weight Matrix of {self.strategy.name}", fontsize=16)
        ax.set_xlabel("Dates", fontsize=14)
        ax.set_ylabel("Stocks", fontsize=14)

        # Add grid for improved readability
        ax.grid(alpha=0.3, linestyle="--")

        # Improve layout if a new figure is created
        if ax.get_figure() and ax.get_figure() is not plt.gcf():
            plt.tight_layout()

        return ax

    def compare_strategies(
        self,
        strategies: dict,
        metrics: List[str] = ["correlation", "nav"],
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        include_benchmark: bool = True,
        width: int = 12,
        height: int = 6,
    ) -> None:
        """
        Compare the performance of the current strategy with other strategies based on specified metrics.

        Parameters
        ----------
        strategies : dict
            A dictionary where keys are strategy names and values are either:
            - StrategyClass objects, which will be processed to calculate NAVs.
            - Precomputed NAVs (pd.Series).
        metrics : List[str]
            List of metrics to compare. Options include:
            - "correlation" (signal correlation)
            - "excess_returns" (bar plot of mean excess returns)
            - "return" (annualized return)
            - "volatility" (annualized volatility)
            - "sharpe_ratio" (Sharpe ratio)
            - "nav" (compare NAVs in a single plot)
            - "matshow" (weight matrix visualization)
            - "binplot" (bin plot visualization)
        start_date : Optional[int], optional
            The start date for the comparison in YYYYMMDD format. Default is None.
            If None, uses `self.start_date`.
        end_date : Optional[int], optional
            The end date for the comparison in YYYYMMDD format. Default is None.
            If None, uses `self.end_date`.
        include_benchmark : bool, optional
            Whether to include the benchmark NAV in the comparison. Default is True.
        width : int, optional
            Width of the plot. Default is 12.
        height : int, optional
            Height of the plot. Default is 6.

        Returns
        -------
        None
        """
        print("Comparing strategies...")

        # Use self's start_date and end_date if not provided
        start_date = start_date or self.start_date
        end_date = end_date or self.end_date

        # Ensure the current strategy NAV is available
        if self.nav is None:
            self.calculate_nav()

        # Filter NAV and signals for the given date range
        def filter_by_date(data, start_date, end_date):
            """Filter data by start_date and end_date."""
            return data[(data.index >= pd.to_datetime(str(start_date), format="%Y%m%d")) &
                        (data.index <= pd.to_datetime(str(end_date), format="%Y%m%d"))]

        strategy_nav = filter_by_date(self.nav, start_date, end_date)
        navs = {"Current Strategy": strategy_nav}
        signals = {"Current Strategy": self.strategy.get_positions().stack().values}

        for name, strategy in strategies.items():
            if isinstance(strategy, StrategyClass):
                # Prepare strategy data
                strategy.fetch_data(data_class=self.data_class, required_factors=strategy.factor_library.factors)
                strategy.generate_positions()

                # Initialize BackTestClass for the strategy
                backtest = BackTestClass(
                    strategy=strategy,
                    data_class=self.data_class,
                    start_date=start_date,
                    end_date=end_date,
                    lag=self.lag,
                )
                navs[name] = filter_by_date(backtest.calculate_nav(), start_date, end_date)
                signals[name] = strategy.get_positions().stack().values
            elif isinstance(strategy, pd.Series):
                navs[name] = filter_by_date(strategy, start_date, end_date)
            else:
                raise ValueError(f"Unsupported strategy type for {name}.")

        # Process and visualize each metric
        for metric in metrics:
            if metric == "nav":
                # Plot NAV comparison
                print("NAV Comparison...")
                plt.figure(figsize=(width, height))
                for name, nav in navs.items():
                    plt.plot(nav, label=name, linewidth=2.5)
                plt.legend()
                plt.title("Net Asset Value (NAV)", fontsize=14, weight="bold")
                plt.ylabel("Cumulative NAV")
                plt.xlabel("Date")
                plt.grid(alpha=0.5)
                plt.tight_layout()
                plt.show()

            elif metric == "correlation":
                # Plot correlation matrix using sns.pairplot for daily returns
                print("Correlation Matrix for Daily Returns...")

                # Prepare daily return data for pairplot
                return_frames = []
                for name, nav in navs.items():
                    # Calculate daily log returns
                    daily_returns = np.log(nav / nav.shift(1)).dropna()
                    daily_returns_df = pd.DataFrame(daily_returns, columns=[name])
                    return_frames.append(daily_returns_df)

                # Combine daily returns into a single DataFrame, aligning by time index
                combined_daily_returns = pd.concat(return_frames, axis=1).dropna()

                if combined_daily_returns.empty:
                    print("No overlapping daily returns found for correlation analysis.")
                else:
                    # Use sns.pairplot to visualize pairwise relationships
                    pairplot_fig = sns.pairplot(
                        combined_daily_returns,
                        diag_kind="kde",            # Kernel density estimation on diagonals
                        plot_kws={"alpha": 0.7},    # Set transparency for scatter plots
                        corner=True,                # Display only lower triangle
                    )
                    pairplot_fig.fig.suptitle(
                        "Daily Return Correlation Matrix",
                        y=1.02, fontsize=16, weight="bold"
                    )
                    plt.show()

            elif metric == "excess_returns":
                # Plot mean excess returns
                print("Excess Returns Comparison...")
                if self.benchmark_returns is None:
                    self.calculate_benchmark_returns()

                excess_returns_data = {
                    name: nav.pct_change().mean() - self.benchmark_returns.mean()
                    for name, nav in navs.items()
                }
                plt.figure(figsize=(width, height))
                sns.barplot(x=list(excess_returns_data.keys()), y=list(excess_returns_data.values()), palette="mako")
                plt.title("Mean Excess Returns", fontsize=14, weight="bold")
                plt.ylabel("Excess Return")
                plt.xlabel("Strategy")
                plt.grid(alpha=0.5)
                plt.tight_layout()
                plt.show()

            elif metric == "return":
                # Plot annualized return
                print("Annualized Return Comparison...")
                annualized_return_data = {
                    name: ((1 + nav.pct_change().mean()) ** 252) - 1 for name, nav in navs.items()
                }
                plt.figure(figsize=(width, height))
                sns.barplot(x=list(annualized_return_data.keys()), y=list(annualized_return_data.values()), palette="mako")
                plt.title("Annualized Return", fontsize=14, weight="bold")
                plt.ylabel("Return")
                plt.xlabel("Strategy")
                plt.grid(alpha=0.5)
                plt.tight_layout()
                plt.show()

            elif metric == "volatility":
                # Plot annualized volatility
                print("Annualized Volatility Comparison...")
                volatility_data = {
                    name: nav.pct_change().std() * (252 ** 0.5) for name, nav in navs.items()
                }
                plt.figure(figsize=(width, height))
                sns.barplot(x=list(volatility_data.keys()), y=list(volatility_data.values()), palette="mako")
                plt.title("Annualized Volatility", fontsize=14, weight="bold")
                plt.ylabel("Volatility")
                plt.xlabel("Strategy")
                plt.grid(alpha=0.5)
                plt.tight_layout()
                plt.show()

            elif metric == "sharpe_ratio":
                # Plot Sharpe ratio
                print("Sharpe Ratio Comparison...")
                sharpe_ratio_data = {
                    name: (nav.pct_change().mean() - 0.02 / 252) / (nav.pct_change().std() * (252 ** 0.5))
                    for name, nav in navs.items()
                }
                plt.figure(figsize=(width, height))
                sns.barplot(x=list(sharpe_ratio_data.keys()), y=list(sharpe_ratio_data.values()), palette="mako")
                plt.title("Sharpe Ratio", fontsize=14, weight="bold")
                plt.ylabel("Sharpe Ratio")
                plt.xlabel("Strategy")
                plt.grid(alpha=0.5)
                plt.tight_layout()
                plt.show()

            elif metric == "matshow":
                # Matshow visualization
                print("Weight Matrix Visualization...")
                fig, axes = plt.subplots(
                    nrows=1,
                    ncols=len(navs),
                    figsize=(width * len(navs), height),
                    constrained_layout=True,
                )
                if len(navs) == 1:
                    axes = [axes]  # Ensure axes is iterable for a single strategy
                for idx, (name, nav) in enumerate(navs.items()):
                    if name == "Current Strategy":
                        self.matshow(ax=axes[idx])
                    else:
                        strategy_backtest = BackTestClass(
                            strategy=strategies[name],
                            data_class=self.data_class,
                            start_date=start_date,
                            end_date=end_date,
                            lag=self.lag,
                        )
                        strategy_backtest.matshow(ax=axes[idx])
                    axes[idx].set_title(f"Weight Matrix of {name}", fontsize=14, weight="bold")
                plt.show()

            elif metric == "binplot":
                # Binplot visualization
                print("Binplot Visualization...")
                fig, axes = plt.subplots(
                    nrows=1,
                    ncols=len(navs),
                    figsize=(width * len(navs), height),
                    constrained_layout=True,
                )
                if len(navs) == 1:
                    axes = [axes]  # Ensure axes is iterable for a single strategy
                for idx, (name, nav) in enumerate(navs.items()):
                    if name == "Current Strategy":
                        self.plot_binplot(ax=axes[idx])
                    else:
                        strategy_backtest = BackTestClass(
                            strategy=strategies[name],
                            data_class=self.data_class,
                            start_date=start_date,
                            end_date=end_date,
                            lag=self.lag,
                        )
                        strategy_backtest.plot_binplot(ax=axes[idx])
                    axes[idx].set_title(f"Binplot of {name}", fontsize=14, weight="bold")
                plt.show()

            else:
                print(f"Metric {metric} is not supported.")

    def create_strategies_dropdown(self, additional_strategies=None):
        """
        Create a dropdown widget to select strategies dynamically.

        Parameters
        ----------
        additional_strategies : dict, optional
            A dictionary of additional strategies to include in the dropdown. Keys
            are strategy names, and values are either StrategyClass objects or precomputed NAVs.

        Returns
        -------
        widgets.SelectMultiple
            A dropdown widget populated with available strategies.
        """

        # Add self.strategy
        available_strategies = {"Current Strategy": self.strategy}

        # Merge with additional strategies if provided
        if additional_strategies:
            available_strategies.update(additional_strategies)

        # Generate the widget
        self.strategies_dropdown = widgets.SelectMultiple(
            options=list(available_strategies.keys()),
            value=["Current Strategy"],  # Default selection
            description="Strategies",
        )

        # Store available strategies for later use
        self.available_strategies = available_strategies

        return self.strategies_dropdown

    def analyze_strategy_interact(self, width=16, height=6):
        """
        Interactively analyze the performance of the current strategy.

        This function provides a user-friendly interface to explore the 
        performance of the current strategy using various metrics.

        Parameters
        ----------
        width : int, optional
            The width of the generated plots. Default is 16.
        height : int, optional
            The height of the generated plots. Default is 6.

        Returns
        -------
        None
            Displays interactive widgets for strategy analysis.

        Notes
        -----
        - The interactive widget allows users to select multiple metrics to analyze.
        - Metrics include NAV, weight matrix visualization, bin plots, 
        and key performance metrics like annualized return, volatility, 
        max drawdown, and Sharpe ratio.

        Examples
        --------
        
        >>> backtest = BackTestClass(strategy=my_strategy, data_class=data, start_date=20200101, end_date=20231231)
        >>> backtest.analyze_strategy_interact()
        # This will display an interactive widget for selecting metrics and analyzing the strategy.
        """
        # Dropdown and inputs for user interaction
        metrics_dropdown = widgets.SelectMultiple(
            options=[
                "nav", 
                "matshow", 
                "binplot", 
                "annualized_return", 
                "annualized_volatility", 
                "max_drawdown", 
                "sharpe_ratio"
            ],
            value=["nav"],  # Default selected metric
            description="Metrics",  # Label for the dropdown
        )
        start_date_input = widgets.IntText(
            placeholder="YYYYMMDD",  # Example date format
            description="Start Date",  # Label for the input
            value=self.start_date  # Default to the strategy's start date
        )
        end_date_input = widgets.IntText(
            placeholder="YYYYMMDD",  # Example date format
            description="End Date",  # Label for the input
            value=self.end_date  # Default to the strategy's end date
        )

        # Button to trigger analysis and output display
        analyze_button = widgets.Button(description="Analyze Current Strategy")
        analysis_output = widgets.Output()

        # Define behavior for the "Analyze" button
        def on_analyze_clicked(b):
            with analysis_output:
                # Clear previous output
                analysis_output.clear_output()
                # Fetch user-selected metrics and date range
                selected_metrics = metrics_dropdown.value
                start_date = start_date_input.value
                end_date = end_date_input.value

                print(f"Analyzing current strategy...")
                print(f"Selected metrics: {selected_metrics}")
                print(f"Start Date: {start_date}, End Date: {end_date}")

                # Analyze and visualize each selected metric
                for metric in selected_metrics:
                    try:
                        if metric == "nav":
                            print("NAV Analysis:")
                            self.plot_nav(include_benchmark=True, width=width, height=height)
                        elif metric == "matshow":
                            print("Weight Matrix Visualization:")
                            self.matshow(width=width, height=height)
                        elif metric == "binplot":
                            print("Binplot Visualization:")
                            self.plot_binplot(width=width, height=height)
                        elif metric == "annualized_return":
                            print("Annualized Return Analysis:")
                            annualized_return = self.calculate_annualized_return()
                            print(annualized_return.tail())  # Display last few entries
                        elif metric == "annualized_volatility":
                            print("Annualized Volatility Analysis:")
                            volatility = self.calculate_annualized_volatility()
                            print(volatility.tail())  # Display last few entries
                        elif metric == "max_drawdown":
                            print("Max Drawdown Analysis:")
                            max_drawdown = self.calculate_max_drawdown()
                            print(max_drawdown.tail())  # Display last few entries
                        elif metric == "sharpe_ratio":
                            print("Sharpe Ratio Analysis:")
                            sharpe_ratio = self.calculate_sharpe_ratio()
                            print(sharpe_ratio.tail())  # Display last few entries
                        else:
                            print(f"Metric {metric} is not supported for single analysis.")
                    except Exception as e:
                        print(f"Error during {metric} analysis: {e}")

        # Link the "Analyze" button to the behavior
        analyze_button.on_click(on_analyze_clicked)

        # Display the interactive widgets and output area
        display(
            widgets.VBox([
                widgets.Label("Select metrics for analysis:"),  # Instructional label
                metrics_dropdown,  # Dropdown for metrics
                start_date_input,  # Input for start date
                end_date_input,  # Input for end date
                analyze_button,  # Button to trigger analysis
                analysis_output,  # Output area for results
            ])
        )

    def compare_strategies_interact(self, additional_strategies=None, width=12, height=6):
        """
        Interactively compare the performance of multiple strategies.

        This function creates an interactive widget-based interface for users 
        to compare the performance of different investment strategies.

        Parameters
        ----------
        additional_strategies : dict, optional
            Additional strategies to compare, passed as a dictionary with
            strategy names as keys and `StrategyClass` objects as values.
        width : int, optional
            Width of the plots. Default is 12.
        height : int, optional
            Height of the plots. Default is 6.

        Returns
        -------
        None
            Displays the interactive interface for strategy comparison.

        Notes
        -----
        - Allows the user to select strategies and metrics to compare.
        - Supports interactive input for the date range (start and end date).
        - Comparison results include various metrics like NAV, correlation, and excess returns.

        Examples
        --------
        
        >>> backtest.compare_strategies_interact({
        ...     "Momentum Strategy": momentum_strategy,
        ...     "Reversal Strategy": reversal_strategy,
        ... })
        # This will display an interactive widget to compare the strategies.
        """
        # Dropdown to select strategies
        strategies_dropdown = self.create_strategies_dropdown(additional_strategies=additional_strategies)

        # Dropdown to select metrics for comparison
        metrics_dropdown = widgets.SelectMultiple(
            options=[
                "correlation", 
                "excess_returns", 
                "return", 
                "volatility", 
                "nav", 
                "matshow", 
                "binplot"
            ],
            value=["nav"],  # Default selected metric
            description="Metrics",
        )

        # Input fields for start and end dates
        start_date_input = widgets.IntText(
            placeholder="YYYYMMDD",
            description="Start Date",
            value=self.start_date
        )
        end_date_input = widgets.IntText(
            placeholder="YYYYMMDD",
            description="End Date",
            value=self.end_date
        )

        # Button to trigger the comparison
        compare_button = widgets.Button(description="Compare Strategies")

        # Output area to display results
        comparison_output = widgets.Output()

        # Ensure only one event handler is linked to the button
        if hasattr(self, "_compare_button_click_handler"):
            compare_button.on_click(self._compare_button_click_handler, remove=True)

        # Define behavior for the button click event
        def on_compare_clicked(b):
            with comparison_output:
                # Clear previous output
                comparison_output.clear_output()

                # Retrieve selected strategies and metrics
                selected_strategies = strategies_dropdown.value
                selected_metrics = metrics_dropdown.value
                start_date = start_date_input.value
                end_date = end_date_input.value

                # Inform the user about the progress
                print(f"Comparing strategies...")
                print(f"Selected strategies: {selected_strategies}")
                print(f"Selected metrics: {selected_metrics}")
                print(f"Date range: {start_date} to {end_date}")

                # Extract strategies for comparison
                comparison_strategies = {
                    name: self.available_strategies.get(name, None)
                    for name in selected_strategies
                    if name != "Current Strategy"
                }

                # Perform the comparison and handle errors
                try:
                    self.compare_strategies(
                        strategies=comparison_strategies,
                        metrics=selected_metrics,
                        start_date=start_date,
                        end_date=end_date,
                    )
                except Exception as e:
                    print(f"Error during comparison: {e}")

        # Link the button to the behavior
        compare_button.on_click(on_compare_clicked)
        self._compare_button_click_handler = on_compare_clicked

        # Display the interactive widget
        display(
            widgets.VBox([
                widgets.Label("Select strategies and metrics for comparison:"),
                strategies_dropdown,
                metrics_dropdown,
                start_date_input,
                end_date_input,
                compare_button,
                comparison_output,
            ])
        )

    def __repr__(self):
        """
        Provide a string representation of the BackTestClass instance.

        This method returns a summary of key attributes such as the strategy name,
        initial capital, lag, and benchmark, making it easier to understand
        the configuration of the backtest at a glance.

        Returns
        -------
        str
            A string representation of the BackTestClass instance.
        """
        return (
            f"BackTestClass(strategy={self.strategy.name}, "
            f"initial_capital={self.initial_capital}, lag={self.lag}, "
            f"benchmark={self.benchmark})"
        )

    def check_nav_jumps(self, threshold: float = 0.1):
        """
        Identify large jumps in the net asset value (NAV) and their causes.

        Parameters
        ----------
        threshold : float
            The percentage threshold to flag NAV jumps. Default is 0.1 (10%).

        Returns
        -------
        pd.DataFrame
            A DataFrame with dates, NAV values, and their changes for flagged jumps.
        """
        if self.nav is None:
            self.calculate_nav()

        # Calculate the relative NAV changes
        nav_diff = self.nav.diff()
        nav_relative_change = nav_diff / self.nav.shift(1)

        # Flag large jumps
        jumps = nav_relative_change[abs(nav_relative_change) > threshold]

        # Create a summary DataFrame
        jumps_df = pd.DataFrame({
            "date": jumps.index,
            "nav": self.nav[jumps.index],
            "change": nav_relative_change[jumps.index]
        })

        return jumps_df.sort_values(by="change", key=abs, ascending=False) 