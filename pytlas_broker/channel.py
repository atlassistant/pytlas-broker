from pytlas_broker.messages import Message
from pytlas_broker.topics import extract
import json

class Channel:
  """Represents a transport layer for messages.
  """

  _client: object

  def __init__(self, client=None):
    self._client = client

  def attach(self, client):
    """Attach a client to this channel.

    It means that this client will receive channel events.

    Args:
      client (object): Object which will receive events.

    """

    self._client = client

  def open(self):
    pass

  def close(self):
    pass

  def subscribe(self, *topics):
    pass

  def write(self, topic, payload):
    pass

  def _try_call_callback(self, msg):
    if not self._client:
      return

    cb = getattr(self._client, 'on_%s' % msg.__class__.__name__.lower(), None)

    if cb:
      cb(msg)

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

    try:
      self._try_call_callback(Message.from_data(name, did, uid, **payload))
    except:
      pass # TODO: Proper handling
