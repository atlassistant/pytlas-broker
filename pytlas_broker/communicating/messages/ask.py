# pylint: disable=C0111,R0913

from pytlas_broker.communicating.messages.message import Message


class Ask(Message):
    """Represents an answer message.
    """

    def __init__(self, device_identifier: str, user_identifier: str, language: str,
                 slot: str, text: str, choices: list, **meta) -> None:
        """Instantiates a new message for the given client.

        Args:
          device_identifier (str): Unique device identifier for which this message
            has been generated.
          user_identifier (str): Unique identifier representing the subject.
          language (str): Agent language
          slot (str): Slot needed
          text (str): Answer text
          choices (list): List of choices associated with the answer
          meta (dict): any metadata related to this ask message

        """
        super().__init__(device_identifier, user_identifier)

        self.language = language
        self.slot = slot
        self.text = text
        self.choices = choices
        self.meta = meta
