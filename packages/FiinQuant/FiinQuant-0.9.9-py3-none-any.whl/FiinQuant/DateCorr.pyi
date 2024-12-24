from typing import Union
class FindDateCorrelation(object):
    def __init__(self, access_token: str) -> None: ...
    
    def intraday_Prediction(self, Tickers: Union[str, list], Timeframe: str, 
                            t1: str = None, t2: str = None, method: str = "pearson correlation",
                            year: int = 1, field=['C'], adjusted=True) -> None:
        self.field: list [str]
        self.adjusted: bool
