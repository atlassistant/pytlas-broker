from pytlas_broker.messages.message import Message
from pytlas_broker.topics import CONTEXT

class Context(Message):
  """Represents a context message.
  """

  def __init__(self, did: str, uid: str, context: str) -> None:
    """Instantiates a new message for the given client.

    Args:
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier representing the subject.
      context (str): Name of the new active context
    
    """

    super().__init__(CONTEXT, did, uid)

    self.context = context