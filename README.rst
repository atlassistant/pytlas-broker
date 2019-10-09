pytlas-broker |travis| |cover| |pypi| |license|
===============================================

.. |travis| image:: https://travis-ci.org/atlassistant/pytlas-broker.svg?branch=master
    :target: https://travis-ci.org/atlassistant/pytlas-broker

.. |cover| image:: https://codecov.io/gh/atlassistant/pytlas-broker/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/atlassistant/pytlas-broker

.. |pypi| image:: https://badge.fury.io/py/pytlas-broker.svg
    :target: https://badge.fury.io/py/pytlas-broker

.. |license| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0

Library and Command Line Utilities to communicate with the
`pytlas open-source assistant <https://github.com/atlassistant/pytlas>`_ using
channels (such as GSM or MQTT).

Purpose
-------

It wraps the **pytlas** library in a tiny **server** accessible from multiple
**channels** to make it easy to create clients in the language of your choice
to trigger user agents.

Installation
------------

.. code-block:: bash

  $ pip install pytlas-broker # Gets the latest release from pypi
  $ git clone https://github.com/atlassistant/pytlas-broker && cd pytlas-broker && pip install -e . # or directly from source

Getting started
---------------

For now, both the server and the client CLI communicates with an MQTT server. If
you wish to provider host, port and credentials, just sets pytlas settings in the
**mqtt** section:

.. code-block:: ini

  [pytlas]
  skills_dir=skills/

  [mqtt]
  host=localhost
  port=1883
  username=
  password=

Server
~~~~~~

At the moment, the CLI will serve agents loaded from a configuration folder using
MQTT.

It assumes the following directory structure:

- your_data_folder/
  
  - default/ # Represents the default directory if the user does not have one
  
    - skills/ # Referenced via the below pytlas.ini file
    - cache/ # Cache folder for pytlas interpreter
    - pytlas.ini # This file will be loaded at startup by the CLI for initial configuration
  
  - john/
    
    - cache/ # Cache folder specific for that user
    - pytlas.ini # May override settings for this user only

When the server receive a message from an opened channel, it will create an agent
for the user (if it doesn't exist yet) and answer on the last available channel
for that user.

To start the broker, use the following command:

.. code-block:: bash

  $ pytlas-broker serve your_data_folder/

And if you have already cloned the **pytlas** repository in the previous folder,
you can serve the examples right away using:

.. code-block:: bash

  $ pytlas-broker serve ../pytlas/ --default example

Client
~~~~~~

Once your server is running, you can start a tiny REPL client with the command:

.. code-block:: bash

  $ pytlas-broker repl

Testing
-------

.. code-block:: bash

  $ pip install -e .[test]
  $ python -m nose --with-doctest -v --with-coverage --cover-package=pytlas_broker

Linting
-------

.. code-block:: bash

  $ pylint --rcfile .pylintrc pytlas_broker setup.py # in the root directory
