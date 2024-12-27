# PyBotTrader


PyBotTrader is an experimental Python library designed to help create trading
bots, particularly for retail traders. It offers tools for real-time financial
analysis, including indicators like moving averages (like MA, EMA, RSI, MACD, and
ROI), which update dynamically with new data. The library includes data streamers
to handle sequential data from sources like CSV files or the YFinance API, and
basic portfolio managers for back-testing simple buy/sell strategies. Users can
define custom strategies that integrate data streams, indicators, and
decision-making rules to generate trading signals. A basic trader module is
included for testing strategies, making the library a versatile framework for
algorithmic trading experimentation.

## Example

Using this library looks like:

``` python
from pybottrader.indicators import RSI
from pybottrader.datastreamers.yfinance import YFHistory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.strategies import Strategy, Position, StrategySignal
from pybottrader.traders import Trader


class SimpleRSIStrategy(Strategy):
    """A simple strategy based on the RSI indicator"""

    rsi: RSI
    last_flip = Position.SELL
    lower_band: float
    upper_band: float

    def __init__(self, lower_band=30.0, upper_band=70.0):
        self.rsi = RSI()
        self.lower_band = lower_band
        self.upper_band = upper_band

    def evaluate(self, data) -> StrategySignal:
        # default positio STAY
        position = Position.STAY
        # Update the RSI indicator
        self.rsi.update(open_price=data["open"], close_price=data["close"])
        # Make the decision what position to advice
        if self.last_flip == Position.SELL and self.rsi[0] < self.lower_band:
            position = Position.BUY
            self.last_flip = Position.BUY
        elif self.last_flip == Position.BUY and self.rsi[0] > self.upper_band:
            position = Position.SELL
            self.last_flip = Position.SELL
        return StrategySignal(time=data["time"], price=data["close"], position=position)


# Apple, daily data from 2021 to 2023
datastream = YFHistory("AAPL", start="2021-01-01", end="2023-12-31")
# Start with USD 1,000
portfolio = DummyPortfolio(1000.0)
# My strategy
strategy = SimpleRSIStrategy(lower_band=25.0, upper_band=75.0)

# Putting everything together
trader = Trader(strategy, portfolio, datastream)
# A default runner, but you can implement your own loop
trader.run()
```

Output is shown below.

```
Time                      Pos.      Price        ROI   Valuation  Accum.ROI
2021-02-11 00:00:00-05:00 BUY      132.34       0.00%    1000.00       0.00%
2021-06-21 00:00:00-04:00 SELL     129.78      -1.93%     980.72      -1.93%
2021-09-20 00:00:00-04:00 BUY      140.43       0.00%     980.72      -1.93%
2021-10-22 00:00:00-04:00 SELL     146.08       4.02%    1020.17       2.02%
2022-05-24 00:00:00-04:00 BUY      138.48       0.00%    1020.17       2.02%
2022-07-08 00:00:00-04:00 SELL     145.07       4.76%    1068.72       6.87%
2022-09-02 00:00:00-04:00 BUY      153.93       0.00%    1068.72       6.87%
2023-01-24 00:00:00-05:00 SELL     141.05      -8.37%     979.26      -2.07%
2023-08-07 00:00:00-04:00 BUY      177.50       0.00%     979.26      -2.07%
2023-10-12 00:00:00-04:00 SELL     179.59       1.18%     990.78      -0.92%
```

## Installation

```sh
pip install git+https://github.com/jailop/pybottrader.git
```

Shortly, I'm going to release more documentation and more examples.

## Installation Requirements

### Linux
- GCC/G++ compiler
- CMake 3.15 or higher
- Python development headers (python3-dev)

### Windows
- Visual Studio 2019 or later with C++ build tools
- CMake 3.15 or higher
- Windows SDK

### macOS
- Xcode Command Line Tools
- CMake 3.15 or higher

