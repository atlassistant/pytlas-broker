from pytlas_broker.messages.message import Message
from pytlas_broker.topics import PONG

class Pong(Message):
  """Represents a pong message.
  """

  language: str

  def __init__(self, uid, language):
    """Instantiates a new message for the given client.

    Args:
      uid (str): Unique identifier representing the subject.
      language (str): Agent language
    
    """
    
    super().__init__(PONG, uid)

    self.language = language