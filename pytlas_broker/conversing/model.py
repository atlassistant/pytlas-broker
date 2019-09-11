# pylint: disable=missing-docstring

from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Message, Ask, Answer, Context, Done, Thinking


class ChannelModel:
    """Represents an agent model tied to a Channel. This is the model you must
    provide to a pytlas agent inside the broker project.

    This model enables the agent to communicate back with the last used channel
    for a particular user.
    """

    def __init__(self, lang: str, user_identifier: str) -> None:
        """Instantiates a new channel model.

        Args:
            lang (str): Language of the agent, used in some messages
            user_identifier (str): User identifier

        """
        self._channel: Channel = None
        self._device_identifier: str = None
        self._user_identifier = user_identifier
        self._lang = lang

    def last_seen_on(self, device_identifier: str, channel: Channel) -> None:
        """Update the channel attached to this model. Basically, it will always be
        the last channel a user has used to communicate with an agent.

        Args:
            device_identifier (str): Last seen device identifier
            channel (Channel): Channel to use when replying

        """
        self._channel = channel
        self._device_identifier = device_identifier

    def on_thinking(self) -> None:
        self._send(Thinking(self._device_identifier, self._user_identifier))

    def on_done(self, require_input: bool) -> None:
        self._send(Done(self._device_identifier, self._user_identifier, require_input))

    def on_ask(self, slot: str, text: str, choices: list, **meta) -> None:
        self._send(Ask(self._device_identifier, self._user_identifier,
                       self._lang, slot, text, choices, **meta))

    def on_answer(self, text: str, cards: list, **meta) -> None:
        self._send(Answer(self._device_identifier, self._user_identifier,
                          self._lang, text, cards, **meta))

    def on_context(self, context: str) -> None:
        self._send(Context(self._device_identifier, self._user_identifier, context))

    def _send(self, msg: Message):
        if self._channel:
            self._channel.send(msg)
