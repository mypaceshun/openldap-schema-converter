from pathlib import Path
from typing import List, Union

from openldap_schema_parser.schema import Schema

from openldap_schema_converter.handler.base import BaseHandler


class JsonHandler(BaseHandler):
    def read(self, readfile: Union[Path, str]) -> Schema:
        print("JsonHandler read")
        return Schema(name="test")

    def get_prity_lines(self, schema_data: Schema) -> List[str]:
        return [""]
