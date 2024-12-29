import click
from .bot import run

@click.command()
def run_ai():
    """Run the AI."""
    run()

if __name__ == '__main__':
    run_ai()
