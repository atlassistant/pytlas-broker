import os
from unittest.mock import patch
from sure import expect
from pytlas_broker.conversing.agents import FromFileFactory
from pytlas_broker.conversing.agents.from_file import get_config_directories_path

class TestGetConfigDirectoriesPath:

    def test_it_should_returns_appropriate_path(self):
        p = get_config_directories_path('__settings', 'john')
        expect(p[0]).to.equal(os.path.abspath(os.path.join('__settings', 'john', 'cache')))
        expect(p[1]).to.equal(os.path.abspath(os.path.join('__settings', 'john', 'pytlas.ini')))

class TestFromFile:

    def test_it_should_instantiate_an_agent_from_a_file(self):
        f = FromFileFactory(os.path.join(os.path.dirname(__file__), '../../__settings'))
        agt = f.create('john')

        expect(agt.lang).to.equal('fr')
        expect(agt.settings.get('another_key')).to.equal('with a value')
        expect(agt.settings.get('apikey', section='weather')).to.equal('john_api_key')
        expect(f._default_settings['PYTLAS_LANGUAGE']).to.equal('en')

    def test_it_should_instantiate_an_agent_with_default_settings_if_not_found(self):
        f = FromFileFactory(os.path.join(os.path.dirname(__file__), '../../__settings'))
        agt = f.create('julie')

        expect(agt.lang).to.equal('en')
        expect(agt.settings.get('another_key')).to.equal('with a value')
        expect(agt.settings.get('apikey', section='weather')).to.equal('global_api_key')
