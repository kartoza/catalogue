SANSA-EO Catalogue Coding Standards
===================================

.. note:: This document is based on Linfiniti Consulting CC. coding standards document.


Coding Standards
================

Code Style
----------

Please observe the following coding standards when working on the codebase:

* **Docstrings** should be enclosed in three double quotes :samp:`"""`
* **Pep8**: Coding must follow a style guide. In case of Python it is
  `pep8 <http://www.python.org/dev/peps/pep-0008>`_ and
  using the command line tool pep8 (or :samp:`make pep8`) to enforce this
* **pep257:** `Python documentation guide <http://www.python.org/dev/peps/pep-0257>`_
* **String literals:** String literals should be enclosed in single quotes :samp:`'foo'` and not
  `"foo"`
* **Line continuation**  should be done using brackets not slashes e.g.::

   myString = ('Very long'
              'string')

   not:

   myString = 'Very long' \
              'string'

* In cases where you need to wrap you should align parameters e.g.::

      myNewReffedPath = os.path.join(
          myThumbOutputPath,
          self.product_id + '-reffed.jpg')


* Use single blank lines to separate logic in a function e.g::

   foo = 1
   bar = 2

   result = foo * bar

* Place comments above the relevant line not at the end of it as far as
  far as possible::

   # Collect all data from input port
   myData = some.obscure.function()

* Don't use 'magic' numbers - your code should provide semantic meaning to the
  reader. Bad::

    myResult = foo(12)  # what is 12?

  Good::

    myHouseCount = 12  # ok now it is obvious
    myResult = foo(theValue=myHouseCount)

* Call functions using named arguments. Bad::

     myResult = foo(myHouseCount)

  Good::

     myResult = foo(theValue=myHouseCount)



Standard headers and documentation
----------------------------------

We aim to produce self documenting code.

* Each source file should include a standard header containing copyright,
  authorship and version metadata as shown in the exampled below.

**Example standard header**::

   """
   SANSA-EO Catalogue - Views.py - implements views as per MVC design pattern

   Contact : lkleyn@sansa.org.za

   .. note:: This program is the property of the South African National Space
      Agency (SANSA) and may not be redistributed without expresse permission.
      This program may include code which is the intellectual property of
      Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
      license to use any code contained herein which is the intellectual property
      of Linfiniti Consulting CC.

   """

   __author__ = 'tim@linfiniti.com'
   __version__ = '0.2.1'
   __date__ = '10/01/2011'
   __copyright__ = 'South African National Space Agency'


* **Method Docstrings:** Each method should include a docstring which includes a short one line description
  of the method, detailed description (where appropriate), and then a list of input,
  output and exceptions as per the example below. Note that ReSTructured Text may
  be used in this docstring to improve readability.

  **Example method docstring**::

  def translate(self, theString):
      """
      One line description.

      Additional notes.

      Args:
          theString str - Required. String for translation.
      Returns:
          str - Translated version of theString.
      Raises:
          no exceptions explicitly raised.
      """

  The arguments should be followed by their type and then an indication of
  whether the argument is optional or required.

Import management
-----------------

* **Explicit imports:** Wildcard imports are not allowed - they make it difficult
  to follow application logic. Rather one of the following two schemes should
  be followed::

   from foo import (bar,
                   alpha,
                   beta)

   or

   import foo
   myAlpha = foo.alpha

  The first form is preferred.

DRY:
----

* If you use a few lines of code in more than one place, refactor them into
  their own function.
* If you use a literal string or expression in more than one place, refactor
  it into a function or variable.

Variables
---------

* **Unused imports:** Unused imports are not allowed. They should either be
  commented out or removed from the source code.
* **Unused variables:** Unused variables are not allowed. They should either
  be commented out or removed from the source code. In some cases where the
  above are not possible, use del to clear them .e.g. del fooUnusedVar
  or you should use the semantic trick of assigning the variable the name '_'
  in order for it to be silently ignored. e.g. :samp:`_ = 50 * 50`.
