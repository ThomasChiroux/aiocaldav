# aiocaldav

aiocaldav is a fork of the caldav project since v0.5.0

It uses aiohttp client library instead of synchronous request lib.
It also targets only python 3.6+ (remove six and older python support)

## Drawbacks

* no DigestAuth Support for now

## Bug corrections since caldav v0.5.0

* Todo list without completed query syntax was wrong
* It was possible to completed an already completed task. Now complete() an already
  completed task does nothing (perhaps should we raise an error instead ?)
* changed datetime output in cdav to match rfc 5545 (for timezones)
* 

Evolutions since caldav v0.5.0 (incompatible change in top of 'asyncification')

* package name changed from caldav to aiocaldav
* Principal.calendar_home_set is no longer a property, it's now a async method
  To set the prop, now use Principal._calendar_home_setter(url)
  To retrieve is use await Principal.calendar_home_set()

## Tests

Tests uses pytest and pytest_asyncio and need (by default) docker and docker-compose.
Just run: 

```
$ pytest .
```

to launch the tests.
It will build the necessary docker images.
At the first launch, it could take a lot of time to build the images (especially for the cyrus image which need compilation)

### to test against a specific backend, you can use pytest cli options:

```
$ pytest --only-backend-radicale .
```


```
$ pytest --only-backend-davical .
```


```
$ pytest --only-backend-xandikos .
```


```
$ pytest --only-backend-cyrus .
```

### to exclude a backend, you can use this pytest cli options:

* --no-backend-radicale
* --no-backend-davical
* --no-backend-xandikos
* --no-backend-cyrus

(note: xandikos is not included in the default test suite for now)

