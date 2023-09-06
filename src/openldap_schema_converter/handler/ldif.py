import re
from pathlib import Path
from textwrap import TextWrapper
from typing import Dict, List, Tuple, Union

from ldif import LDIFParser
from openldap_schema_parser.parser import parse_str
from openldap_schema_parser.schema import Schema

from openldap_schema_converter.handler.base import BaseHandler
from openldap_schema_converter.handler.schema import SchemaHandler

DN = str
ATTRS = Dict[str, List[str]]


class LdifHandler(BaseHandler):
    def __init__(self):
        self.wrap = True
        self.schema_handler = SchemaHandler()
        self.schema_handler.wrap = False
        self.whsp = " "
        self.wrapper = TextWrapper(width=80, subsequent_indent=self.whsp * 2)

    def read(self, readfile: Union[Path, str]) -> Schema:
        readpath = Path(readfile)
        ldifdata: List[Tuple[DN, ATTRS]] = []
        with readpath.open("rb") as fd:
            parser = LDIFParser(fd)
            for dn, attrs in parser.parse():
                ldifdata.append((dn, attrs))
        # あまりないが、1つのLDIFに複数のエントリが定義されていた場合、
        # 1つめのエントリしか認識できない。
        return self.ldif2schema(*ldifdata[0])

    def get_prity_lines(self, schema_data: Schema) -> List[str]:
        lines: List[str] = []
        lines.append(f"dn: cn={schema_data.name},cn=schema,cn=config")
        lines.append(f"cn: {schema_data.name}")
        lines.append("objectClass: olcSchemaConfig")
        lines += self.get_lines_objectidentifier(schema_data)
        lines += self.get_lines_attributetype(schema_data)
        lines += self.get_lines_objectclass(schema_data)
        return lines

    def ldif2schema(self, dn: DN, attrs: ATTRS) -> Schema:
        _name = dn.split(",")[0].split("=")[1]
        # _name = "{0}core"
        name = self.lines2str([_name])
        schema_text = ""
        schema_text += self._ldif2schema(
            attrs, "olcObjectIdentifier", "objectIdentifier"
        )
        schema_text += self._ldif2schema(attrs, "olcAttributeTypes", "attributeType")
        schema_text += self._ldif2schema(attrs, "olcObjectClasses", "objectClass")
        return parse_str(schema_text, name)

    def _ldif2schema(self, attrs: ATTRS, key: str, prefix: str):
        vars = attrs.get(key, [])
        schema_text = self.lines2str(vars)
        schema_text = self.add_prefix(schema_text, prefix)
        return schema_text

    def lines2str(self, lines: List[str]) -> str:
        """
        {n}xxx という文字列のリストをnの値を行数とし、一つの文字列に結合する。

        例:
        {0}abc
        {2}012
        {1}xyz

        -> abc
           xyz
           012
        """
        Line = Tuple[int, str]
        no_match_lines: List[Line] = []
        match_lines: List[Line] = []
        pattern = re.compile(r"\{(\d+)\}(.*)")
        for line in lines:
            m = pattern.match(line)
            if m:
                num = m.group(1)
                _line = m.group(2)
                match_lines.append((int(num), _line))
            else:
                no_match_lines.append((-1, line))
        match_lines = sorted(match_lines, key=lambda line: line[0])
        result_lines = [line[1] for line in match_lines] + [
            line[1] for line in no_match_lines
        ]
        return "\n".join(result_lines)

    def add_prefix(self, text: str, prefix: str) -> str:
        """
        各行にプレフィックスをつける
        (1.1.1.1.1) となっているものを attributeType(1.1.1.1.1)とするため
        """
        if len(text) == 0:
            return text
        new_lines = []
        for line in text.split("\n"):
            new_lines.append(f"{prefix}{line}")
        return "\n".join(new_lines)

    def get_lines_objectidentifier(self, schema_data: Schema) -> List[str]:
        key = "olcObjectIdentifier"
        lines: List[str] = []
        for objectidentifier in schema_data.objectidentifier_list:
            lines.append(f"{key}: {objectidentifier.key} {objectidentifier.oid}")

        return lines

    def get_lines_attributetype(self, schema_data: Schema) -> List[str]:
        key = "olcAttributeTypes"
        lines: List[str] = []
        for attribute in schema_data.attribute_list:
            _lines = self.schema_handler.get_prity_lines_attributetype_one(attribute)
            text = self.whsp.join(_lines)
            text = text.replace("attributeType", f"{key}:", 1)
            if self.wrap:
                lines.append(self.wrapper.fill(text))
            else:
                lines.append(text)
        return lines

    def get_lines_objectclass(self, schema_data: Schema) -> List[str]:
        key = "olcObjectClasses"
        lines: List[str] = []
        for objectclass in schema_data.objectclass_list:
            _lines = self.schema_handler.get_prity_lines_objectclass_one(objectclass)
            text = self.whsp.join(_lines)
            text = text.replace("objectClass", f"{key}:", 1)
            if self.wrap:
                lines.append(self.wrapper.fill(text))
            else:
                lines.append(text)
        return lines
