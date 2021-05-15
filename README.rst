consul-decouple
===============

An extension for
`python-decouple <https://github.com/henriquebastos/python-decouple>`__
to read Consul using
`python-consul2 <https://github.com/poppyred/python-consul2>`__.

.. code:: bash

    pip install consul-decouple


How it works
------------

1. Read config from environment;
2. If it's connected with Consul, it'll read the config from there;
3. python-decouple behavior:

   1. Repository: ini or .env file;
   2. default argument passed to config;


How to use
----------

-  Read Consul settings from enviroment. CONSUL\_HOST=host,
   CONSUL\_PORT=port, CONSUL\_TOKEN=token, CONSUL\_SCHEME=scheme

.. code-block:: python

    from consul_decouple import config

    my_key = config('my_bool_key', cast=bool, default=False)


-  Creating a custom Consul connection

.. code-block:: python

    from consul import Consul
    from consul_decouple import AutoConfig

    consul = Consul(host='127.0.0.1', port=8500, token=None, scheme='http')
    config = AutoConfig(consul)
    my_key = config('my_bool_key', cast=bool, default=False)


-  Read only one KeyValue from Consul and parse it from JSON. It'll
   reads the configs from the parsed JSON

.. code-block:: python

    from consul_decouple import AutoConfig

    config = AutoConfig(json_kv='my_key_with_json_value')
    my_key = config('my_bool_key', cast=bool, default=False)


Contribute
----------

.. code:: bash

    git clone https://github.com/lucasrcezimbra/consul-decouple
    cd consul-decouple
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt
    pre-commit install
    pytest
