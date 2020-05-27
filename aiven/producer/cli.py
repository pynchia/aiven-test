"""
The command line interface to the Producer application
"""

import click
import logging
from aiven.producer.main import main


DEFAULT_TOPIC = 'webmetrics'
DEFAULT_WEBSITE = 'http://www.example.com/'
DEFAULT_DELAY = 5  # in seconds
DEFAULT_PATTERN = ''  # match anything


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

@click.command()
@click.option(
    "--kafka-uri", "-k", required=True, help="Full address and credentials to the kafka service"
)
@click.option(
    "--topic", "-t", default=DEFAULT_TOPIC, help="Name of the topic"
)
@click.option(
    "--web-uri", "-w", default=DEFAULT_WEBSITE, help="The website to check"
)
@click.option(
    "--delay", "-d", default=DEFAULT_DELAY, help="Delay between checks (s)"
)
@click.option(
    "--pattern", "-p", default=DEFAULT_PATTERN, help="Pattern to search in page (regex)"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Log at debug level"
)
def cli(kafka_uri, topic, web_uri, delay, pattern, verbose):
    if verbose:
        log.setLevel(logging.INFO)
    main(kafka_uri, topic, web_uri, delay, pattern)


if __name__ == '__main__':
    cli()
