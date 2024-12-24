import click


@click.group()
def cli():
    """
    Main CLI group that serves as the entry point for all commands.
    """
    pass


if __name__ == "__main__":
    from endpoints.cli import *

    cli()
