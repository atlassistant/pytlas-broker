from pytlas_broker.messages.message import Message
from pytlas_broker.topics import THINKING

class Thinking(Message):
  """Represents a thinking message.
  """

  def __init__(self, did: str, uid: str) -> None:
    """Instantiates a new message for the given client.

    Args:
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier representing the subject.
    
    """

    super().__init__(THINKING, did, uid)