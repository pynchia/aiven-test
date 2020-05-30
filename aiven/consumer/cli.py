"""
The command line interface to the Consumer application
"""

import click
import logging
from aiven.consumer.main import main


DEFAULT_TOPIC = 'webmetrics'


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
    "--db-uri", "-d", required=True, help="Full address and credentials to the postgreSQL service"
)
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Log at debug level"
)
def cli(kafka_uri, topic, db_uri, verbose):
    if verbose:
        log.setLevel(logging.INFO)
    main(kafka_uri, topic, db_uri)


if __name__ == '__main__':
    cli()
