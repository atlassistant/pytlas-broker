# pylint: disable=C0111

from pytlas_broker.communicating.messages.message import Message


class Done(Message):
    """Represents a done message.
    """

    def __init__(self, device_identifier: str, user_identifier: str, require_input: bool) -> None:
        """Instantiates a new message for the given client.

        Args:
          device_identifier (str): Unique device identifier for which this message
            has been generated.
          user_identifier (str): Unique identifier representing the subject.
          require_input (bool): True if more actions is needed, false otherwise.

        """
        super().__init__(device_identifier, user_identifier)

        self.require_input = require_input
