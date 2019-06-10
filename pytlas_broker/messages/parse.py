from pytlas_broker.messages.message import Message
from pytlas_broker.topics import PARSE

class Parse(Message):
  """Represents a parse message.
  """

  text: str
  meta: dict

  def __init__(self, uid, text, **meta):
    """Instantiates a new message for the given client.

    Args:
      uid (str): Unique identifier representing the subject.
      text (str): Answer text
      meta (dict): any metadata related to this answer
    
    """
    
    super().__init__(PARSE, uid)

    self.text = text
    self.meta = meta