import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, TextIO, Union

from openldap_schema_parser.schema import Schema


class BaseHandler(ABC):
    @abstractmethod
    def read(self, filepath: Union[str, Path]) -> Schema:
        pass

    @abstractmethod
    def get_prity_lines(self, schema_data: Schema) -> List[str]:
        pass

    def _write_fd(self, schema_data: Schema, fd: TextIO) -> None:
        lines = self.get_prity_lines(schema_data)
        for line in lines:
            fd.write(f"{line}\n")

    def write(self, schema_data: Schema, filepath: Union[str, Path]) -> None:
        p = Path(filepath)
        with p.open("w") as fd:
            self._write_fd(schema_data, fd)

    def output(self, schema_data: Schema) -> None:
        self._write_fd(schema_data, sys.stdout)
