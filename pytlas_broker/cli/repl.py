# pylint: disable=unused-argument,missing-docstring,no-self-use

import cmd
from pytlas_broker.__about__ import __version__
from pytlas_broker.conversing import Client
from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Ask, Answer


class ReplClient(cmd.Cmd):
    """Tiny repl client used to communicate with a remote server.
    """

    intro = 'pytlas broker prompt v%s (type exit to leave)' % __version__
    prompt = ''

    def __init__(self, device_identifier: str, channel: Channel) -> None:
        super().__init__()
        self._client = Client(device_identifier, channel)

        # Since we already inherits from Cmd, lets redirect message handling
        self._client.on_ask = self.on_ask
        self._client.on_answer = self.on_answer

    def _print(self, msg):
        print('🤖💬 >', msg)

    def on_ask(self, channel: Channel, msg: Ask):
        self._print(msg.meta.get('raw_text', msg.text))

    def on_answer(self, channel: Channel, msg: Answer):
        self._print(msg.meta.get('raw_text', msg.text))

    def do_exit(self, msg):
        return True

    def default(self, line):
        self._client.parse(line, 'repl')
