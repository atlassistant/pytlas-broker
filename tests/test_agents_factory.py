from sure import expect
from pytlas_broker.agents_factory import from_settings
from pytlas import settings
import os


class TestAgentsFactory:

    def test_it_should_create_an_agent_from_settings(self):
        settings.load(os.path.join(os.path.dirname(__file__), 'test.conf'))

        agt = from_settings('john')

        expect(agt._interpreter.lang).to.equal('fr')
        expect(agt.meta).to.have.key('OPENWEATHER_APIKEY')
        expect(agt.meta['OPENWEATHER_APIKEY']).to.equal('john_api_key')
