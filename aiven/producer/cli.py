"""
The command line interface to the Meter application
"""

import click
import logging
from aiven.producer.main import main


DEFAULT_TOPIC = 'webmetrics'
DEFAULT_FREQ = 5  # in seconds
DEFAULT_WEBSITE = 'http://www.example.com/'


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

@click.command()
@click.option(
    "--kafka", "-k", required=True, help="Full address and credentials to the kafka service"
)
@click.option(
    "--topic", "-t", default=DEFAULT_TOPIC, help="Name of the topic"
)
@click.option(
    "--website", "-w", default=DEFAULT_WEBSITE, help="The website to check"
)
@click.option(
    "--freq", "-f", default=DEFAULT_FREQ, help="Frequency of checks (s)"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Log at debug level"
)
def cli(kafka, topic, website, freq, verbose):
    if verbose:
        log.setLevel(logging.INFO)
    main(kafka, topic, website, freq)


if __name__ == '__main__':
    cli()
