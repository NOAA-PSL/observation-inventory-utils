import click

@click.group()
def cli():
    """Cli for observations Inventory."""

@cli.command()
def hello_world():
    click.echo('Hello World!')
    
