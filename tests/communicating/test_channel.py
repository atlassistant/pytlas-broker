from unittest.mock import MagicMock
from sure import expect
from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Parse

class FakeHandler:
    def __init__(self):
        self.on_parse = MagicMock()


class TestChannel:

    def test_it_should_attach_handlers(self):
        hdl1 = FakeHandler()
        hdl2 = FakeHandler()

        c = Channel('test')
        c.attach(hdl1, hdl2)

        expect(c._handlers).to.have.length_of(2)
        expect(c._handlers).to.contain(hdl1)
        expect(c._handlers).to.contain(hdl2)

    def test_it_should_detach_handlers(self):
        hdl1 = FakeHandler()
        hdl2 = FakeHandler()
        hdl3 = FakeHandler()

        c = Channel('test')
        c.attach(hdl1, hdl2, hdl3)
        expect(c._handlers).to.have.length_of(3)

        c.detach(hdl2)
        expect(c._handlers).to.have.length_of(2)
        expect(c._handlers).to.contain(hdl1)
        expect(c._handlers).to_not.contain(hdl2)
        expect(c._handlers).to.contain(hdl3)

    def test_it_should_not_crash_when_removing_an_handler_not_registered(self):
        hdl = FakeHandler()
        c = Channel('test')
        c.detach(hdl)

    def test_it_should_trigger_call_on_each_model_upon_receiving_a_message(self):
        hdl1 = FakeHandler()
        hdl2 = FakeHandler()
        m = Parse('pod', 'john', 'Hello there!')

        c = Channel('test')
        c.attach(hdl1, hdl2)

        c.receive(m)

        hdl1.on_parse.assert_called_once_with(c, m)
        hdl2.on_parse.assert_called_once_with(c, m)

    def test_it_should_not_crash_when_model_attr_does_not_exists(self):
        class AnHandler:
            pass
        
        hdl = AnHandler()
        c = Channel('test')
        c.attach(hdl)

        c.receive(Parse('pod', 'john', 'Hello there!'))

    def test_enter_and_exit_should_call_open_and_close(self):
        c = Channel('test')
        c.open = MagicMock()
        c.close = MagicMock()

        with c:
            c.open.assert_called_once()
            c.close.assert_not_called()
        
        c.open.assert_called_once()
        c.close.assert_called_once()
