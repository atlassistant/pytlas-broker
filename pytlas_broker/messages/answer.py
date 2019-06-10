from pytlas_broker.messages.message import Message
from pytlas_broker.topics import ANSWER

class Answer(Message):
  """Represents an answer message.
  """

  language: str
  text: str
  cards: list
  meta: dict

  def __init__(self, did, uid, language, text, cards, **meta):
    """Instantiates a new message for the given client.

    Args:
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier representing the subject.
      language (str): Agent language
      text (str): Answer text
      cards (list): List of cards associated with the answer
      meta (dict): any metadata related to this answer
    
    """
    
    super().__init__(ANSWER, did, uid)

    self.language = language
    self.text = text
    self.cards = cards
    self.meta = meta