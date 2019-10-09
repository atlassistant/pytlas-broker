# pylint: disable=missing-module-docstring

import logging
from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Message, Parse, Ask, Answer, Context, \
    Done, Thinking


class Client:
    """Tiny client used to communicate with a broker server instance.

    It represents a single device which wants to send and receive message to and
    from the broker.
    """

    def __init__(self, device_identifier: str, channel: Channel) -> None:
        self._logger = logging.getLogger('client')
        self._device_identifier = device_identifier
        self._channel = channel
        self._channel.attach(self) # Attach to the channel right away

    def accept_message(self, msg: Message) -> bool:
        """Determine if this client accepts an incoming message.
        """
        return msg.device_identifier == self._device_identifier

    def parse(self, message: str, user_identifier: str, **meta) -> None:
        """Sends a parse message to the remote broker.
        """
        self._channel.send(Parse(self._device_identifier, user_identifier, message, **meta))

    def on_ask(self, channel: Channel, message: Ask) -> None: # pylint: disable=missing-function-docstring
        pass

    def on_answer(self, channel: Channel, message: Answer) -> None: # pylint: disable=missing-function-docstring
        pass

    def on_context(self, channel: Channel, message: Context) -> None: # pylint: disable=missing-function-docstring
        pass

    def on_done(self, channel: Channel, message: Done) -> None: # pylint: disable=missing-function-docstring
        pass

    def on_thinking(self, channel: Channel, message: Thinking) -> None: # pylint: disable=missing-function-docstring
        pass
