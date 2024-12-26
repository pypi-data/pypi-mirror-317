from abc import ABC, abstractmethod
from typing import Any, Generator, List, Type

from pandas import DataFrame


class Frame:
    name: str
    attributes: dict[str, Type]

    @property
    def records(self) -> Generator[dict[str, Any], None, None]:
        raise NotImplementedError

    @property
    def records_list(self) -> List[dict[str, Any]]:
        return list(self.records)


class DataSource(ABC):
    @property
    @abstractmethod
    def frames(self) -> Generator[Frame, None, None]:
        pass

    @property
    def frames_list(self) -> List[Frame]:
        return list(self.frames)

    @property
    def frames_dict(self) -> dict[str, Frame]:
        return {frame.name: frame for frame in self.frames}

    @property
    def dataframe(self) -> DataFrame:
        return DataFrame(self.dataframe_dict)

    @property
    def dataframe_dict(self) -> dict[str, list[dict[str, Any]]]:
        df_data = dict[str, list[dict[str, Any]]]()
        for frame in self.frames:
            if frame.name not in df_data:
                df_data[frame.name] = []
            for record in frame.records:
                df_data[frame.name].append(record)

        return df_data
