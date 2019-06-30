from sure import expect
from unittest.mock import MagicMock
from pytlas_broker.topics import contextualize, ANSWER, PARSE
from pytlas_broker.channel import Channel
from pytlas_broker.messages import Answer, Parse

class TestChannel:

  def test_it_should_serialize_a_message_when_sending(self):
    c = Channel()
    c.write = MagicMock()

    c.send(Answer('pod', 'john', 'en-US', 'Hello!', []))

    c.write.assert_called_once_with(contextualize(ANSWER, 'pod', 'john'), '{"language": "en-US", "text": "Hello!", "cards": [], "meta": {}}')

  def test_it_should_call_subcribe_callback_when_receiving_data(self):
    on_parse = MagicMock()
    on_answer = MagicMock()

    c = Channel()
    c.subscribe(PARSE, on_parse)
    c.subscribe(ANSWER, on_answer)

    c.receive(contextualize(PARSE, 'pod', 'john'), '{"text": "Hello you!"}')

    on_answer.assert_not_called()
    on_parse.assert_called_once()
    msg = on_parse.call_args[0][0]

    expect(msg).to.be.a(Parse)
    expect(msg.text).to.equal('Hello you!')
