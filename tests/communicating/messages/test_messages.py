from sure import expect
from pytlas_broker.communicating.messages import Message, Ping, Pong, Parse, \
    Answer, Ask, Context, Done, Thinking


class TestPingMessage:

    def test_it_should_contain_no_payload(self):
        m = Ping('pod', 'john')
        expect(m.data()).to.be.empty

    def test_it_should_be_deserializable(self):
        m = Message.from_data('ping', 'pod', 'john')
        expect(m).to.be.a(Ping)
        expect(m.device_identifier).to.equal('pod')
        expect(m.user_identifier).to.equal('john')


class TestPongMessage:

    def test_it_should_contain_attr_data(self):
        m = Pong('pod', 'john', 'fr-FR')

        expect(m.data()).to.equal({
            'language': 'fr-FR',
        })

    def test_it_should_be_deserializable(self):
        m = Message.from_data('pong', 'pod', 'john',
                              language='en-US')

        expect(m).to.be.a(Pong)
        expect(m.device_identifier).to.equal('pod')
        expect(m.user_identifier).to.equal('john')
        expect(m.language).to.equal('en-US')


class TestParseMessage:

    def test_it_should_contain_attr_data(self):
        m = Parse('pod', 'john', 'Turn the lights on', a_meta=5)

        expect(m.data()).to.equal({
            'text': 'Turn the lights on',
            'meta': {
                'a_meta': 5,
            }
        })

    def test_it_should_be_deserializable(self):
        m = Message.from_data('parse', 'pod', 'john',
                              text='Turn the lights on', meta={'a_meta': 5})

        expect(m).to.be.a(Parse)
        expect(m.device_identifier).to.equal('pod')
        expect(m.user_identifier).to.equal('john')
        expect(m.text).to.equal('Turn the lights on')
        expect(m.meta).to.equal({
            'a_meta': 5,
        })


class TestAnswerMessage:

    def test_it_should_contain_attr_data(self):
        m = Answer('pod', 'john', 'fr-FR', 'This is a message', [],
                   a_meta=5, another_one=66)

        expect(m.data()).to.equal({
            'language': 'fr-FR',
            'text': 'This is a message',
            'cards': [],
            'meta': {
                'a_meta': 5,
                'another_one': 66,
            },
        })

        def test_it_should_be_deserializable(self):
            m = Message.from_data('answer', 'pod', 'john', language='en-US',
                                  text='This is a message', cards=[], meta={'a_meta': 5, 'another_one': 66})

            expect(m).to.be.an(Answer)
            expect(m.device_identifier).to.equal('pod')
            expect(m.user_identifier).to.equal('john')
            expect(m.language).to.equal('en-US')
            expect(m.text).to.equal('This is a message')
            expect(m.cards).to.be.empty
            expect(m.meta).to.equal({
                'a_meta': 5,
                'another_one': 66,
            })


class TestAskMessage:

    def test_it_should_contain_attr_data(self):
        m = Ask('pod', 'john', 'fr-FR',
                'room', 'Which rooms?', [], a_meta=5)

        expect(m.data()).to.equal({
            'language': 'fr-FR',
            'slot': 'room',
            'text': 'Which rooms?',
            'choices': [],
            'meta': {
                'a_meta': 5,
            },
        })

    def test_it_should_be_deserializable(self):
        m = Message.from_data('ask', 'pod', 'john', language='en-US',
                              slot='room', text='Which rooms?', choices=[], meta={'a_meta': 5})

        expect(m).to.be.an(Ask)
        expect(m.device_identifier).to.equal('pod')
        expect(m.user_identifier).to.equal('john')
        expect(m.language).to.equal('en-US')
        expect(m.slot).to.equal('room')
        expect(m.text).to.equal('Which rooms?')
        expect(m.choices).to.be.empty
        expect(m.meta).to.equal({
            'a_meta': 5,
        })


class TestContextMessage:

    def test_it_should_contain_attr_data(self):
        m = Context('pod', 'john', 'new_context')

        expect(m.data()).to.equal({
            'context': 'new_context',
        })

    def test_it_should_be_deserializable(self):
        m = Message.from_data('context', 'pod',
                              'john', context='new_context')

        expect(m).to.be.a(Context)
        expect(m.device_identifier).to.equal('pod')
        expect(m.user_identifier).to.equal('john')
        expect(m.context).to.equal('new_context')


class TestDoneMessage:

    def test_it_should_contain_attr_data(self):
        m = Done('pod', 'john', False)

        expect(m.data()).to.equal({
            'require_input': False,
        })

    def test_it_should_be_deserializable(self):
        m = Message.from_data('done', 'pod', 'john', require_input=True)

        expect(m).to.be.a(Done)
        expect(m.device_identifier).to.equal('pod')
        expect(m.user_identifier).to.equal('john')
        expect(m.require_input).to.be.true


class TestThinkingMessage:

    def test_it_should_contain_attr_data(self):
        m = Thinking('pod', 'john')

        expect(m.data()).to.be.empty

    def test_it_should_be_deserializable(self):
        m = Message.from_data('thinking', 'pod', 'john')

        expect(m).to.be.a(Thinking)
        expect(m.device_identifier).to.equal('pod')
        expect(m.user_identifier).to.equal('john')
