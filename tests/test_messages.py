from sure import expect
from pytlas_broker.messages import Message, Ping, Pong, Parse, Answer, Ask, \
  Context, Done, Thinking
from pytlas_broker.topics import PING, PONG, PARSE, ANSWER, ASK, CONTEXT, \
  DONE, THINKING, contextualize

TEST_DID = 'pod'
TEST_UID = 'john'
TEST_LANGUAGE = 'fr-FR'

class TestPingMessage:

  def test_it_should_contain_no_payload(self):
    m = Ping(TEST_DID, TEST_UID)

    expect(m.topic).to.equal(contextualize(PING, TEST_DID, TEST_UID))
    expect(m.data()).to.be.empty

  def test_it_should_be_deserializable(self):
    m = Message.from_data('ping', TEST_DID, TEST_UID)

    expect(m).to.be.a(Ping)

class TestPongMessage:

  def test_it_should_contain_attr_data(self):
    m = Pong(TEST_DID, TEST_UID, TEST_LANGUAGE)

    expect(m.topic).to.equal(contextualize(PONG, TEST_DID, TEST_UID))
    expect(m.data()).to.equal({
      'language': TEST_LANGUAGE,
    })

  def test_it_should_be_deserializable(self):
    m = Message.from_data('pong', TEST_DID, TEST_UID, language=TEST_LANGUAGE)

    expect(m).to.be.a(Pong)
    expect(m.language).to.equal(TEST_LANGUAGE)

class TestParseMessage:

  def test_it_should_contain_attr_data(self):
    m = Parse(TEST_DID, TEST_UID, 'Turn the lights on', a_meta=5)
    
    expect(m.topic).to.equal(contextualize(PARSE, TEST_DID, TEST_UID))
    expect(m.data()).to.equal({
      'text': 'Turn the lights on',
      'meta': {
        'a_meta': 5,
      }
    })

  def test_it_should_be_deserializable(self):
    m = Message.from_data('parse', TEST_DID, TEST_UID, text='Turn the lights on', meta={'a_meta': 5})

    expect(m).to.be.a(Parse)
    expect(m.text).to.equal('Turn the lights on')
    expect(m.meta).to.equal({
      'a_meta': 5,
    })

class TestAnswerMessage:

  def test_it_should_contain_attr_data(self):
    m = Answer(TEST_DID, TEST_UID, TEST_LANGUAGE, 'This is a message', [],
      a_meta=5, another_one=66)  

    expect(m.topic).to.equal(contextualize(ANSWER, TEST_DID, TEST_UID))
    expect(m.data()).to.equal({
      'language': TEST_LANGUAGE,
      'text': 'This is a message',
      'cards': [],
      'meta': {
        'a_meta': 5,
        'another_one': 66,
      },
    })

    def test_it_should_be_deserializable(self):
      m = Message.from_data('answer', TEST_DID, TEST_UID, language=TEST_LANGUAGE, text='This is a message', cards=[], meta={'a_meta': 5, 'another_one': 66})

      expect(m).to.be.an(Answer)
      expect(m.language).to.equal(TEST_LANGUAGE)
      expect(m.text).to.equal('This is a message')
      expect(m.cards).to.be.empty
      expect(m.meta).to.equal({
        'a_meta': 5,
        'another_one': 66,
      })

class TestAskMessage:

  def test_it_should_contain_attr_data(self):
    m = Ask(TEST_DID, TEST_UID, TEST_LANGUAGE, 'room', 'Which rooms?', [], a_meta=5)  

    expect(m.topic).to.equal(contextualize(ASK, TEST_DID, TEST_UID))
    expect(m.data()).to.equal({
      'language': TEST_LANGUAGE,
      'slot': 'room',
      'text': 'Which rooms?',
      'choices': [],
      'meta': {
        'a_meta': 5,
      },
    })
  
  def test_it_should_be_deserializable(self):
    m = Message.from_data('ask', TEST_DID, TEST_UID, language=TEST_LANGUAGE, slot='room', text='Which rooms?', choices=[], meta={'a_meta': 5})

    expect(m).to.be.an(Ask)
    expect(m.language).to.equal(TEST_LANGUAGE)
    expect(m.slot).to.equal('room')
    expect(m.text).to.equal('Which rooms?')
    expect(m.choices).to.be.empty
    expect(m.meta).to.equal({
      'a_meta': 5,
    })

class TestContextMessage:

  def test_it_should_contain_attr_data(self):
    m = Context(TEST_DID, TEST_UID, 'new_context')

    expect(m.topic).to.equal(contextualize(CONTEXT, TEST_DID, TEST_UID))
    expect(m.data()).to.equal({
      'context': 'new_context',
    })

  def test_it_should_be_deserializable(self):
    m = Message.from_data('context', TEST_DID, TEST_UID, context='new_context')

    expect(m).to.be.a(Context)
    expect(m.context).to.equal('new_context')

class TestDoneMessage:

  def test_it_should_contain_attr_data(self):
    m = Done(TEST_DID, TEST_UID, False)

    expect(m.topic).to.equal(contextualize(DONE, TEST_DID, TEST_UID))
    expect(m.data()).to.equal({
      'require_input': False,
    })

  def test_it_should_be_deserializable(self):
    m = Message.from_data('done', TEST_DID, TEST_UID, require_input=True)

    expect(m).to.be.a(Done)
    expect(m.require_input).to.be.true

class TestThinkingMessage:

  def test_it_should_contain_attr_data(self):
    m = Thinking(TEST_DID, TEST_UID)

    expect(m.topic).to.equal(contextualize(THINKING, TEST_DID, TEST_UID))
    expect(m.data()).to.be.empty

  def test_it_should_be_deserializable(self):
    m = Message.from_data('thinking', TEST_DID, TEST_UID)

    expect(m).to.be.a(Thinking)