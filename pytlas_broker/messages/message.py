from pytlas_broker.topics import contextualize

class Message:
  """Base class for a message which should be processed by a channel.
  """

  def __init__(self, topic: str, did: str, uid: str) -> None:
    """Intantiates a new message.

    Args:
      topic (str): Topic at which the message should be published.
      did (str): Unique device identifier for which this message has been generated.
      uid (str): Unique identifier for which this message has been generated.

    """

    self.topic = contextualize(topic, did, uid)
    self.did = did
    self.uid = uid

  def data(self) -> dict:
    """Gets the representation of this message.

    Returns:
      dict: Message representation.

    """

    d = dict(self.__dict__)

    del d['topic']
    del d['did']
    del d['uid']

    return d

  @staticmethod
  def from_data(name: str, did: str, uid: str, **payload) -> 'Message':
    """Try to instantiate a strongly typed message from the given name and payload.

    Args:
      name (str): Name of the message to be instantiated
      did (str): Device identifier
      uid (str): Subject of the message
      payload (dict): Key value pairs of the message data
    
    Returns:
      object: the instantiated message

    """

    cls = next((c for c in Message.__subclasses__() if c.__name__.lower() == name))

    payload['did'] = did
    payload['uid'] = uid
    
    # Handle the metadata specific case by flattening them in the payload
    if 'meta' in payload:
      payload.update(payload['meta'])
      del payload['meta']

    return cls(**payload)
    