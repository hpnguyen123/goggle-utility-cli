import os
import click
import json
import csv
from shutil import copyfile
from .cli_context import pass_context
from .helpers import get_stdin


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--verbose', '-v', is_flag=True, help='Print output verbose')
@pass_context
def cli(ctx, verbose):
    pass


@cli.command()
@pass_context
@click.argument('client-secret-file')
def init(ctx, client_secret_file):
    """ Invoke authentication workflow and get a the access token
    """
    assert os.path.exists(client_secret_file)
    copyfile(client_secret_file, ctx.client_secret)

    creds = ctx.get_credentials()
    click.echo(creds.to_json())


@cli.command('get')
@pass_context
@click.argument('sheets-id')
@click.argument('values-range')
def sheets_get(ctx, sheets_id, values_range):
    """ Invoke authentication workflow and get a the access token
    """
    assert sheets_id, values_range

    sheets = ctx.get_service('sheets').spreadsheets()
    results = sheets.values().get(spreadsheetId=sheets_id, range=values_range).execute()
    click.echo(json.dumps(results))


@cli.command('update')
@pass_context
@click.argument('sheets-id')
@click.argument('values-range')
def sheets_update(ctx, sheets_id, values_range):
    """ Update sheets range with input data
    """
    assert sheets_id, values_range
    sheets = ctx.get_service('sheets').spreadsheets()
    values = get_stdin()

    body = {
        'values': values
    }

    results = sheets.values().update(
        spreadsheetId=sheets_id,
        range=values_range,
        valueInputOption="RAW",
        body=body).execute()

    click.echo(json.dumps(results))


@cli.command('show')
@click.argument('property')
@pass_context
def show(ctx, property):
    """ Show the configuration property
    """
    click.echo(ctx.__dict__[property])


@cli.command()
@pass_context
def test(ctx):
    """ Invoke authentication workflow and get a the access token
    """
    pass


def main():

    # auth.get_credentials('credentials.json', 'client_secret.json')
    cli()
    pass


if __name__ == "__main__":
    cli()
