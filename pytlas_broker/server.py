from pytlas import Agent
from pytlas_broker.channel import Channel
from pytlas_broker.messages import Message, Pong
from pytlas_broker.topics import PARSE, PING
from pytlas_broker.agents_factory import from_settings
from typing import List
import os, logging

def wrap_channel_handler(channel: Channel, func: callable) -> callable:
  """Wrap a func inside a lambda and call it with the given channel.
  """
  return lambda msg: func(channel, msg)

class Server:
  """Base class which represents a broker server that respond to some messages.
  
  You probably want to extend this class and provide your own way to create
  pytlas agents on incoming requests by overriding the method `create_agent`.
  """

  def __init__(self, agents_factory: callable=None) -> None:
    """Instantiate a pytlas broker server.

    Args:
      agents_factory (callable): Method called when instantiating an agent. If no one is provided, the default will fallback to `agents_factory.from_settings`. this method will receive the user identifier as an argument and should use a `ChannelModel`.

    """
    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self._agents = {}
    self._factory = agents_factory or from_settings

  def subscribe_on(self, *channels: List[Channel]) -> None:
    """Ask the server to subscribe to the given Channel.

    Args:
      channel (Channel): Channel to subscribe on
    
    """
    for channel in channels:
      channel.subscribe(PING, wrap_channel_handler(channel, self.on_ping))
      channel.subscribe(PARSE, wrap_channel_handler(channel, self.on_parse))

  def agent_from_channel_message(self, channel: Channel, msg: Message) -> Agent:
    """Retrieve an agent for the given message. If an agent does not exists, it
    will be created using the `create_agent` method.

    It also update the current agent channel to match the given channel.

    Args:
      channel (Channel): Channel which wants to communicate with the agent
      msg (Message): Message received
    
    """
    if msg.uid not in self._agents:
      self._logger.info(f'Agent not found, creating one for user "{msg.uid}"')
      self._agents[msg.uid] = self._factory(msg.uid)

    agt = self._agents[msg.uid]
    agt.model.update_device_channel(channel, msg.did)
    return agt

  def on_parse(self, channel: Channel, msg: Message):
    agt = self.agent_from_channel_message(channel, msg)
    agt.parse(msg.text, **msg.meta)

  def on_ping(self, channel: Channel, msg: Message):
    agt = self.agent_from_channel_message(channel, msg)
    channel.send(Pong(msg.did, msg.uid, agt._interpreter.lang))