from pytlas_broker.topics import contextualize

class Message:
  """Base class for a message which should be processed by a channel.
  """

  topic: str
  uid: str

  def __init__(self, topic, uid):
    """Intantiates a new message.

    Args:
      topic (str): Topic at which the message should be published.
      uid (str): Unique identifier for which this message has been generated.

    """

    self.topic = contextualize(topic, uid)
    self.uid = uid

  def data(self) -> dict:
    """Gets the representation of this message.

    Returns:
      dict: Message representation.

    """

    d = dict(self.__dict__)

    del d['topic']
    del d['uid']

    return d

  @staticmethod
  def from_data(name, uid, **payload):
    """Try to instantiate a strongly typed message from the given name and payload.

    Args:
      name (str): Name of the message to be instantiated
      uid (str): Subject of the message
      payload (dict): Key value pairs of the message data
    
    Returns:
      object: the instantiated message

    """

    cls = next((c for c in Message.__subclasses__() if c.__name__.lower() == name))

    payload['uid'] = uid
    
    # Handle the metadata specific case by flattening them in the payload
    if 'meta' in payload:
      payload.update(payload['meta'])
      del payload['meta']

    return cls(**payload)
    