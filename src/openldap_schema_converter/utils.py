import re
import sys
from pathlib import Path
from textwrap import wrap
from typing import List, Union

from ldif import LDIFParser


def load_schema_file(targetfile: Union[str, Path]) -> List:
    targetpath: Path = Path(targetfile)
    if targetpath.suffix == ".ldif":
        return load_schema_file_ldif(targetfile)
    else:
        return []


def load_schema_file_ldif(targetfile: Union[str, Path]) -> List:
    targetpath: Path = Path(targetfile)
    res: list[tuple[str, dict]] = []
    try:
        with targetpath.open("rb") as fd:
            parser = LDIFParser(fd)
            for dn, attrs in parser.parse():
                res.append((dn, attrs))
    except Exception as error:
        print(error, file=sys.stdout)
    return res


def print_schema_data(schema_data: List) -> None:
    res_text = schema_data_convert(schema_data)
    print("\n\n".join(res_text))


def write_schema_data(schema_data: List, outfile: Union[str, Path]) -> None:
    res_text = schema_data_convert(schema_data)
    outpath = Path(outfile)
    with outpath.open("w") as fd:
        fd.write("\n\n".join(res_text))
        fd.write("\n")


def schema_data_convert(schema_data: List) -> List[str]:
    res_text = []
    for dn, attrs in schema_data:
        if "objectClass" not in attrs:
            continue
        if "olcSchemaConfig" not in attrs["objectClass"]:
            continue
        attribute_types = attrs.get("olcAttributeTypes", [])
        object_classes = attrs.get("olcObjectClasses", [])
        res_text += parse_attribute_types(attribute_types)
        res_text += parse_objecct_classes(object_classes)
    return res_text


def prity_text(value: str) -> str:
    sepalator = "\n    "
    keywords = [
        "NAME",
        "DESC",
        "EQUALITY",
        "SUBSTR",
        "SYNTAX",
        "X-ORIGIN",
        "SUP",
        "AUXILIARY",
        "MAY",
        "MUST",
    ]
    for keyword in keywords:
        value = value.replace(keyword, f"{sepalator}{keyword}")
    text_list = []
    for line in value.split("\n"):
        _line = sepalator.join(wrap(line))
        text_list.append(_line)
    return "\n".join(text_list)


def parse_attribute_types(attribute_types: List[str]) -> List[str]:
    res_text = []
    for attr_type in attribute_types:
        _attr_type = re.sub(r"\{[0-9]*\}", "", attr_type, 1)
        pattr_type = prity_text(_attr_type)
        res_text.append(f"attributeType {pattr_type}")
    return res_text


def parse_objecct_classes(object_classes: List[str]) -> List[str]:
    res_text = []
    for object_cls in object_classes:
        _object_cls = re.sub(r"\{[0-9]*\}", "", object_cls, 1)
        pobject_cls = prity_text(_object_cls)
        res_text.append(f"objectClass {pobject_cls}")
    return res_text
