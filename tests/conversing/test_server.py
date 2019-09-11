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
        c = Channel()

        s = Server(f)
        s.on_ping(c, Ping('pod', 'john'))

        f.create.assert_called_once_with('john')

        s.on_ping(c, Ping('pod', 'john'))
        f.create.assert_called_once()

    def test_it_should_handle_a_ping_request_and_answer_with_a_pong(self):
        f = Factory('test')
        f.create = MagicMock(return_value=Agent(Interpreter('test', 'fr')))
        c = Channel()
        c.send = MagicMock()

        s = Server(f)
        s.on_ping(c, Ping('pod', 'john'))

        c.send.assert_called_once()
        mes = c.send.call_args[0][0]
        expect(mes).to.be.a(Pong)
        expect(mes.device_identifier).to.equal('pod')
        expect(mes.user_identifier).to.equal('john')
        expect(mes.language).to.equal('fr')

    def test_it_should_handle_a_parse_request(self):
        agt = Agent(Interpreter('test', 'fr'))
        agt.parse = MagicMock()
        f = Factory('test')
        f.create = MagicMock(return_value=agt)
        c = Channel()
        s = Server(f)
        s.on_parse(c, Parse('pod', 'john', 'hi there', a_meta='value'))

        agt.parse.assert_called_once_with('hi there', a_meta='value')
