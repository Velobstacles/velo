Developers
==========

* `velo` uses `pyramid web framework <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_;


Coding guidelines
-----------------

Python coding guidelines are standard `PEP-8
<http://www.python.org/dev/peps/pep-0008/>`_, with the following variations:

- **No** wildcard imports (``from foo import *``). **Ever.**
- Indent your code with 4 spaces per indentation level. Tabs are forbidden.
  (SublimeText users: ``"translate_tabs_to_spaces": true``)
- Remove any trailing whitespace upon save.
  (SublimeText users: ``"trim_trailing_white_space_on_save": true``)
- Source code encoding is US-ASCII. When US-ASCII is insufficient, use UTF-8,
  not latin-1.


Unit Testing guidelines
-----------------------

velo project follows `pyramid unit testing guidelines
<http://docs.pylonsproject.org/en/latest/community/testing.html>`_


Get velo running
----------------

Mongo DB
````````

Two options:

#. Install and run ``mongodb`` locally: http://www.mongodb.org/downloads

#. Open an account on https://www.mongohq.com/ and create a (free) database


Velo
````

#. To download all necesary dependencies, in a virtualenv, run::

   (env)$ pip install -r requirements-dev.txt
   (env)$ python setup.py develop


#. Export mongo environment variables with mongo database info::

     (env)$ export MONGO_DB_NAME=<database_name>
     (env)$ export MONGO_URI=mongodb://<user>:<password>@<mongo_server_hostname>/<database_name>

#. To run tests::

     (env)$ nosetests

#. To run local server::

     (env)$ pserve development.ini --reload
