"""Defines an MQTT channel to be used by the broker and related stuff.
"""

import json
from typing import Tuple
import paho.mqtt.client as mqtt
from pytlas_broker.communicating.messages import Message
from pytlas_broker.communicating.channel import Channel


def contextualize(topic: str, device_identifier: str, user_identifier: str) -> str:
    """Creates the MQTT topic from given parts.

    Args:
        topic (str): Topic name
        device_identifier (str): Device identifier
        user_identifier (str): Subject of the message

    Returns:
        str: Fully qualified topic to use

    Examples:
        >>> contextualize('parse', 'pod', 'john')
        "atlas/pod/john/parse"

    """
    return f'atlas/{device_identifier}/{user_identifier}/{topic}'


def extract(topic: str) -> Tuple[str, str, str]:
    """Extract informations from a topic. This is the inverse function of
    contextualize.

    Args:
      topic (str): Topic source

    Returns:
      tuple: Message name, Device and unique identifiers extracted.

    Example:
      >>> extract('atlas/pod/john/ping')
      ('ping', 'pod', 'john')

    """
    _, did, uid, *_, name = topic.split('/')

    return (name, did, uid)


class MQTTChannel(Channel):
    """MQTT Channel implementation used to communicate with pytlas.
    """

    def __init__(self, host='localhost', port=1883) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connected
        self._client.on_disconnect = self._on_disconnected
        self._client.on_message = self._on_message

    def open(self) -> None:
        self._client.connect(self._host, self._port)
        self._client.loop_start()

    def close(self) -> None:
        self._client.disconnect()
        self._client.loop_stop()

    def send(self, message: Message) -> None:
        topic = message.__class__.__name__.lower()
        payload = json.dumps(message.data())
        self._client.publish(contextualize(topic,
                                           message.device_identifier,
                                           message.user_identifier),
                             payload)

    def _on_connected(self, client, userdata, flags, rc) -> None: # pylint: disable=invalid-name, unused-argument
        self._logger.info('Successfully connected to the broker at "%s"', self._host)

        for sub in (contextualize(m, '+', '+') for m in Message.available()):
            self._client.subscribe(sub)

    def _on_disconnected(self, client, userdata, rc): # pylint: disable=invalid-name, unused-argument
        self._logger.warning('Disconnected from the broker')

    def _on_message(self, client, userdata, msg) -> None: # pylint: disable=unused-argument
        topic, device, user = extract(msg.topic)
        payload = json.loads(msg.payload) if msg.payload else {}
        message = Message.from_data(topic, device, user, **payload)
        self.receive(message)
