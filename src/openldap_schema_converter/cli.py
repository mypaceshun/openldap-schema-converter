import click

from openldap_schema_converter import __name__, __version__
from openldap_schema_converter.converter import FORMAT
from openldap_schema_converter.utils import load_file, print_data, write_data


@click.command()
@click.version_option(version=__version__, package_name=__name__)
@click.help_option("-h", "--help")
@click.option("-o", "--outfile", help="output filename")
@click.option(
    "--input-type", type=click.Choice(list(FORMAT)), help="Select input file format"
)
@click.option(
    "-t",
    "--output-type",
    type=click.Choice(list(FORMAT)),
    help="Select output format",
)
@click.argument("targetfile", type=click.Path(exists=True), required=True)
def cli(outfile, input_type, output_type, targetfile):
    schema_data = load_file(targetfile)
    if outfile is None:
        print_data(schema_data)
    else:
        write_data(schema_data, outfile)
