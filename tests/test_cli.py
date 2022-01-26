from pathlib import Path
from difflib import unified_diff
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
    stdout_strlist = result.stdout.splitlines(keepends=True)
    expect_strlist = []
    with TEST_SCHEMA_FILE_SCHEMA.open() as fd:
        expect_str = fd.read()
        expect_strlist = expect_str.splitlines(keepends=True)
    diff = unified_diff(expect_strlist,
                        stdout_strlist,
                        fromfile=str(TEST_SCHEMA_FILE_SCHEMA),
                        tofile='stdout')
    diff_str = ''.join(diff)
    assert not diff_str, diff_str


def test_cli_fileout_success(tmp_path):
    runner = CliRunner()
    output_filepath = Path(tmp_path, 'test.schema')
    result = runner.invoke(cli, [str(TEST_SCHEMA_FILE_LDIF), "-o", str(output_filepath)])
    assert result.exit_code == 0
    output_strlist = []
    with output_filepath.open() as fd:
        output_str = fd.read()
        output_strlist = output_str.splitlines(keepends=True)
    expect_strlist = []
    with TEST_SCHEMA_FILE_SCHEMA.open() as fd:
        expect_str = fd.read()
        expect_strlist = expect_str.splitlines(keepends=True)
    diff = unified_diff(expect_strlist,
                        output_strlist,
                        fromfile=str(TEST_SCHEMA_FILE_SCHEMA),
                        tofile=str(output_filepath))
    diff_str = ''.join(diff)
    assert not diff_str, diff_str
