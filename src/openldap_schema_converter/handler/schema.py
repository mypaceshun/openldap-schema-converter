from pathlib import Path
from textwrap import TextWrapper
from typing import List, Optional, Union

from openldap_schema_parser.attribute import ATTRIBUTE_USAGE
from openldap_schema_parser.objectclass import STRUCTURAL_TYPE
from openldap_schema_parser.parser import parse
from openldap_schema_parser.schema import Schema

from openldap_schema_converter.handler.base import BaseHandler


class SchemaHandler(BaseHandler):
    def __init__(self):
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
        print("SchemaHandler read")
        return parse(str(readfile))

    def get_prity_lines(self, schema_data: Schema) -> List[str]:
        print("SchemaHandler write")
        lines: List[str] = []

        lines += self.get_prity_lines_objectidentifier(schema_data)

        lines += self.get_prity_lines_attributetype(schema_data)

        lines += self.get_prity_lines_objectclass(schema_data)
        if len(lines) == 0:
            return lines
        if len(lines[-1]) == 0:
            del lines[-1]
        return lines

    def get_prity_lines_objectidentifier(self, schema_data: Schema) -> List[str]:
        lines: List[str] = []
        for objectidentifier in schema_data.objectidentifier_list:
            id = "objectIdentifier"
            key = objectidentifier.key
            oid = objectidentifier.oid
            lines.append(f"{id}{self.whsp}{key}{self.whsp}{oid}")
        if len(lines) > 0:
            lines.append("")
        return lines

    def get_prity_lines_attributetype(
        self,
        schema_data: Schema,
    ) -> List[str]:
        lines: List[str] = []
        for attributetype in schema_data.attribute_list:
            id = "attributeType"
            lines.append(f"{id}{self.whsp}{self.left}{self.whsp}{attributetype.oid}")
            self._line_add_name(
                lines,
                attributetype.name,
                attributetype.alias,
            )
            if isinstance(attributetype.description, str):
                value = self.quote + attributetype.description + self.quote
                lines.append(self._get_line_key_value("DESC", value))
            self._line_add_key_flag(lines, "OBSOLETE", attributetype.obsolete)
            self._line_add_key_value(lines, "SUP", attributetype.sup)
            self._line_add_key_value(lines, "EQUALITY", attributetype.equality)
            self._line_add_key_value(lines, "ORDERING", attributetype.ordering)
            self._line_add_key_value(lines, "SUBSTR", attributetype.substr)
            self._line_add_key_value(lines, "SYNTAX", attributetype.syntax)
            self._line_add_key_flag(
                lines,
                "SINGLE-VALUE",
                attributetype.single_value,
            )
            self._line_add_key_flag(lines, "COLLECTIVE", attributetype.collective)
            self._line_add_key_flag(
                lines,
                "NO-USER-MODIFICATION",
                attributetype.no_user_modification,
            )
            if isinstance(attributetype.usage, ATTRIBUTE_USAGE):
                self._line_add_key_value(lines, "USAGE", str(attributetype.usage))
            lines[-1] = f"{lines[-1]}{self.whsp}{self.right}"
            lines.append("")

        return lines

    def get_prity_lines_objectclass(
        self,
        schema_data: Schema,
    ) -> List[str]:
        lines: List[str] = []
        for objectclass in schema_data.objectclass_list:
            id = "objectClass"
            lines.append(f"{id}{self.whsp}{self.left}{self.whsp}{objectclass.oid}")
            self._line_add_name(lines, objectclass.name, objectclass.alias)
            self._line_add_description(lines, objectclass.description)
            self._line_add_key_flag(lines, "OBSOLETE", objectclass.obsolete)
            self._line_add_key_value(lines, "SUP", objectclass.sup)
            if isinstance(objectclass.structural_type, STRUCTURAL_TYPE):
                self._line_add_key_flag(lines, str(objectclass.structural_type))
            self._line_add_may(lines, objectclass.may)
            self._line_add_must(lines, objectclass.must)
            lines.append("")
        return lines

    def _line_add_name(
        self,
        lines: List[str],
        name: Optional[str],
        alias: Optional[List[str]],
    ) -> List[str]:
        if name is None:
            return lines
        value = self.quote + name + self.quote
        if alias is not None:
            names = [name] + alias
            items = (
                [self.left]
                + [f"{self.quote}{name}{self.quote}" for name in names]
                + [self.right]
            )
            value = self.whsp.join(items)
        lines.append(self._get_line_key_value("NAME", value))
        return lines

    def _line_add_description(
        self,
        lines: List[str],
        description: str = None,
    ) -> List[str]:
        if description is None:
            return lines
        value = self.quote + description + self.quote
        return self._line_add_key_value(lines, "DESC", value)

    def _line_add_may(self, lines: List[str], may: List[str]) -> List[str]:
        if len(may) == 0:
            return lines
        if len(may) == 1:
            return self._line_add_key_value(lines, "MAY", may[0])
        attrs = f"$${self.whsp}".join(may)
        value = self.whsp.join([self.left, attrs, self.right])
        line = self._get_line_key_value("MAY", value)
        line = line.replace("$$", f"{self.whsp}$")
        lines.append(line)
        return lines

    def _line_add_must(self, lines: List[str], must: List[str]) -> List[str]:
        if len(must) == 0:
            return lines
        if len(must) == 1:
            return self._line_add_key_value(lines, "MUST", must[0])
        attrs = f"$${self.whsp}".join(must)
        value = self.whsp.join([self.left, attrs, self.right])
        line = self._get_line_key_value("MUST", value)
        line = line.replace("$$", f"{self.whsp}$")
        lines.append(line)
        return lines

    def _line_add_key_flag(
        self, lines: List[str], key: str, flag: bool = True
    ) -> List[str]:
        if flag:
            lines.append(self._get_line_key_value(key, None))
        return lines

    def _line_add_key_value(
        self,
        lines: List[str],
        key: str,
        value: str = None,
    ) -> List[str]:
        if value is None:
            return lines
        lines.append(self._get_line_key_value(key, value))
        return lines

    def _get_line_key_value(self, key: str, value: str = None) -> str:
        if value is None:
            return self.wrapper.fill(key)
        return self.wrapper.fill(f"{key}{self.whsp}{value}")
