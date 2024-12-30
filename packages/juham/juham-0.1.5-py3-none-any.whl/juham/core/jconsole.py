from typing import Any
from masterpiece.timeseries import TimeSeries


class JConsole(TimeSeries):
    """Timeseries database that simply dumps the written records to stdout
    solely for testing and debugging purposes."""

    def __init__(self, name: str = "jconsole") -> None:
        super().__init__(name)

    def write(self, point: Any) -> None:
        print(f"Table:{self.database}:  {str(point)}")

    def read(self, point: Any) -> None:
        print(f"Table:{self.database}:  {str(point)}")
