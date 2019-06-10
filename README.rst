pytlas-broker
=============

Library and Command Line Utilities to communicate with the `pytlas open-source assistant <https://github.com/atlassistant/pytlas>`_ using an MQTT channel.

Testing
-------

.. code-block:: bash

  $ pip install -e .[snips,test]
  $ python -m nose --with-doctest -v --with-coverage --cover-package=pytlas_broker