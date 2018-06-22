# aiocaldav

[WARNING: THIS IS A WORK IN PROGRESS]

aiocaldav is a fork of the caldav project v0.5.0

It uses aiohttp client library instead of synchronous request lib.
It also targets only python 3.6+ (remove six and older python support)

Drawbacks:

* no DigestAuth Support for now

Bug corrections since caldav v0.5.0:

* Todo list without completed query syntax was wrong
* It was possible to completed an already completed task. Now complete() an already
  completed task does nothing (perhaps should we raise an error instead ?)
* changed datetime output in cdav to match rfc 5545 (for timezones)
* 

Evolutions since caldav v0.5.0:

* package name changed from caldav to aiocaldav

