from .Trading_Data_Stream import Trading_Data_Stream
from .Fetch_Trading_Data import Fetch_Trading_Data
from datetime import datetime 
from .FiinIndicator import _FiinIndicator
from typing import Union
from .DateCorr import FindDateCorrelation
from .Rebalance import VN30Rebalance
class FiinSession:
    def __init__(self, username: str, password: str):...

    def login(self) -> FiinSession: ...
   
    def FiinIndicator(self) -> _FiinIndicator: ...
    
    def Trading_Data_Stream(self, 
                        tickers: list, 
                        callback: callable) -> Trading_Data_Stream: ...
    # """Using this class to stream real-time stock market matching data """
    
    def Fetch_Trading_Data(self,
                 realtime: bool,
                 tickers: list, 
                 fields:list, 
                 adjusted: bool, 
                 period:Union[int, None] = None, 
                 by:str = '1M',
                 from_date: Union[str, datetime, None] = None,
                 to_date: Union[str, datetime, None] = None,
                 callback: callable = None,
                 wait_for_full_timeFrame: bool = False) -> Fetch_Trading_Data: ...

    def FindDateCorrelation (self) -> FindDateCorrelation: ...

    def VN30Rebalance(self) -> VN30Rebalance: ...




