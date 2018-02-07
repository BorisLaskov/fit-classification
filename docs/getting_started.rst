Getting started
***************

Installation
============

You can get a current version of the library via PyPI.
Install it with the following command:

.. code:: bash

    python -m pip install fit-classification

Please note, that you need to have Python installed of the version at least 3.6.

There are also tests packaged inside.
To run, them simply use the following command:

.. code:: bash

    python setup.py test

All dependencies should be installed automatically for both the regular
installation and for tests.

If you happen to have our ``.tar.gz`` distribution package,
you can install it by unpacking it and typing:

.. code:: bash

    python setup.py install

Logging in
==========

To log in, you will need not only your username and password,
but also a Client ID and Secret codes. Get them by registering
a new web application in the
`AppsManager <https://auth.fit.cvut.cz/manager/>`__.
As a callback URL, use your host and a free port so that the library
can instantiate a web server and catch a callback with authorization code
(for example, type in :code:`http://localhost:8080`).
