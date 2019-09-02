"""Represents some implementations of agent factory used in the server 
component.
"""

import os
from pytlas import Agent, settings
from pytlas.interpreters.snips import SnipsInterpreter
from pytlas_broker.channel_model import ChannelModel


def from_settings(uid: str) -> Agent:
    """Creates an agent for the given unique identifier. It will look in the
    settings for a section with this uid and extract all user related stuff
    to agent metadata.

    Args:
      uid (str): Unique identifier

    Returns:
      Agent: The instantiated agent

    """
    lang = settings.get('lang', 'en', section=uid)
    cache_dir = os.path.join(settings.get(
        settings.SETTING_CACHE, 'cache'), uid)
    prefix = uid + '.'
    meta = {}

    # Let's transform user sections to agent metadata
    user_sections = [s for s in settings.config.sections()
                     if s.startswith(prefix)]

    for section in user_sections:
        meta.update({
            settings.to_env_key(section.replace(prefix, ''), k): v
            for k, v in settings.config.items(section)})

    interpreter = SnipsInterpreter(lang, cache_directory=cache_dir)
    return Agent(interpreter, ChannelModel(lang, uid), **meta)
