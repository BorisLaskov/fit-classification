Python library for Classification portal
****************************************

This Python library lets you call API of the Classification portal (at FIT, CTU [1]_) and work with it from your Python programs. It is a coursework for MI-PYT subject.

Key features
============

- Access token management: login with your credentials once, and the token will be stored locally. If it expires, the library will automatically get a new one using refresh token retrieved earlier together with access token.
- Save certain URL parameters — no need to supply them with every API call.
- Use Python objects to generate request bodies — your IDE will show, what parameters they accept.
- Deal with retrieving and saving students' classifications with the help of simplified data format (these operations are considered to be used most frequently).

Installation notes
==================

You need to have Python installed of the version at least 3.6.

To log in, you will need not only your username and password, but also a Client ID and Secret codes. Get them by registering a new web application in the `AppsManager <https://auth.fit.cvut.cz/manager/>`__. As a callback URL, use your host and a free port so that the library can instantiate a web server and catch a callback with authorization code (for example, type in :code:`http://localhost:8080`).

Documentation
=============

The documentation can be found in the :code:`docs` folder.

If you would like to build it, you should firstly install the required dependencies. They can be found in the :code:`docs` folder in the :code:`requirements.txt` file.

To automatically install the requirements, you can use this command: :code:`pip install -r docs/requirements.txt`

To build it, use: :code:`cd docs && make html`

Please note, that you will likely need to have all dependencies of the library itself (not only of documentation) installed too. Just make sure that the library was installed (and brought all required projects with it).

Tests
=====

This package also has tests inside. To run them, use: :code:`python setup.py test`

Authors
=======

The library is created by Boris Laskov (`GitHub profile <https://github.com/145k0v>`__). For the flow of initial logging in, the author used `the code <https://gitlab.fit.cvut.cz/pulcpetr/classification-scripts>`__ authored by Petr Pulc (under MIT license).

License
=======

This project is licensed under the MIT License — see the LICENSE file for details.

Footnotes
=========

.. [1] `Faculty of Information Technology <https://www.fit.cvut.cz/en>`__,
       Czech Technical University in Prague.
