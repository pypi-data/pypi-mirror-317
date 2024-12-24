class Trading_Data_Stream:
    """Using this class to stream real-time stock market matching data. """
    def __init__(self,tickers: list, callback: callable) -> None:
        self.tickers: list
        self._stop: bool
        
    def start(self) -> None: ...
        
    def stop(self) -> None: ...

