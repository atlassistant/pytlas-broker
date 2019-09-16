# pylint: disable=missing-docstring

import os
from configparser import ConfigParser
from typing import Dict, Tuple
from pytlas import Agent
from pytlas.understanding.snips import SnipsInterpreter
from pytlas.settings import SettingsStore, to_env_key
from pytlas_broker.conversing.agents.factory import Factory

def get_config_directories_path(base_path: str, uid: str) -> Tuple[str, str]:
    """Retrieve directories path used by the FromFileFactory.

    Args:
        base_path (str): Base directory
        uid (str): Unique identifier

    Returns:
        (str, str): Cache directory and configuration path

    """
    return (
        os.path.abspath(os.path.join(base_path, uid, 'cache')),
        os.path.abspath(os.path.join(base_path, uid, 'pytlas.ini'))
    )

def env_from_configparser(config: ConfigParser) -> Dict[str, str]:
    """Convert a ConfigParser instance to a dictionary which will be used by an
    agent settings and take precedence over the global ones.

    Args:
        config (ConfigParser): Instance to flatten

    Returns:
        dict: Env dictionary

    """
    result = {}
    for section in config.sections():
        result.update({to_env_key(section, k): v for k, v in config.items(section)})
    return result

class FromFileFactory(Factory): # pylint: disable=too-few-public-methods
    """Defines a factory which will create an agent by reading user specific
    .ini files.
    """

    def __init__(self, directory: str) -> None:
        """Instantiates a new factory by providing a directory which will contain
        user data. The directory should follow this structure:

        directory/
            default/ <-- Default configuration, used when could not find the user one
                cache/ <-- Will be created by the interpreter
                pytlas.ini
            john/ <-- Your user
                pytlas.ini <-- Will override the default configuration

        Args:
            directory (str): Path containing user data

        """
        super().__init__('file')
        self._directory = directory
        # Let's read the default configuration right now
        self._default_cache_dir, default_conf_path = \
            get_config_directories_path(self._directory, 'default')
        settings = SettingsStore()
        settings.load_from_file(default_conf_path)
        self._default_settings = env_from_configparser(settings.config)


    def create(self, uid: str) -> Agent:
        cache_dir, conf_path = get_config_directories_path(self._directory, uid)
        settings = self._default_settings.copy()

        if os.path.isfile(conf_path):
            store = SettingsStore()
            store.load_from_file(conf_path)
            settings.update(env_from_configparser(store.config))
        else:
            cache_dir = self._default_cache_dir
            self._logger.warning('Could not find a pytlas.ini file in "%s", using the default one',
                                 conf_path)

        interpreter = SnipsInterpreter(settings.get(to_env_key('pytlas', 'language'), 'en'),
                                       cache_directory=cache_dir)
        interpreter.fit_from_skill_data()
        return Agent(interpreter, **settings)