* **Variable abbreviation:** Variable acronyms are not allowed. e.g. mxincrval
  should be written as maximumIncrementValue.
* **Variable Naming:** Variables need to follow the following specific
  naming convention:
  * **Globals:** All caps, underscore separated e.g. :samp:`MAXIMUM_VALUE`
  * **Class members:** camel case, unprefixed, no abbreviations e.g. :samp:`sensorAngle`
  * **Method / Function arguments:** camel case, prefixed with 'the', no abbreviations
    e.g. :samp:`theSensorName`
  * **Variables with method/function scope:** camel case, prefixed with 'my', no
    abbreviations e.g. :samp:`myCounter`
* **Exceptions:** In some cases these rules can be broken in particular the use of
  python conventions such as 'self','kwargs' etc. Also using the acronym 'Id' for
  identifier is acceptible.
* **File naming:** files and directories (modules and packages in python parlance)
  should be lower case, underscore separated, no abbreviations e.g.
  :samp:`test_utilities.py`
* **Code verbosity:** prefer verbose code to condensed but hard to understand code.
* **Code provenance:** never mix code into the code base that is not licensed under
  e.g. BSD or similar completely public domain license. If you need to include GPL
  or more restrictive licesed code, it should be included as it's own module with
  appropriate license information in the header.
* **Undocumented API's:** Do not use undocumented API's from libraries (e.g. django)
* **Unit test:**
  * No code should added without an accompanying unit test.
  * No code should be modified without (if needed) a new unit test.
  * No code should be committed to master or live branches without all tests passing.
* **Leaving things better than you found them:** if you work on a method / function
  and it doesn't already comply with these conventions, it is required that you
  refactor it so that every function after being touched

**HTML, Javascript and CSS**

For the most part the items above apply equally to javascript and css/html. Here are a couple of extra guidelines:

* **Element Id:** Element identifiers should be written in the form
  ``search-box`` with no abbreviation, dash separated. The name should have
  semantic meaning.
* **Class Id:** Class identifiers should be written in the form
  ``search-box`` with no abbreviation, dash separated. The name should have
  semantic meaning.


**File Names**

* **javascript:** Lower case dash separated e.g. ``catalogue-utilities.js``
* **python:** Lower case underscore separated with no abbreviations e.g.
  ``catalogue_utilities.py``
* **css:** Lower case dash separated e.g. ``catalogue_utilities.css``
* **html:** Lower case dash separated e.g. ``catalogue-index.html``


Unit testing and quality control
--------------------------------

* All code should pass lint validation. You can test this using the make target
  ``scripts/lint-check.sh``. In some cases you may wish to override a line or
  group of lines so that they are not validated by lint. You can do this by
  adding either::

     import foo  # pylint: diable=W1203

  or::

     # pylint: disable=W1234
     print 'hello'
     print 'goodbye'
     # pylint: enable=W1234

  The relevant id (W1234) is provided on the output of the above mentioned lint
  command's output.
* No code should added without an accompanying unit test.
* No code should be modified without (if needed) a new unit test.
* No code should be committed to master or live branches without all tests passing.
* Code parsimony: Less code is better than more code (i.e. don't keep unused
  code laying about in the code base because you think it may be useful one
  day).
* Code verbosity: Prefer verbose code to condensed but hard to understand code.

* Leaving things better than you found them: if you work on a method / function
  and it doesn't already comply with these conventions, it is required that you
  refactor it so that every function after being touched does comply with these
  rules.

* To execute **pylint** tool using project specific pylintrc config file, in
  ``sac_catalogue`` top level folder run::

    pylint --rcfile=pylintrc_config catalogue/views/others.py

Legal stuff
-----------

* Code provenance: never mix code into the code base that is not licensed under
  e.g. BSD or similar completely public domain license. If you need to include GPL
  or more restrictive licensed code, it should be included as it's own module with
  appropriate license information in the header.
* Undocumented API's: Do not use undocumented API's from libraries (e.g. django)




