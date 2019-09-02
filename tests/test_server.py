from sure import expect
from unittest.mock import MagicMock
from pytlas_broker.channel import Channel
from pytlas_broker.server import Server
from pytlas_broker.messages import Parse
from pytlas_broker.topics import contextualize, PING, PONG, PARSE
import os


class TestServer:

    def test_it_should_create_an_agent_only_if_it_doesnt_exist_yet(self):
        chan = Channel()
        s = Server()
        s.subscribe_on(chan)

        expect(chan._handlers).to.have.length_of(2)
        expect(s._agents).to.be.empty

        chan.receive(contextualize(PING, 'pod', 'julie'), '{}')

        expect(s._agents).to.have.key('julie')

        agt = s._agents['julie']

        chan.receive(contextualize(PING, 'pod', 'julie'), '{}')

        expect(s._agents['julie']).to.equal(agt)

    def test_it_should_answer_on_the_right_channel(self):
        chan1 = Channel()
        chan1.write = MagicMock()
        chan2 = Channel()
        chan2.write = MagicMock()

        s = Server()
        s.subscribe_on(chan1, chan2)

        chan1.receive(contextualize(PING, 'pod', 'julie'), '{}')
        chan1.write.assert_called_once_with(contextualize(
            PONG, 'pod', 'julie'), '{"language": "en"}')
        chan2.write.assert_not_called()

        chan2.receive(contextualize(PING, 'pod', 'julie'), '{}')
        chan1.write.assert_called_once()
        chan2.write.assert_called_once_with(contextualize(
            PONG, 'pod', 'julie'), '{"language": "en"}')

    def test_it_should_answer_to_a_parse_request(self):
        chan = Channel()
        s = Server()
        s.on_parse = MagicMock()
        s.subscribe_on(chan)

        chan.receive(contextualize(PARSE, 'pod', 'john'),
                     '{"text": "hello there", "meta": {"a_meta": "a_value"} }')

        s.on_parse.assert_called_once()
        c, m = s.on_parse.call_args[0]

        expect(c).to.equal(chan)
        expect(m.data()).to.equal(
            Parse('pod', 'john', 'hello there', a_meta='a_value').data())
