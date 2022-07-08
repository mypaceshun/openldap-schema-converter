from enum import Enum
from pathlib import Path
from typing import Union

from openldap_schema_parser.schema import Schema

from openldap_schema_converter.handler.base import BaseHandler
from openldap_schema_converter.handler.json import JsonHandler
from openldap_schema_converter.handler.ldif import LdifHandler
from openldap_schema_converter.handler.schema import SchemaHandler


class HANDLER_TYPE(str, Enum):
    LDIF = "ldif"
    SCHEMA = "schema"
    JSON = "json"


def get_handler(handler_type: HANDLER_TYPE) -> BaseHandler:
    if handler_type == HANDLER_TYPE.SCHEMA:
        return SchemaHandler()
    elif handler_type == HANDLER_TYPE.JSON:
        return JsonHandler()
    return LdifHandler()


def suffix2handler(filepath: Union[str, Path]) -> HANDLER_TYPE:
    p = Path(filepath)
    suffix = p.suffix
    if suffix == ".schema":
        return HANDLER_TYPE.SCHEMA
    elif suffix == ".ldif":
        return HANDLER_TYPE.LDIF
    elif suffix == ".json":
        return HANDLER_TYPE.JSON
    return HANDLER_TYPE.SCHEMA


def read(readfile: Union[Path, str], handler_type: HANDLER_TYPE = None) -> Schema:
    if handler_type is None:
        handler_type = suffix2handler(readfile)
    handler = get_handler(handler_type)
    return handler.read(readfile)


def write(
    schema_obj: Schema, outfile: Union[Path, str], handler_type: HANDLER_TYPE = None
) -> None:
    if handler_type is None:
        handler_type = suffix2handler(outfile)
    handler = get_handler(handler_type)
    return handler.write(schema_obj, outfile)


def output(
    schema_obj: Schema, handler_type: HANDLER_TYPE = HANDLER_TYPE.SCHEMA
) -> None:
    handler = get_handler(handler_type)
    return handler.output(schema_obj)
