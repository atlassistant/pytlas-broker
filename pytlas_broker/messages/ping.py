from pytlas_broker.messages.message import Message
from pytlas_broker.topics import PING

class Ping(Message):
  """Represents a ping message.
  """

  def __init__(self, uid):
    """Instantiates a new message for the given client.

    Args:
      uid (str): Unique identifier representing the subject.
    
    """

    super().__init__(PING, uid)