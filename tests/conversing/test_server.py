from unittest.mock import MagicMock
from sure import expect
from pytlas import Agent
from pytlas.understanding import Interpreter
from pytlas_broker.conversing import Server
from pytlas_broker.conversing.agents import Factory
from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Ping, Pong, Parse

class TestServer:
  
    def test_it_should_create_an_agent_if_needed(self):
        f = Factory('test')
        f.create = MagicMock(return_value=Agent(Interpreter('test', 'fr')))
        c = Channel('test')

        s = Server(f)
        s.on_ping(c, Ping('pod', 'john'))

        f.create.assert_called_once_with('john')

        s.on_ping(c, Ping('pod', 'john'))
        f.create.assert_called_once()

    def test_it_should_handle_a_ping_request_and_answer_with_a_pong(self):
        f = Factory('test')
        f.create = MagicMock(return_value=Agent(Interpreter('test', 'fr')))
        c = Channel('test')
        c.send = MagicMock()

        s = Server(f)
        s.on_ping(c, Ping('pod', 'john'))

        c.send.assert_called_once()
        mes = c.send.call_args[0][0]
        expect(mes).to.be.a(Pong)
        expect(mes.device_identifier).to.equal('pod')
        expect(mes.user_identifier).to.equal('john')
        expect(mes.language).to.equal('fr')

    def test_it_should_answer_on_the_last_used_channel(self):
        f = Factory('test')
        f.create = MagicMock(return_value=Agent(Interpreter('test', 'fr')))

        c1 = Channel('test1')
        c1.send = MagicMock()
        c2 = Channel('test2')
        c2.send = MagicMock()

        s = Server(f)
        s.on_parse(c1, Parse('pod', 'john', 'hello there'))

        c1.send.assert_called_once()
        c2.send.assert_not_called()

        c1.send.reset_mock()

        s.on_parse(c2, Parse('pod', 'john', "What's up?"))
        c1.send.assert_not_called()
        c2.send.assert_called_once()

    def test_it_should_handle_a_parse_request(self):
        agt = Agent(Interpreter('test', 'fr'))
        agt.parse = MagicMock()
        f = Factory('test')
        f.create = MagicMock(return_value=agt)
        c = Channel('test')
        s = Server(f)
        s.on_parse(c, Parse('pod', 'john', 'hi there', a_meta='value'))

        agt.parse.assert_called_once_with('hi there', a_meta='value')
