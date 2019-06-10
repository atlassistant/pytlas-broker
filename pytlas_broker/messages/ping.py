from pytlas_broker.messages.message import Message
from pytlas_broker.topics import PING

class Ping(Message):
  """Represents a ping message.
  """

  def __init__(self, did, uid):
    """Instantiates a new message for the given client.

    Args:
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier representing the subject.
    
    """

    super().__init__(PING, did, uid)