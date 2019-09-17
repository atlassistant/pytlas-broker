# pylint: disable=missing-docstring

import os
import click
from pytlas.cli import install_logs, SKILLS_DIR, WATCH
from pytlas.settings import CONFIG
from pytlas.handling.importers import import_skills
from pytlas_broker.communicating.mqtt import MQTTChannel
from pytlas_broker.conversing import Server
from pytlas_broker.conversing.agents import FromFile
from pytlas_broker.__about__ import __version__


@click.group()
@click.version_option(__version__)
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('--debug', is_flag=True, help='Debug mode')
def main(verbose, debug):
    """The broker exposes a pytlas instance to the outside world on multiple channels.
    """
    install_logs(verbose, debug)


@main.command()
@click.argument('data_dir', type=click.Path(), required=True)
def serve(data_dir):
    """Starts the server.
    """
    agents_factory = FromFile(data_dir)

    # Let's load the configuration and load the skills
    CONFIG.load_from_file(agents_factory._default_conf_path) # pylint: disable=protected-access
    import_skills(CONFIG.getpath(SKILLS_DIR, os.path.join(data_dir, 'skills')),
                  CONFIG.getbool(WATCH))

    server = Server(agents_factory)

    with MQTTChannel() as mqtt:
        mqtt.attach(server)
        input()


if __name__ == '__main__':
    main(True, True)
