from pathlib import Path
from typing import Dict, List, Tuple, Union

from ldif import LDIFParser
from openldap_schema_parser.schema import Schema

from openldap_schema_converter.handler.base import BaseHandler

DN = str
ATTRS = Dict[str, List[str]]


class LdifHandler(BaseHandler):
    def read(self, readfile: Union[Path, str]) -> Schema:
        print("LdifHandler read")
        readpath = Path(readfile)
        ldifdata: List[Tuple[DN, ATTRS]] = []
        with readpath.open("rb") as fd:
            parser = LDIFParser(fd)
            for dn, attrs in parser.parse():
                ldifdata.append((dn, attrs))

        return self.ldif2schema(*ldifdata[0])

    def get_prity_lines(self, schema_data: Schema) -> List[str]:
        print("LdifHandler write")
        return [""]

    def ldif2schema(self, dn: DN, attrs: ATTRS) -> Schema:
        name = dn.split(",")[0].split("=")[1]
        return Schema(name)
