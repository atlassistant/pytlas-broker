import os
from configparser import ConfigParser
from sure import expect
from pytlas.settings import CONFIG
from pytlas_broker.conversing.agents import FromFile
from pytlas_broker.conversing.agents.from_file import get_config_directories_path, \
    CACHE_DIR, CONF_FILENAME

class TestGetConfigDirectoriesPath:

    def test_it_should_returns_appropriate_path(self):
        p = get_config_directories_path('__settings', 'john')
        expect(p[0]).to.equal(os.path.abspath(os.path.join('__settings', 'john', CACHE_DIR)))
        expect(p[1]).to.equal(os.path.abspath(os.path.join('__settings', 'john', CONF_FILENAME)))

class TestFromFile:

    def setup(self):
        CONFIG.load_from_file(os.path.join(os.path.dirname(__file__), '../../__settings/default/pytlas.ini'))

    def teardown(self):
        CONFIG.reset()

    def test_it_should_not_crash_when_the_directory_does_not_exist(self):
        f = FromFile('an/unkown/path')
        # TODO some tests to create an agent (failed on windows when persisting the engine :/)

    def test_it_should_instantiate_an_agent_from_a_file(self):
        f = FromFile(os.path.join(os.path.dirname(__file__), '../../__settings'))
        agt = f.create('john')

        expect(agt.lang).to.equal('fr')
        expect(agt.settings.get('another_key')).to.equal('with a value')
        expect(agt.settings.get('apikey', section='weather')).to.equal('john_api_key')

    def test_it_should_instantiate_an_agent_with_default_settings_if_not_found(self):
        f = FromFile(os.path.join(os.path.dirname(__file__), '../../__settings'))
        agt = f.create('julie')

        expect(agt.lang).to.equal('en')
        expect(agt.settings.get('another_key')).to.equal('with a value')
        expect(agt.settings.get('apikey', section='weather')).to.equal('global_api_key')
