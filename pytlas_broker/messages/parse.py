from pytlas_broker.messages.message import Message
from pytlas_broker.topics import PARSE

class Parse(Message):
  """Represents a parse message.
  """

  def __init__(self, did: str, uid: str, text: str, **meta) -> None:
    """Instantiates a new message for the given client.

    Args:
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier representing the subject.
      text (str): Answer text
      meta (dict): any metadata related to this answer
    
    """
    
    super().__init__(PARSE, did, uid)

    self.text = text
    self.meta = meta