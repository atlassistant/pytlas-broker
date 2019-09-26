# pylint: disable=missing-module-docstring

import logging
from typing import Dict
from pytlas import Agent
from pytlas_broker.communicating import Channel
from pytlas_broker.communicating.messages import Message, Parse, Ping, Pong
from pytlas_broker.conversing.agents.factory import Factory
from pytlas_broker.conversing.model import ChannelModel


class Server:
    """Represents the base component which will handle client requests.

    It will manages its own dictionary of instantiated agents.
    """

    def __init__(self, agent_factory: Factory) -> None:
        """Instantiate a new server to handle client requests.

        Args:
            agent_factory (Factory): Factory used to create agent when none
            exists yet

        """
        self._logger = logging.getLogger('serv')
        self._agent: Dict[str, Agent] = {}
        self._factory = agent_factory

    def on_parse(self, channel: Channel, message: Parse) -> None:
        """Handler called when a parse message has been received.

        Args:
            channel (Channel): Channel which received the message
            message (Parse): Parse message received by the channel

        """
        agt = self._retrieve_or_create_agent_for(channel, message)
        agt.parse(message.text, **message.meta)

    def on_ping(self, channel: Channel, message: Ping) -> None:
        """Handler called when a ping message has been received. It will ensure
        an agent exists for the given uid and send a Pong response.

        Args:
            channel (Channel): Channel which received the message
            message (Ping): Parse message received by the channel

        """
        agt = self._retrieve_or_create_agent_for(channel, message)
        channel.send(Pong(message.device_identifier, message.user_identifier, agt.lang))

    def _retrieve_or_create_agent_for(self, channel: Channel, message: Message) -> Agent:
        if message.user_identifier not in self._agent:
            agt = self._factory.create(message.user_identifier)
            agt.model = ChannelModel(agt.lang, message.user_identifier)
            self._agent[message.user_identifier] = agt
        else:
            agt = self._agent[message.user_identifier]

        agt.model.last_seen_on(message.device_identifier, channel)

        return agt
