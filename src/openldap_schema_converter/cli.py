import click

from openldap_schema_converter import (
    load_schema_file,
    print_schema_data,
    write_schema_data,
)


@click.command()
@click.option("-o", "--outfile", help="output filename")
@click.argument("targetfile", type=click.Path(exists=True), required=True)
def cli(outfile, targetfile):
    schema_data = load_schema_file(targetfile)
    if outfile is None:
        print_schema_data(schema_data)
    else:
        write_schema_data(schema_data, outfile)
