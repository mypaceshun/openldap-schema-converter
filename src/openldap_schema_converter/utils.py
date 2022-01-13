from pathlib import Path
from textwrap import wrap
from typing import Union

from ldif import LDIFParser


def load_schema_file(targetfile: Union[str, Path]) -> list:
    targetpath: Path = Path(targetfile)
    if targetpath.suffix == ".ldif":
        return load_schema_file_ldif(targetfile)
    else:
        return []


def load_schema_file_ldif(targetfile: Union[str, Path]) -> list:
    targetpath: Path = Path(targetfile)
    res: list[tuple[str, dict]] = []
    with targetpath.open("rb") as fd:
        parser = LDIFParser(fd)
        for dn, attrs in parser.parse():
            res.append((dn, attrs))
    return res


def print_schema_data(schema_data: list) -> None:
    res_text = schema_data_convert(schema_data)
    print("\n\n".join(res_text))


def write_schema_data(schema_data: list, outfile: Union[str, Path]) -> None:
    res_text = schema_data_convert(schema_data)
    outpath = Path(outfile)
    with outpath.open("w") as fd:
        fd.write("\n\n".join(res_text))


def schema_data_convert(schema_data: list) -> list[str]:
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


def parse_attribute_types(attribute_types: list[str]) -> list[str]:
    res_text = []
    for attr_type in attribute_types:
        pattr_type = prity_text(attr_type)
        res_text.append(f"attributeType {pattr_type}")
    return res_text


def parse_objecct_classes(object_classes: list[str]) -> list[str]:
    res_text = []
    for object_cls in object_classes:
        pobject_cls = prity_text(object_cls)
        res_text.append(f"objectClass {pobject_cls}")
    return res_text
