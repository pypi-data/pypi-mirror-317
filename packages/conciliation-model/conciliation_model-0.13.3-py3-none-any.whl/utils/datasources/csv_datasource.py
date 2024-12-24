from typing import Any, Generator, Literal, Sequence

import pandas as pd
from pandas._typing import ReadCsvBuffer

from utils.datasources.abc_datasource import DataSource, Frame


class CsvFrame(Frame):

    def __init__(self, df: pd.DataFrame, name: str | int) -> None:
        self.name = str(name)
        self._df = df

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def records(self) -> Generator[dict[str, Any], Any, None]:
        for _, row in self.df.iterrows():
            yield row.to_dict()


class CsvDatasource(DataSource):
    def __init__(
        self,
        csv_file: ReadCsvBuffer[bytes],
        header: int | Sequence[int] | Literal["infer"] | None = ...,  # type: ignore
    ) -> None:
        super().__init__()
        self._csv_file = csv_file
        self._header = header
        self._csv_df = pd.read_csv(
            filepath_or_buffer=self._csv_file,
            header=self._header,  # type: ignore
        )

    @property
    def frames(self) -> Generator[CsvFrame, Any, None]:
        yield from self._get_frames()

    def _get_frames(self) -> Generator[CsvFrame, Any, None]:
        yield CsvFrame(self._csv_df, "csv")

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._csv_df
