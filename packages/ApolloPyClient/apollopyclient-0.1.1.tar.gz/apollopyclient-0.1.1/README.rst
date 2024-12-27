==============
ApolloPyClient
==============

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://opensource.org/license/MIT
    :alt: MIT License

.. image:: https://img.shields.io/pypi/v/ApolloPyClient.svg
    :target: https://pypi.python.org/pypi/ApolloPyClient



A Python SDK that is easy to integrate with the Apollo configuration management syste.

A Python package for apollo.

* GitHub repo: https://github.com/gcj-bit/ApolloPyClient
* Free software: MIT license

Installation
------------

.. code:: python

    pip install ApolloPyClient


Usage
--------
.. code:: python

    client = ApolloClient(
        app_id=os.environ.get('APOLLO_APP_ID'),
        config_service_url=os.environ.get('APOLLO_CONFIG_URL'),
        cluster=os.environ.get('APOLLO_CLUSTER'),
        secret=os.environ.get('APOLLO_SECRET'),
        env=os.environ.get('APOLLO_ENV'),
        namespaces=['application', 'test', 'testjson.json', 'testyaml.yaml'],
        ignore_ssl_verify=True,
    )
    print(client.all())
    # sleep for 100000 seconds, you can view log to get the config
    time.sleep(100000)



Reference
~~~~~~~~~~~~~~~~~~~~~~~~
Apollo : https://www.apolloconfig.com/#/en/client/other-language-client-user-guide
