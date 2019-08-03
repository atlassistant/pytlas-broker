from pytlas_broker.channel import Channel
from pytlas_broker.messages import Message, Ask, Answer, Context, Done, Thinking

class ChannelModel:
  """Represents an agent model tied to a Channel. This is the model you must
  provide to a pytlas agent if you want it to communicate via the current
  Channel.

  This model will be used by the Server implementation to communicate back with
  the client in the other side of a Channel.
  """
  
  def __init__(self, lang: str, uid: str) -> None:
    self._channel: Channel = None
    self._did: str = ''
    self._uid = uid
    self._lang = lang

  def update_device_channel(self, channel: Channel, id: str) -> None:
    self._channel = channel
    self._did = id

  def _send(self, msg: Message):
    if self._channel:
      self._channel.send(msg)

  def on_thinking(self) -> None:
    self._send(Thinking(self._did, self._uid))

  def on_done(self, require_input: bool) -> None:
    self._send(Done(self._did, self._uid, require_input))

  def on_ask(self, slot: str, text: str, choices: list, **meta) -> None:
    self._send(
      Ask(self._did, self._uid, self._lang, slot, text, choices, **meta)
    )

  def on_answer(self, text: str, cards: list, **meta) -> None:
    self._send(Answer(self._did, self._uid, self._lang, text, cards, **meta))

  def on_context(self, context: str) -> None:
    self._send(Context(self._did, self._uid, context))