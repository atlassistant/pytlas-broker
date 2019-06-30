from pytlas_broker.channel import Channel
from pytlas_broker.messages import Pong, Ask, Answer, Context, Done, Thinking
from pytlas_broker.topics import PARSE, PING
from pytlas.interpreters.snips import SnipsInterpreter
from pytlas import settings, Agent

class Model:
  """Represents a pytlas model used to communicate with the provided server
  using a Channel.
  """

  _uid: str
  _did: str
  _lang: str
  _channel: Channel

  def __init__(self, channel, lang, did, uid):
    self._channel = channel
    self._uid = uid
    self._did = did
    self._lang = lang

  def update_device(self, id):
    self._did = id

  def on_thinking(self):
    self._channel.send(Thinking(self._did, self._uid))

  def on_done(self, require_input):
    self._channel.send(Done(self._did, self._uid, require_input))

  def on_ask(self, slot, text, choices, **meta):
    self._channel.send(
      Ask(self._did, self._uid, self._lang, slot, text, choices, **meta)
    )

  def on_answer(self, text, cards, **meta):
    self._channel.send(
      Answer(self._did, self._uid, self._lang, text, cards, **meta)
    )

  def on_context(self, context):
    self._channel.send(Context(self._did, self._uid, context))

class Server:
  """Base class which represents a broker server that respond to some messages.
  
  You probably want to extend this class and provide your own way to create
  pytlas agents on incoming requests by overriding the method `create_agent`.
  """

  _channel: Channel
  _agents: dict = {}

  def __init__(self, channel):
    """Instantiate a pytlas broker server.

    Args:
      channel (Channel): Channel used to communicate with clients.
    
    """
    self._channel = channel
    self._channel.subscribe(PING, self.on_ping)
    self._channel.subscribe(PARSE, self.on_parse)

  def create_agent(self, uid):
    """Creates an agent for the given unique identifier. It will look in the
    settings for a section with this uid and extract all user related stuff
    to agent metadata.

    Args:
      uid (str): Unique identifier

    Returns:
      Agent: The instantiated agent

    """
    lang = settings.get('language', 'en', section=uid)
    prefix = uid + '.'
    meta = {}

    # Let's transform user sections to agent metadata
    user_sections = [s for s in settings.config.sections() if s.startswith(prefix)]

    for section in user_sections:
      meta.update({ 
        settings.to_env_key(section.replace(prefix, ''), k): v 
        for k, v in settings.config.items(section) })

    interpreter = SnipsInterpreter(lang)
    return Agent(interpreter, self.create_model(lang, uid), **meta)

  def create_model(self, lang, uid):
    """Creates a pytlas model with the server channel to communicate with
    clients.

    Args:
      lang (str): Language of the agent
      uid (str): Unique identifier
    
    Returns:
      Model: A model object

    """
    return Model(self._channel, lang, '', uid)

  def agent_from_message(self, msg):
    """Retrieve an agent for the given message. If an agent does not exists, it
    will be created using the `create_agent` method.

    Args:
      msg (Message): Message received
    
    """
    if msg.uid not in self._agents:
      self._agents[msg.uid] = self.create_agent(msg.uid)
    
    agt = self._agents[msg.uid]
    agt.model.update_device(msg.did)
    return agt

  def on_parse(self, msg):
    agt = self.agent_from_message(msg)
    agt.parse(msg.text, **msg.meta)

  def on_ping(self, msg):
    agt = self.agent_from_message(msg)
    self._channel.send(Pong(msg.did, msg.uid, agt._interpreter.lang))