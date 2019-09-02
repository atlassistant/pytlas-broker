def contextualize(topic: str, did: str, uid: str = None) -> str:
    """Contextualize a topic for a specific subject.

    Args:
      topic (str): Topic to contextualize
      did (str): Device identifier
      uid (str): Unique subject identifier

    Returns:
      str: The contextualized topic

    Examples:
      >>> contextualize('atlas/+/+/ping', 'pod')
      'atlas/pod/+/ping'
      >>> contextualize('atlas/+/+/ping', 'pod', 'john')
      'atlas/pod/john/ping'

    """
    t = topic.replace('+', did, 1)

    if uid:
        t = t.replace('+', uid, 1)

    return t


def extract(topic: str) -> tuple:
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

# ----------------------------------------------------------
# CLIENT -> SERVER topics
# ----------------------------------------------------------


# Ping the broker server which should answer with a pong when
# the agent is ready.
PING = 'atlas/+/+/ping'

# Ask the server to parse a client message.
PARSE = 'atlas/+/+/parse'

# ----------------------------------------------------------
# SERVER -> CLIENT topics
# ----------------------------------------------------------

# Reply to a ping request when an agent is ready to fulfil requests.
PONG = 'atlas/+/+/pong'

# Call when a skill wants to communicate back with the client.
ANSWER = 'atlas/+/+/answer'

# Call when a skill needs more inputs to fulfil a client request.
ASK = 'atlas/+/+/ask'

# Call when switching to a new context.
CONTEXT = 'atlas/+/+/context'

# Call when a skill has ended his job.
DONE = 'atlas/+/+/done'

# Call when a skill has started processing a request.
THINKING = 'atlas/+/+/thinking'
