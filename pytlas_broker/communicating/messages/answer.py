# pylint: disable=C0111,R0913

from pytlas_broker.communicating.messages.message import Message


class Answer(Message):
    """Represents an answer message.
    """

    def __init__(self, device_identifier: str, user_identifier: str, language: str,
                 text: str, cards: list, **meta) -> None:
        """Instantiates a new message for the given client.

        Args:
          device_identifier (str): Unique device identifier for which this message
            has been generated.
          user_identifier (str): Unique identifier representing the subject.
          language (str): Agent language
          text (str): Answer text
          cards (list): List of cards associated with the answer
          meta (dict): any metadata related to this answer

        """
        super().__init__(device_identifier, user_identifier)

        self.language = language
        self.text = text
        self.cards = cards
        self.meta = meta
