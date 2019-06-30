from sure import expect
from pytlas_broker.server import Server
from pytlas_broker.channel import Channel
from pytlas import settings
import os

class TestServer:

  def setUp(self):
    settings.reset()

  def test_it_should_create_an_agent_with_appropriate_meta(self):
    settings.load(os.path.join(os.path.dirname(__file__), 'test.conf'))

    s = Server(Channel())
    agt = s.create_agent('john')

    expect(agt._interpreter.lang).to.equal('fr')
    expect(agt.meta).to.have.key('OPENWEATHER_APIKEY')
    expect(agt.meta['OPENWEATHER_APIKEY']).to.equal('john_api_key')