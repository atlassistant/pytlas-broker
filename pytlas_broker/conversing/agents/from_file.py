# pylint: disable=missing-module-docstring

import os
from typing import Tuple
from pytlas import Agent
from pytlas.understanding.snips import SnipsInterpreter
from pytlas.settings import SettingsStore, to_env_key, DEFAULT_SECTION
from pytlas_broker.conversing.agents.factory import Factory


DEFAULT_LANGUAGE = 'en'
LANGUAGE_KEY = 'language'
CACHE_DIR = 'cache'
CONF_FILENAME = 'pytlas.ini'


def get_config_directories_path(base_path: str, uid: str) -> Tuple[str, str]:
    """Retrieve directories path used by the FromFileFactory.

    Args:
        base_path (str): Base directory
        uid (str): Unique identifier

    Returns:
        (str, str): Cache directory and configuration path

    """
    return (
        os.path.abspath(os.path.join(base_path, uid, CACHE_DIR)),
        os.path.abspath(os.path.join(base_path, uid, CONF_FILENAME))
    )


class FromFile(Factory): # pylint: disable=too-few-public-methods
    """Defines a factory which will create an agent by reading user specific
    .ini files.
    """

    def __init__(self, directory: str, fallback_folder='default') -> None:
        """Instantiates a new factory by providing a directory which will contain
        user data. The directory should follow this structure:

        directory/
            default/ <-- Default directory when it could not find the user one
                cache/ <-- Will be created by the interpreter
                pytlas.ini <-- Must be loaded manually inside the global CONFIG
            john/ <-- Your user
                pytlas.ini <-- Will override the default configuration

        Args:
            directory (str): Path containing user data
            fallback_folder (str): Fallback folder name inside directory when
                managing unknown users

        """
        super().__init__('file')
        self._directory = directory
        self._default_cache_dir, self._default_conf_path = \
            get_config_directories_path(self._directory, fallback_folder)

    def create(self, uid: str) -> Agent:
        cache_dir, conf_path = get_config_directories_path(self._directory, uid)
        meta = {}

        if os.path.isfile(conf_path):
            store = SettingsStore()
            store.load_from_file(conf_path)
            meta = store.to_dict()
            self._logger.info('Using settings from "%s"', conf_path)
        else:
            cache_dir = self._default_cache_dir
            self._logger.warning('Could not find a pytlas.ini file in "%s", using the default one',
                                 conf_path)

        interpreter = SnipsInterpreter(meta.get(to_env_key(DEFAULT_SECTION, LANGUAGE_KEY),
                                                DEFAULT_LANGUAGE),
                                       cache_directory=cache_dir)
        interpreter.fit_from_skill_data()
        return Agent(interpreter, **meta)
