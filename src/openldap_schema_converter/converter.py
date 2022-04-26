from enum import Enum


class FORMAT(str, Enum):
    SCHEMA = "schema"
    LDIF = "ldif"
    JSON = "json"
