from sure import expect
from unittest.mock import MagicMock
from pytlas_broker.channel import Channel
from pytlas_broker.server import Server
from pytlas_broker.topics import contextualize, PING, PONG
from pytlas import settings
import os

class TestServer:

  def setUp(self):
    settings.reset()

  def test_it_should_create_an_agent_with_appropriate_meta(self):
    settings.load(os.path.join(os.path.dirname(__file__), 'test.conf'))

    s = Server()
    agt = s.create_agent('john')

    expect(agt._interpreter.lang).to.equal('fr')
    expect(agt.meta).to.have.key('OPENWEATHER_APIKEY')
    expect(agt.meta['OPENWEATHER_APIKEY']).to.equal('john_api_key')

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
    chan1.write.assert_called_once_with(contextualize(PONG, 'pod', 'julie'), '{"language": "en"}')
    chan2.write.assert_not_called()

    chan2.receive(contextualize(PING, 'pod', 'julie'), '{}')
    chan1.write.assert_called_once()
    chan2.write.assert_called_once_with(contextualize(PONG, 'pod', 'julie'), '{"language": "en"}')
