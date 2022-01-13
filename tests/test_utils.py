from pathlib import Path

from openldap_schema_converter.utils import (
    load_schema_file,
    print_schema_data,
    write_schema_data,
)

TEST_BASE_DIR = Path(__file__).parent
TEST_SCHEMA_FILE_LDIF = Path(TEST_BASE_DIR, "schema/ldif/test.ldif")
TEST_SCHEMA_FILE_SCHEMA = Path(TEST_BASE_DIR, "schema/schema/test.schema")


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


class TestPrintSchemaData:
    def test_print_schema_data(self):
        schema_data = [("cn=schema", {"cn": "schema"})]
        print_schema_data(schema_data)


class TestWriteSchemaData:
    def test_write_schema_data(self, tmpdir):
        schema_data = [("cn=schema", {"cn": "schema"})]
        outfile = Path(tmpdir, "test.schema")
        write_schema_data(schema_data, outfile)
