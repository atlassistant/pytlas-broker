# pylint: disable=C0111

from pytlas_broker.communicating.messages.message import Message


class Parse(Message):
    """Represents a parse message.
    """

    def __init__(self, device_identifier: str, user_identifier: str, text: str, **meta) -> None:
        """Instantiates a new message for the given client.

        Args:
          device_identifier (str): Unique device identifier for which this message
            has been generated.
          user_identifier (str): Unique identifier representing the subject.
          text (str): Answer text
          meta (dict): any metadata related to this answer

        """
        super().__init__(device_identifier, user_identifier)

        self.text = text
        self.meta = meta
