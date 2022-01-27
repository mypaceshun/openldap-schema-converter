from pathlib import Path

from openldap_schema_converter.utils import (
    load_schema_file,
    load_schema_file_ldif,
    print_schema_data,
    write_schema_data,
)

from . import TEST_SCHEMA_FILE_LDIF, TEST_SCHEMA_FILE_SCHEMA


class TestLoadSchemaFile:
    def test_load_schema_file_ldif(self):
        result = load_schema_file(TEST_SCHEMA_FILE_LDIF)
        assert len(result) == 1
        dn, attrs = result[0]
        assert dn == "cn=testschema,cn=schema,cn=config"
        assert attrs["objectClass"] == ["olcSchemaConfig"]

    def test_load_schema_file_error(self):
        result = load_schema_file("no_exists_filename")
        assert result == []

    def test_load_schema_file_schema(self):
        result = load_schema_file(TEST_SCHEMA_FILE_SCHEMA)
        assert result == []


class TestLoadSchemaFileLdif:
    def test_load_schema_file_ldif_success(self):
        result = load_schema_file_ldif(TEST_SCHEMA_FILE_LDIF)
        assert len(result) == 1
        dn, attrs = result[0]
        assert dn == "cn=testschema,cn=schema,cn=config"
        assert attrs["objectClass"] == ["olcSchemaConfig"]

    def test_load_schema_file_no_exists(self):
        result = load_schema_file_ldif("no_exists_filename")
        assert result == []

    def test_load_schema_file_not_ldif(self):
        result = load_schema_file_ldif(TEST_SCHEMA_FILE_SCHEMA)
        assert result == []


class TestPrintSchemaData:
    def test_print_schema_data_empty(self, capsys):
        schema_data = [("cn=schema", {"cn": "schema"})]
        print_schema_data(schema_data)
        captured = capsys.readouterr()
        assert captured.out == "\n"


class TestWriteSchemaData:
    def test_write_schema_data(self, tmpdir):
        schema_data = [("cn=schema", {"cn": "schema"})]
        outfile = Path(tmpdir, "test.schema")
        write_schema_data(schema_data, outfile)
