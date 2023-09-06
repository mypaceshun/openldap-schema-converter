from difflib import unified_diff
from pathlib import Path

from click.testing import CliRunner

from openldap_schema_converter.cli import cli

from . import TEST_SCHEMA_FILE_LDIF, TEST_SCHEMA_FILE_SCHEMA


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_cli_stdout_success():
    runner = CliRunner()
    result = runner.invoke(cli, [str(TEST_SCHEMA_FILE_LDIF)])
    assert result.exit_code == 0


def test_cli_fileout_success(tmp_path):
    runner = CliRunner()
    output_filepath = Path(tmp_path, "test.schema")
    result = runner.invoke(
        cli, [str(TEST_SCHEMA_FILE_LDIF), "-o", str(output_filepath)]
    )
    assert result.exit_code == 0
