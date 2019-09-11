# pylint: disable=missing-docstring

import logging
from pytlas import Agent


class Factory: # pylint: disable=too-few-public-methods
    """Base class for agents factories which handle agent creation.
    """

    def __init__(self, name):
        self._logger = logging.getLogger(name)

    def create(self, uid: str) -> Agent:
        """Instantiate an agent for the given uid.

        Args:
            uid (str): Unique identifier representing the user

        Returns:
            Agent: Agent trained and ready to accept message to parse

        """
        pass # pylint: disable=unnecessary-pass
