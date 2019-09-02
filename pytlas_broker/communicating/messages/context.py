# pylint: disable=C0111

from pytlas_broker.communicating.messages.message import Message


class Context(Message):
    """Represents a context message.
    """

    def __init__(self, device_identifier: str, user_identifier: str, context: str) -> None:
        """Instantiates a new message for the given client.

        Args:
          device_identifier (str): Unique device identifier for which this message
            has been generated.
          user_identifier (str): Unique identifier representing the subject.
          context (str): Name of the new active context

        """
        super().__init__(device_identifier, user_identifier)

        self.context = context
