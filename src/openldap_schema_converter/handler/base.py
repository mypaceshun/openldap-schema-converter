import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TextIO, Union

from openldap_schema_parser.schema import Schema


class BaseHandler(ABC):
    @abstractmethod
    def read(self, filepath: Union[str, Path]) -> Schema:
        pass

    @abstractmethod
    def write_fd(self, schema_data: Schema, fd: TextIO) -> None:
        pass

    def write(self, schema_data: Schema, filepath: Union[str, Path]) -> None:
        p = Path(filepath)
        with p.open() as fd:
            self.write_fd(schema_data, fd)

    def print(self, schema_data: Schema) -> None:
        self.write_fd(schema_data, sys.stdout)
