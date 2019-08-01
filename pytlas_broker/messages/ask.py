from pytlas_broker.messages.message import Message
from pytlas_broker.topics import ASK

class Ask(Message):
  """Represents an answer message.
  """

  def __init__(self, did: str, uid: str, language: str, slot: str, 
    text: str, choices: list, **meta) -> None:
    """Instantiates a new message for the given client.

    Args:
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier representing the subject.
      language (str): Agent language
      slot (str): Slot needed
      text (str): Answer text
      choices (list): List of choices associated with the answer
      meta (dict): any metadata related to this ask message
    
    """
    
    super().__init__(ASK, did, uid)

    self.language = language
    self.slot = slot
    self.text = text
    self.choices = choices
    self.meta = meta