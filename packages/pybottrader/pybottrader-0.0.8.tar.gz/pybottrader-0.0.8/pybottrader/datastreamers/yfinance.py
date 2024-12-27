"""
Data streamear for yfinance
"""

from typing import Union
import pandas as pd
import yfinance
from . import DataStreamer


class YFHistory(DataStreamer):
    """Using Yahoo Finance to retrieve data"""

    index = 0
    data: pd.DataFrame

    def __init__(self, symbol, *args, **kwargs):
        super().__init__()
        ticker = yfinance.Ticker(symbol)
        self.data = ticker.history(*args, **kwargs)
        self.data.columns = [col.lower() for col in self.data.columns]
        self.data.index.names = ["time"]
        self.data.reset_index(inplace=True)

    def next(self) -> Union[dict, None]:
        if self.index >= len(self.data):
            return None
        result = self.data.iloc[self.index].to_dict()
        result["time"] = result["time"].to_pydatetime()
        self.index += 1
        return result
