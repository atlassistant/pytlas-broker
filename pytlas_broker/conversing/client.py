# pylint: disable=missing-module-docstring

import logging
from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Message


class Client:
    """Tiny client used to communicate with a broker server instance.

    It represents a single device which wants to send and receive message to and
    from the broker.
    """

    def __init__(self, device_identifier: str, channel: Channel):
        self._logger = logging.getLogger('client')
        self._device_identifier = device_identifier
        self._channel = channel
        self._channel.attach(self) # Attach to the channel right away

    def accept_message(self, msg: Message):
        """Determine if this client accepts an incoming message.
        """
        return msg.device_identifier == self._device_identifier

    def parse(self, message: str, user_identifier: str, **meta):
        pass
