# pylint: disable=C0111

import logging
from pytlas_broker.communicating.messages import Message


class Channel:
    """Represents a transport layer for messages.
    """

    def __init__(self, name) -> None:
        self._name = name
        self._logger = logging.getLogger(self._name)
        self._handlers = []

    def __enter__(self) -> None:
        self.open()
        return self

    def __exit__(self, type, value, traceback) -> None: # pylint: disable=W0622
        return self.close()

    def attach(self, *models) -> None:
        """Attach one or more models which will receive messages received by this
        channel.

        So basically when a raw message will be received, it will be parsed by the
        channel and a method matching `on_<message_class_name>` will be triggered
        on the given model and will have the current channel and the parsed
        message as arguments.

        Args:
            models (list of any): Models which will receive parsed messages.

        """
        for model in models:
            self._handlers.append(model)

    def detach(self, *models) -> None:
        """Detach one or more previously added models from this channel. They will
        not received any messages from this channel.

        Args:
            models (list of any): Models previously registered.

        """
        for model in models:
            try:
                self._handlers.remove(model)
            except ValueError:
                self._logger.warning('"%s" does not exists in the channel handlers', model)

    def receive(self, message: Message) -> None:
        """Sends the given message to each attached models. a method matching
        `on_<message_class_name>` will be triggered and will have the current
        channel and the parsed message as arguments.

        Args:
            message (Message): Message received.

        """
        for handler in self._handlers:
            attr_name = f'on_{message.__class__.__name__.lower()}'
            attr = getattr(handler, attr_name, None)

            if attr:
                self._logger.debug('Calling "%s.%s"', handler, attr_name)
                attr(self, message)
            else:
                self._logger.debug('Could not find "%s" on handler "%s", skipping',
                                   attr_name, handler)

    def send(self, message: Message) -> None:
        """Sends a message on this channel, implementation specific.

        Args:
          message (Message): Message to send

        """
        pass # pragma: no cover pylint: disable=W0107

    def open(self) -> None:
        """Open the channel, implementation specific.
        """
        pass # pragma: no cover pylint: disable=W0107

    def close(self) -> None:
        """Close the current channel, implementation specific.
        """
        pass # pragma: no cover pylint: disable=W0107
