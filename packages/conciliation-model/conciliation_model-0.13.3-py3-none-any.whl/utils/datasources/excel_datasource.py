from typing import Any, Generator, Optional

import pandas as pd
from pandas._typing import ReadBuffer

from utils.datasources.abc_datasource import DataSource, Frame


class Sheet(Frame):

    def __init__(
        self, name: str | int, file_path: str | ReadBuffer[bytes], header_row: int = 0
    ) -> None:
        self.name = str(name)
        self._df = None
        self._file_path = file_path
        self.header_row = header_row
        self.attributes = self.df.dtypes.to_dict()

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            self._df: Optional[pd.DataFrame] = pd.read_excel(
                self._file_path, sheet_name=self.name, header=self.header_row
            )
        return self._df

    @property
    def records(self) -> Generator[dict[str, Any], Any, None]:
        for _, row in self.df.iterrows():
            yield row.to_dict()


class ExcelDataSource(DataSource):
    def __init__(self, file_path: str | ReadBuffer[bytes], header_row: int) -> None:
        self._file_path = file_path
        self._header_row = header_row

    @property
    def frames(self) -> Generator[Sheet, Any, None]:
        yield from self._get_frames()

    def _get_frames(self) -> Generator[Sheet, Any, None]:
        with pd.ExcelFile(self._file_path) as xls:
            for sheet_name in xls.sheet_names:
                yield Sheet(sheet_name, self._file_path, self._header_row)

    def set_header_row(self, header_row: int):
        self._header_row = header_row
