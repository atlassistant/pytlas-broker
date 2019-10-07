from unittest.mock import MagicMock
from sure import expect
from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Thinking, Ask, Answer, Done, Context
from pytlas_broker.conversing.model import ChannelModel

class TestChannelModel:

    def test_it_should_be_initialized_without_channel(self):
        m = ChannelModel('fr', 'john')

        expect(m._user_identifier).to.equal('john')
        expect(m._lang).to.equal('fr')
        expect(m._channel).to.be.none
        expect(m._device_identifier).to.be.none

    def test_it_should_allow_updates_to_his_inner_channel_and_use_it(self):
        c = Channel('test')
        c.send = MagicMock()
        m = ChannelModel('fr', 'john')
        m.last_seen_on('pod', c)

        expect(m._channel).to.equal(c)
        expect(m._device_identifier).to.equal('pod')

        m.on_thinking()
        c.send.assert_called_once()

    def test_it_should_do_nothing_if_no_channel_has_been_provided_yet(self):
        m = ChannelModel('fr', 'john')
        m.on_thinking()
        m.on_answer('an answer', [], meta='one')
        m.on_ask('location', 'a question', [], meta='two')
        m.on_done(False)
        m.on_context('a_context')

    def test_it_should_send_thinking_message(self):
        m = ChannelModel('fr', 'john')
        m._device_identifier = 'pod'
        m._send = MagicMock()
        
        m.on_thinking()

        m._send.assert_called_once()
        mes = m._send.call_args[0][0]
        expect(mes).to.be.a(Thinking)
        expect(mes.device_identifier).to.equal('pod')
        expect(mes.user_identifier).to.equal('john')

    def test_it_should_send_done_message(self):
        m = ChannelModel('fr', 'john')
        m._device_identifier = 'pod'
        m._send = MagicMock()

        m.on_done(True)
        m._send.assert_called_once()
        mes = m._send.call_args[0][0]
        expect(mes).to.be.a(Done)
        expect(mes.device_identifier).to.equal('pod')
        expect(mes.user_identifier).to.equal('john')
        expect(mes.require_input).to.be.true

    def test_it_should_send_ask_message(self):
        m = ChannelModel('fr', 'john')
        m._device_identifier = 'pod'
        m._send = MagicMock()

        m.on_ask('location', 'a question', ['choice 1', 'choice 2'], meta='two')
        mes = m._send.call_args[0][0]
        expect(mes).to.be.an(Ask)
        expect(mes.device_identifier).to.equal('pod')
        expect(mes.user_identifier).to.equal('john')
        expect(mes.slot).to.equal('location')
        expect(mes.text).to.equal('a question')
        expect(mes.choices).to.equal(['choice 1', 'choice 2'])
        expect(mes.meta).to.equal({ 'meta': 'two' })

    def test_it_should_send_answer_message(self):
        m = ChannelModel('fr', 'john')
        m._device_identifier = 'pod'
        m._send = MagicMock()

        m.on_answer('an answer', [], meta='one')
        mes = m._send.call_args[0][0]
        expect(mes).to.be.an(Answer)
        expect(mes.device_identifier).to.equal('pod')
        expect(mes.user_identifier).to.equal('john')
        expect(mes.text).to.equal('an answer')
        expect(mes.cards).to.be.empty
        expect(mes.meta).to.equal({ 'meta': 'one' })

    def test_it_should_send_context_message(self):
        m = ChannelModel('fr', 'john')
        m._device_identifier = 'pod'
        m._send = MagicMock()

        m.on_context('a_context')
        mes = m._send.call_args[0][0]
        expect(mes).to.be.a(Context)
        expect(mes.device_identifier).to.equal('pod')
        expect(mes.user_identifier).to.equal('john')
        expect(mes.context).to.equal('a_context')
