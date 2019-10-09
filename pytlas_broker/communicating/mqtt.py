"""Defines an MQTT channel to be used by the broker and related stuff.
"""

import json
from typing import Tuple
import paho.mqtt.client as mqtt
from pytlas.settings import CONFIG
from pytlas_broker.communicating.messages import Message
from pytlas_broker.communicating.channel import Channel


SETTINGS_SECTION = 'mqtt'
SETTINGS_HOST = 'host'
SETTINGS_PORT = 'port'
SETTINGS_USERNAME = 'username'
SETTINGS_PASSWORD = 'password'


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
        'atlas/pod/john/parse'

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

    def __init__(self, host: str = None, port: int = None,
                 username: str = None, password: str = None) -> None:
        """Instantiate a new MQTT channel.

        Args:
            host (str): MQTT host. Look in settings mqtt.host and fallback to localhost
            port (int): MQTT port. Look in settings mqtt.port and fallback to 1883
            username (str): MQTT username. Look in settings mqtt.username
            password (str): MQTT password. Look in settings mqtt.password

        """
        super().__init__('mqtt')
        self._host = host or CONFIG.get(SETTINGS_HOST,
                                        'localhost', section=SETTINGS_SECTION)
        self._port = port or CONFIG.getint(SETTINGS_PORT,
                                           1883, section=SETTINGS_SECTION)
        self._username = username or CONFIG.get(SETTINGS_USERNAME, section=SETTINGS_SECTION)
        self._password = password or CONFIG.get(SETTINGS_PASSWORD, section=SETTINGS_SECTION)

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connected
        self._client.on_disconnect = self._on_disconnected
        self._client.on_message = self._on_message

    def open(self) -> None:
        if self._username or self._password:
            self._client.username_pw_set(self._username, self._password)

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
        self._logger.info('Successfully connected to the broker at "%s:%s"', self._host, self._port)

        for sub in (contextualize(m, '+', '+') for m in Message.available()):
            self._client.subscribe(sub)

    def _on_disconnected(self, client, userdata, rc): # pylint: disable=invalid-name, unused-argument
        self._logger.warning('Disconnected from the broker')

    def _on_message(self, client, userdata, msg) -> None: # pylint: disable=unused-argument
        topic, device, user = extract(msg.topic)
        payload = json.loads(msg.payload) if msg.payload else {}
        message = Message.from_data(topic, device, user, **payload)
        self.receive(message)
