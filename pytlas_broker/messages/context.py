from pytlas_broker.messages.message import Message
from pytlas_broker.topics import CONTEXT

class Context(Message):
  """Represents a context message.
  """

  context: str

  def __init__(self, uid, context):
    """Instantiates a new message for the given client.

    Args:
      uid (str): Unique identifier representing the subject.
      context (str): Name of the new active context
    
    """

    super().__init__(CONTEXT, uid)

    self.context = context