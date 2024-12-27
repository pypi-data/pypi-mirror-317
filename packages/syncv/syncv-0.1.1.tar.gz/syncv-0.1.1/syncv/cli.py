import click
from syncv.core import initialize, list_contents, clear_contents, bind_device, start_service, get_binded_peers

@click.group()
def main():
    """ Sync Clipboard Tool"""
    pass

@main.command()
def init():
    """ init """
    code = initialize()
    if code.startswith('Already'):
        click.echo(code)
    else:
        click.echo(f'Initilization complete. Your unique code is: {code}')

@main.command()
@click.argument('code')
def bind(code):
    """ bind between os """
    success = bind_device(code)
    if success:
        click.echo('OS binded')
    else:
        click.echo('Failed to bind')

@main.command()
def binded_list():
    """ list binded """
    peers = get_binded_peers()
    for idx, peer in enumerate(peers):
        click.echo(f'{idx}: {peer}')

@main.command
def start():
    """ start the service """
    start_service()
    click.echo('service started...')

@main.command()
def list():
    """ list all """
    contents = list_contents()
    for idx, cv in enumerate(contents):
        click.echo(f'{idx}: {cv}')

@main.command()
def clear():
    """ clear all """
    clear_contents()
    click.echo('cv history removed.')

if __name__ == '__main__':
    main()