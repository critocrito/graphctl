__version__ = "0.1.0"

from dotenv import load_dotenv
from .cli import cli


def main():
    load_dotenv()

    cli()
