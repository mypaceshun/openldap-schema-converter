import click

from openldap_schema_converter import __name__, __version__
from openldap_schema_converter.handler import HANDLER_TYPE, output, read, write

# from openldap_schema_converter.converter import FORMAT
# from openldap_schema_converter.utils import load_file, print_data, write_data


@click.command()
@click.version_option(version=__version__, package_name=__name__)
@click.help_option("-h", "--help")
@click.option("-o", "--outfile", help="output filename")
@click.option(
    "--input-type",
    type=click.Choice(list(HANDLER_TYPE)),
    help="Select input file format",
)
@click.option(
    "-t",
    "--output-type",
    type=click.Choice(list(HANDLER_TYPE)),
    help="Select output format",
)
@click.argument("targetfile", type=click.Path(exists=True), required=True)
def cli(outfile, input_type, output_type, targetfile):
    schema_data = read(targetfile, handler_type=input_type)
    if schema_data is None:
        print("schema data empty!")
    if outfile is None:
        output(schema_data, handler_type=output_type)
    else:
        write(schema_data, outfile, handler_type=output_type)
