# pylint: disable=C0111


class Message:
    """Base class for a message which should be transported by a channel.
    """

    def __init__(self, device_identifier: str, user_identifier: str) -> None:
        """Intantiates a new message.

        Args:
          topic (str): Topic at which the message should be published.
          device_identifier (str): Unique device identifier for which this message
            has been generated.
          user_identifier (str): Unique identifier for which this message has been generated.

        """
        self.device_identifier = device_identifier
        self.user_identifier = user_identifier

    def data(self) -> dict:
        """Gets the representation of this message.

        Returns:
          dict: Message representation.

        """
        data = dict(self.__dict__)

        # Let's remove unused fields
        del data['device_identifier']
        del data['user_identifier']

        return data

    @staticmethod
    def from_data(name: str, device_identifier: str, user_identifier: str, **payload) -> 'Message':
        """Try to instantiate a strongly typed message from the given name and payload.

        Args:
          name (str): Name of the message to be instantiated
          device_identifier (str): Device identifier
          user_identifier (str): Subject of the message
          payload (dict): Key value pairs of the message data

        Returns:
          object: the instantiated message

        """
        cls = next((c for c in Message.__subclasses__()
                    if c.__name__.lower() == name.lower()))

        # Sets mandatory message arguments
        payload['device_identifier'] = device_identifier
        payload['user_identifier'] = user_identifier

        # Handle the metadata specific case by flattening them in the payload
        if 'meta' in payload:
            payload.update(payload['meta'])
            del payload['meta']

        return cls(**payload)
