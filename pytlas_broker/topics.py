def contextualize(topic, uid):
  """Contextualize a topic for a specific subject.

  Args:
    topic (str): Topic to contextualize
    uid (str): Unique subject identifier
  
  Returns:
    str: The contextualized topic
  
  Examples:
    >>> contextualize('atlas/+/ping', 'john')
    'atlas/john/ping'

  """
  
  return topic.replace('+', uid)

# ----------------------------------------------------------
# CLIENT -> SERVER topics
# ----------------------------------------------------------

# Ping the broker server which should answer with a pong when
# the agent is ready.
PING = 'atlas/+/ping'

# Ask the server to parse a client message.
PARSE = 'atlas/+/parse'

# ----------------------------------------------------------
# SERVER -> CLIENT topics
# ----------------------------------------------------------

# Reply to a ping request when an agent is ready to fulfil requests.
PONG = 'atlas/+/pong'

# Call when a skill wants to communicate back with the client.
ANSWER = 'atlas/+/answer'

# Call when a skill needs more inputs to fulfil a client request.
ASK = 'atlas/+/ask'

# Call when switching to a new context.
CONTEXT = 'atlas/+/context'

# Call when a skill has ended his job.
DONE = 'atlas/+/done'

# Call when a skill has started processing a request.
THINKING = 'atlas/+/thinking'
