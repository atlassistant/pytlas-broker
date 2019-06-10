from pytlas_broker.channel import Channel
from pytlas_broker.topics import PARSE, PING

class Server:

  _channel: Channel

  def __init__(self, channel):
    """Instantiate a pytlas broker server.

    Args:
      channel (Channel): Channel used to communicate with clients.
    
    """

    self._channel = channel
    self._channel.attach(self)
    self._channel.subscribe(PING, PARSE)

  def on_parse(self, msg):
    pass

  def on_ping(self, msg):
    pass