from pytlas_broker.messages.message import Message
from pytlas_broker.topics import DONE

class Done(Message):
  """Represents a done message.
  """

  require_input: bool

  def __init__(self, did, uid, require_input):
    """Instantiates a new message for the given client.

    Args:
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier representing the subject.
      require_input (bool): True if more actions is needed, false otherwise.
    
    """

    super().__init__(DONE, did, uid)

    self.require_input = require_input