bouncestudio is a wrapper around the BoogieTools BounceStudio library
(http://www.boogietools.com/Products/Linux/). While this wrapper is 
provided freely, please note that BoogieTools Bounce studio is not.

INSTALLATION
============
::
  $ python setup.py install

USAGE
=====

bouncestudio.Bounce() requires a raw DSN string as well as a license for
certain functions. bouncestudio.Bounce().bounce_check is the primary
function and returns a named tuple, consisting of the numeric DSN type,
verbose bounce information, and the bounced email address. Keep in mind that
the numeric and verbose bounce info is BounceStudio's standard interpretation.

::
  >>> import bouncestudio
  >>> raw_dsn = open("/path/to/dsn.email", "r").read()
  >>> bounce = bouncestudio.Bounce(dsn=raw_dsn, license="license string")
  >>> bounce.bounce_check()
