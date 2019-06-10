from pytlas_broker.channel import Channel

class Server:

  _channel: Channel

  def __init__(self, channel):
    self._channel = channel

  def on_parse(self, msg):
    pass