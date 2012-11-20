Developers
==========

* `velo` uses `pyramid web framework <http://docs.pylonsproject.org/en/latest/docs/pyramid.html>`_;
* REST resources are exposed using `pyramid rest extension <http://pypi.python.org/pypi/pyramid_rest>`_;


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
- Each Python source file must start with the following line::

    from __future__ import absolute_import

The absolute_import directive serves two purposes:

- It avoids initializing modules twice (once when they're imported absolutely
  and one when they're imported relatively).
- It avoids an issue where if a module in the current package has the same
  name as one in the stdlib or in site-packages (e.g. ``foo.bar.string``),
  importing the stdlib one became impossible. With absolute_import switched on,
  ``import string`` always refers to the string module in the stdlib, and your
  module must be imported with ``from foo.bar import string``.

For more information, read `this link <http://docs.python.org/whatsnew/2.5.html#pep-328-absolute-and-relative-imports>`_.


Unit Testing guidelines
-----------------------

velo project follows `pyramid unit testing guidelines
<http://docs.pylonsproject.org/en/latest/community/testing.html>`_
