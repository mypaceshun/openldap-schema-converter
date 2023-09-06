from pathlib import Path
from textwrap import TextWrapper
from typing import List, Optional, Union

from openldap_schema_parser.attribute import ATTRIBUTE_USAGE, Attribute
from openldap_schema_parser.objectclass import STRUCTURAL_TYPE, ObjectClass
from openldap_schema_parser.parser import parse
from openldap_schema_parser.schema import Schema

from openldap_schema_converter.handler.base import BaseHandler


class SchemaHandler(BaseHandler):
    def __init__(self):
        self.wrap = True
        self.max_width = 80
        self.whsp = " "
        self.indent = self.whsp * 4
        self.left = "("
        self.right = ")"
        self.quote = "'"
        self.wrapper = TextWrapper(
            width=self.max_width,
            initial_indent=self.indent,
            subsequent_indent=self.indent * 2,
        )

    def read(self, readfile: Union[Path, str]) -> Schema:
        return parse(str(readfile))

    def get_prity_lines(self, schema_data: Schema) -> List[str]:
        lines: List[str] = []
        pstr = schema_data.pprint_str(width=self.max_width)
        lines = pstr.splitlines()
        if len(lines) > 0 and len(lines[-1]) == 0:
            del lines[-1]
        return lines

    def get_prity_lines_objectidentifier(self, schema_data: Schema) -> List[str]:
        lines: List[str] = []
        for objectidentifier in schema_data.objectidentifier_list:
            pstr = objectidentifier.pprint_str(width=self.max_width)
            lines.append(pstr)
        if len(lines) > 0:
            lines.append("")
        return lines

    def get_prity_lines_attributetype(
        self,
        schema_data: Schema,
    ) -> List[str]:
        lines: List[str] = []
        for attributetype in schema_data.attribute_list:
            lines += self.get_prity_lines_attributetype_one(attributetype)
        return lines

    def get_prity_lines_attributetype_one(self, attributetype: Attribute):
        lines: List[str] = []
        pstr = attributetype.pprint_str(width=self.max_width)
        lines = pstr.splitlines()
        return lines

    def get_prity_lines_objectclass(
        self,
        schema_data: Schema,
    ) -> List[str]:
        lines: List[str] = []
        for objectclass in schema_data.objectclass_list:
            lines += self.get_prity_lines_objectclass_one(objectclass)
        return lines

    def get_prity_lines_objectclass_one(self, objectclass: ObjectClass) -> List[str]:
        lines: List[str] = []
        pstr = objectclass.pprint_str(width=self.max_width)
        lines = pstr.splitlines()
        return lines
