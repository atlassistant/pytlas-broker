# pylint: disable=missing-module-docstring

import os
import click
from pytlas.cli import install_logs, SKILLS_DIR, WATCH
from pytlas.settings import CONFIG
from pytlas.handling.importers import import_skills
from pytlas_broker.cli.repl import ReplClient
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
@click.option('-c', '--config', type=click.Path(), help='Path to a config file')
@click.option('-did', '--device-identifier', default='cli', help='Device identifier to use')
@click.option('-uid', '--user-identifier', default='default', help='User identifier to use')
def repl(config, user_identifier, device_identifier):
    """Starts a client REPL to communicate with a broker instance.
    """
    if config:
        CONFIG.load_from_file(config)

    with MQTTChannel() as mqtt:
        client = ReplClient(device_identifier, user_identifier, mqtt)
        client.cmdloop()

@main.command()
@click.argument('data_dir', type=click.Path(), required=True)
@click.option('--default', type=str, default='default',
              help='Default folder used for unknown user as a fallback (default to "default")')
def serve(data_dir, default):
    """Starts the server.
    """
    agents_factory = FromFile(data_dir, default)

    # Let's load the configuration and load the skills
    CONFIG.load_from_file(agents_factory._default_conf_path) # pylint: disable=protected-access
    import_skills(CONFIG.getpath(SKILLS_DIR, os.path.join(data_dir, 'skills')),
                  CONFIG.getbool(WATCH))

    server = Server(agents_factory)

    with MQTTChannel() as mqtt:
        mqtt.attach(server)
        input('Press any key, anytime to stop the broker')


if __name__ == '__main__':
    main(True, True)
