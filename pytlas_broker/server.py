from pytlas_broker.channel import Channel
from pytlas_broker.messages import Message, Pong, Ask, Answer, Context, Done, Thinking
from pytlas_broker.topics import PARSE, PING
from pytlas.interpreters.snips import SnipsInterpreter
from pytlas import settings, Agent
from typing import List
import os, logging

class Model:
  """Represents a pytlas model used to communicate with the provided server
  using a Channel.
  """

  def __init__(self, lang: str, uid: str) -> None:
    self._channel: Channel = None
    self._did: str = None
    self._uid = uid
    self._lang = lang

  def update_device_channel(self, channel: Channel, id: str) -> None:
    self._channel = channel
    self._did = id

  def on_thinking(self) -> None:
    self._channel.send(Thinking(self._did, self._uid))

  def on_done(self, require_input: bool) -> None:
    self._channel.send(Done(self._did, self._uid, require_input))

  def on_ask(self, slot: str, text: str, choices: list, **meta) -> None:
    self._channel.send(
      Ask(self._did, self._uid, self._lang, slot, text, choices, **meta)
    )

  def on_answer(self, text: str, cards: list, **meta) -> None:
    self._channel.send(
      Answer(self._did, self._uid, self._lang, text, cards, **meta)
    )

  def on_context(self, context: str) -> None:
    if self._channel:
      self._channel.send(Context(self._did, self._uid, context))

def wrap_channel_handler(channel, func):
  return lambda msg: func(channel, msg)

class Server:
  """Base class which represents a broker server that respond to some messages.
  
  You probably want to extend this class and provide your own way to create
  pytlas agents on incoming requests by overriding the method `create_agent`.
  """

  def __init__(self):
    """Instantiate a pytlas broker server.
    """
    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self._agents = {}

  def subscribe_on(self, *channels: List[Channel]) -> None:
    """Ask the server to subscribe to the given Channel.

    Args:
      channel (Channel): Channel to subscribe on
    
    """
    for channel in channels:
      channel.subscribe(PING, wrap_channel_handler(channel, self.on_ping))
      channel.subscribe(PARSE, wrap_channel_handler(channel, self.on_parse))

  def create_agent(self, uid: str) -> Agent:
    """Creates an agent for the given unique identifier. It will look in the
    settings for a section with this uid and extract all user related stuff
    to agent metadata.

    Args:
      uid (str): Unique identifier

    Returns:
      Agent: The instantiated agent

    """
    self._logger.info(f'Creating agent for uid {uid}')

    lang = settings.get('lang', 'en', section=uid)
    cache_dir = os.path.join(settings.get(settings.SETTING_CACHE, 'cache'), uid)
    prefix = uid + '.'
    meta = {}

    # Let's transform user sections to agent metadata
    user_sections = [s for s in settings.config.sections() if s.startswith(prefix)]

    for section in user_sections:
      meta.update({ 
        settings.to_env_key(section.replace(prefix, ''), k): v 
        for k, v in settings.config.items(section) })

    interpreter = SnipsInterpreter(lang, cache_directory=cache_dir)
    return Agent(interpreter, Model(lang, uid), **meta)

  def agent_from_channel_message(self, channel: Channel, msg: Message) -> Agent:
    """Retrieve an agent for the given message. If an agent does not exists, it
    will be created using the `create_agent` method.

    It also update the current agent channel to match the given channel.

    Args:
      channel (Channel): Channel which wants to communicate with the agent
      msg (Message): Message received
    
    """
    if msg.uid not in self._agents:
      self._agents[msg.uid] = self.create_agent(msg.uid)

    agt = self._agents[msg.uid]
    agt.model.update_device_channel(channel, msg.did)
    return agt

  def on_parse(self, channel: Channel, msg: Message):
    agt = self.agent_from_channel_message(channel, msg)
    agt.parse(msg.text, **msg.meta)

  def on_ping(self, channel: Channel, msg: Message):
    agt = self.agent_from_channel_message(channel, msg)
    channel.send(Pong(msg.did, msg.uid, agt._interpreter.lang))