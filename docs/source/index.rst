.. python-caldav documentation master file, created by
   sphinx-quickstart on Thu Jun  3 10:47:52 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
 Documentation: aiocaldav |release|
===================================

Contents
========

.. toctree::
   :maxdepth: 1

   aiocaldav/davclient
   aiocaldav/objects

Python 3
========

The aiocaldav library is only compatible with python 3.6+

Quickstart
==========

.. code-block:: python

  from datetime import datetime
  import aiocaldav
  from aiocaldav.elements import dav, cdav
  
  # Caldav url
  url = "https://user:pass@hostname/caldav.php/"
  
  vcal = """BEGIN:VCALENDAR
  VERSION:2.0
  PRODID:-//Example Corp.//CalDAV Client//EN
  BEGIN:VEVENT
  UID:1234567890
  DTSTAMP:20100510T182145Z
  DTSTART:20100512T170000Z
  DTEND:20100512T180000Z
  SUMMARY:This is an event
  END:VEVENT
  END:VCALENDAR
  """

  client = caldav.DAVClient(url)
  principal = await client.principal()
  calendars = await principal.calendars()
  if len(calendars) > 0:
      calendar = calendars[0]
      print "Using calendar", calendar
  
      print "Renaming"
      await calendar.set_properties([dav.DisplayName("Test calendar"),])
      print await calendar.get_properties([dav.DisplayName(),])
  
      event = await calendar.add_event(vcal)
      print "Event", event, "created"
  
      print "Looking for events in 2010-05"
      results = await calendar.date_search(
          datetime(2010, 5, 1), datetime(2010, 6, 1))

      for event in results:
          print "Found", event

More examples
=============

See the `test code <https://github.com/ThomasChiroux/aiocaldav/tree/master/tests>`_ for more usage examples.

Notable classes and workflow
============================

 * You'd always start by initiating a :class:`aiocaldav.davclient.DAVClient`
   object, this object holds the authentication details for the
   server.

 * From the client object one can get hold of a
   :class:`caldav.objects.Principal`
   object representing the logged in principal.

 * From the principal object one can fetch / generate
   :class:`caldav.objects.Calendar` objects.  Calendar objects can also be
   instantiated directly from an absolute or relative URL and the client 
   object.

 * From the calendar object one can fetch / generate
   :class:`caldav.objects.Event` objects and
   :class:`caldav.objects.Todo` objects.  Event objects can also be
   instantiated directly from an absolute or relative URL and the client
   object.

Note that those are also available as :class:`caldav.DAVClient`,
:class:`caldav.Principal`, :class:`caldav.Calendar`,
:class:`caldav.Event` and :class:`caldav.Todo`.


Compatibility
=============

The aiocaldav test suite is run locally against radicale and DAVical for now.

Some compatibility issues have been found in caldav project listed below, search the
test code for "COMPATIBILITY" for details.  Notably;

 * You may want to avoid non-ASCII characters in the calendar name, or
   some servers (at least Zimbra) may behave a bit unexpectedly.

 * How would you expect the result to be when doing date searches
   spanning multiple instances of a recurring event?  Would you expect
   one ical object for each occurrence (and maybe that's why
   open-ended date searches tend to break at some implementations) or
   one recurring ical object?  Different servers behave a bit
   differently (but more research is needed on this one).

 * Date search for future instances or recurring events does not seem
   to work in Bedework.

 * There are some special hacks both in the code and the tests to work
   around compatibility issues in Zimbra.

 * The Radicale caldav server seems to be too radical - lots and lots
   of tests fails towards it.

 * Bedework and Zimbra does not support journal entries (but who uses those
   anyway?).

 * Bedework is supposed to support todo-lists, but queries
   for "all non-completed tasks" does not work.

 * iCloud is a bit tricky, the URL discovery part doesn't seem to work
   out very well, out of the box it seems like we get only read-only
   access.  The trick may seem to be to find alternative caldav URLs.
   This is tracked in issue
   https://github.com/python-caldav/caldav/issues/3

Unit testing
============

To start the tests code, run:

.. code-block:: bash

  $ pytest .


Documentation
=============

To build the documentation, install sphinx and run:

.. code-block:: bash

  $ python setup.py build_sphinx


====================
 Indices and tables
====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

