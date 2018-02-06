.. _key_features:

Key features
************

Access token management
=======================

Acquiring an access token can be somewhat complicated. In our project,
it is semi-automatized: it will open a webpage with a login form for you.
Once you put in your credentials and log in, it will capture a callback GET
with authorization code and make another HTTP request to get the real
access token. Once received, the token will be stored locally
in the library configuration folder [1]_. If the token is expired,
the library will automatically get a new one with the help of the refresh
token, which is also sent by the server on login and stored in the same file.

If you want to login again with other credentials, you should either
delete the file
where the token is stored or use ``force_new_token`` boolean parameter
in the constructor of :py:class:`~classification.classification.Classification`
class.
If you do not want to create another client instance, simply call the method
:py:meth:`~classification.classification.Classification.reinit_session`
with the same parameter specified to ``True``.

If you would like to know more about the login process, pelase refer
`here <https://rozvoj.fit.cvut.cz/Main/oauth2>`__.

Memorizing some ubiquitous parameters
=====================================

Looking at the API documentation, you may notice that some parameters
repeat over and over again through different requests. Luckily, you do not
need to provide them with every method call.

Together with the main client,
:py:class:`~classification.classification.Classification`,
this library offers its proxy version,
:py:class:`~classification.classificationproxy.ClassificationParamsProxy`.
It is capable of memorizing some parameters and automatically use them
if you do not provide them again explicitly. Click on this proxy object above
to jump straight to its documentation and see, what parameters you can save
and reuse. You can supply them either through the constructor or set manually
as class attributes later.

.. note:: In order to save some parameters and not supply them later
          as arguments, each of them was set as ``None`` by default
          in the proxy client. Please, keep in mind that:

          - Firstly, the order of arguments in methods of the plain client
            and its proxy version can be different. If you prefer to do without
            named arguments in Python, be sure to double check what you are
            passing to a method.
          - Secondly, if a required parameter is neither saved in proxy
            nor passed to a method explicitly,
            a :py:exc:`~classification.exceptions.MissingParameterError`
            will be raised.

Python objects to simplify request body generation
==================================================

In some methods, you will need to supply a request body. You can pass either
a Python dictionary or use our predefined objects (which will be converted
to dictionaries automatically right before an HTTP request). These objects are:

- :py:class:`~classification.entities.ClassificationTextDto`
- :py:class:`~classification.entities.ClassificationDto`
- :py:class:`~classification.entities.ExpressionParseAllRequestDto`
- :py:class:`~classification.entities.ExpressionParseRequestDto`
- :py:class:`~classification.entities.UserSettingsDto`
- :py:class:`~classification.entities.UserCourseSettingsDto`
- :py:class:`~classification.entities.StudentClassificationPreviewDto`

The main advantage of using them is that your IDE should provide hints
of parameters that should be provided and their data types. Once used
in a request, the object can be modified in any way and used again.

.. _simplified_operations:

Simplified operations
=====================

Even with the help of objects from the section above, building some very common
request bodies can be tedious. Take a look at the following methods:

- :py:meth:`~classification.classification.Classification.save_student_classifications_simple_s2t`
- :py:meth:`~classification.classification.Classification.save_student_classifications_simple_t2s`
- :py:meth:`~classification.classification.Classification.find_student_group_classifications_simple_s2t`
- :py:meth:`~classification.classification.Classification.find_student_group_classifications_simple_t2s`

They help get/save students' classifications in a simplified manner.
``s2t`` stands for the *student to tasks* format:

.. code-block:: none

    {
     'student 1 username': {'task 1': 'grade',
                            'task 2': 'grade'},
     'student 2 username': {'task 1': 'grade',
                            'task 4': 'grade'},
    }

while ``t2s`` corresponds to the *task to students* format:

.. code-block:: none

    {
     'task 1': {'student 1 username': 'grade',
                'student 2 username': 'grade'},
     'task 2': {'student 5 username': 'grade',
                'student 6 username': 'grade'},
    }

Instead of building complex objects according to the API JSON schema,
you can use the above methods with dictionaries of these formats.

.. rubric:: Footnotes

.. [1] This directory varies on different platforms. We use `appdirs <https://pypi.python.org/pypi/appdirs/1.4.3>`__
       library to get and create the correct location. On Windows, for instance,
       it could look like this: ``C:\Users\<User>\AppData\Local\fit_classification\fit_classification\saved_token``.
