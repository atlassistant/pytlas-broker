import os
from configparser import ConfigParser
from unittest.mock import patch
from sure import expect
from pytlas_broker.conversing.agents import FromFileFactory
from pytlas_broker.conversing.agents.from_file import get_config_directories_path, \
    env_from_configparser, CACHE_DIR, CONF_FILENAME

class TestGetConfigDirectoriesPath:

    def test_it_should_returns_appropriate_path(self):
        p = get_config_directories_path('__settings', 'john')
        expect(p[0]).to.equal(os.path.abspath(os.path.join('__settings', 'john', CACHE_DIR)))
        expect(p[1]).to.equal(os.path.abspath(os.path.join('__settings', 'john', CONF_FILENAME)))

class TestEnvFromConfigParser:

    def test_it_should_convert_a_config_parser_object_to_dict(self):
        conf = ConfigParser()
        conf['pytlas'] = {
            'language': 'en',
        }
        conf['weather'] = {
            'apikey': 'akey!',
        }

        expect(env_from_configparser(conf)).to.equal({
            'PYTLAS_LANGUAGE': 'en',
            'WEATHER_APIKEY': 'akey!',
        })

class TestFromFile:

    def test_it_should_not_crash_when_the_directory_does_not_exist(self):
        f = FromFileFactory('an/unkown/path')
        expect(f._default_settings).to.be.empty

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
