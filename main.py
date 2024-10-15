import click
import duckdb

from pprint import pformat

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):

    conn = duckdb.connect(':memory:')
    conn.execute('INSTALL spatial')
    conn.execute('LOAD spatial')

    ctx.obj = conn

@cli.command()
@click.argument('FILE', nargs=1)
@click.pass_context
def dump(ctx, file):
    '''Dump contents of XLS file'''

    conn = ctx.obj
    conn.execute('''
        CREATE TABLE xls AS
            SELECT * FROM st_read(?)
    ''', (file,))

    result = conn.execute('SELECT * FROM xls')

    click.echo(pformat(result.fetchall()))

if __name__ == '__main__':
    cli()
