from click.testing import CliRunner

from openldap_schema_converter.cli import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
