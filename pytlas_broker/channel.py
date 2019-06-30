from pytlas_broker.messages import Message
from pytlas_broker.topics import extract
import json, logging

class Channel:
  """Represents a transport layer for messages.
  """

  _handlers: dict = {}
  _logger = logging.Logger

  def __init__(self):
    self._logger = logging.getLogger(self.__class__.__name__.lower())

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    return False

  def subscribe(self, topic, handler):
    """Subscribes to the given topic. Given handler will receive all events for
    the extracted topic name so wildcards or path doesn't matter here.

    Args:
      topic (str): Topic string, name will be extracted
      handler (callable): Handler which will receive the deserialized Message

    """
    name, *_ = extract(topic) # Let's extract the topic name
    self._handlers[name] = handler

  def send(self, message):
    """Sends a message on this channel.

    Args:
      message (Message): Message to send

    """
    self.write(message.topic, json.dumps(message.data()))

  def receive(self, topic, data):
    """Receive a raw message on a given topic. This method will try to
    convert the raw data in a more meaningful representation and call
    an appropriate handler on the channel client if one exists.

    Args:
      topic (str): Source topic
      data (str): Raw payload

    """
    name, did, uid = extract(topic)
    payload = json.loads(data) if data else {}

    if name in self._handlers:
      handler = self._handlers[name]
      self._logger.info(f'Calling handler {handler} for topic {name}')
      handler(Message.from_data(name, did, uid, **payload))
    else:
      self._logger.info(f'No handlers for topic {name}')
  
  def write(self, topic, payload):
    """Write the given payload to the given topic. Should be overriden by
    implementations.

    Args:
      topic (str): Topic to write to
      payload (str): Serialized data to write

    """
    pass
