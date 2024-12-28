import click

@click.group()
def infrakit():
    """Infrakit CLI - Simplified Infrastructure Management."""
    pass

@infrakit.command()
def setup():
    """Set up your infrastructure."""
    click.echo("Setting up your infrastructure...")

if __name__ == "__main__":
    infrakit()