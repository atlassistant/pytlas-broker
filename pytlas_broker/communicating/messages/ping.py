# pylint: disable=C0111,W0235

from pytlas_broker.communicating.messages.message import Message


class Ping(Message):
    """Represents a ping message.
    """

    def __init__(self, device_identifier: str, user_identifier: str) -> None:
        """Instantiates a new message for the given client.

        Args:
          device_identifier (str): Unique device identifier for which this message
            has been generated.
          user_identifier (str): Unique identifier representing the subject.

        """
        super().__init__(device_identifier, user_identifier)
