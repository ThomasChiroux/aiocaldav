"""aiocaldav tests configurations.

aiocaldav uses pytest and pytest-asyncio.

backends are caldav servers, either 'local' (using docker and docker-compose)
or distant (using url parameters).

This configuration file is used to activate backend servers and other tests parameters.

backends is a dict.

type parameter: either: "docker" or "url"
location: local directory containing docker-compose.yml file  (used when type="docker")
uri: caldav URI
"""
import uuid


backends = {}

backends['radicale'] = {"name": "radicale",
                        "type": "docker",
                        "location": "tests/backends/radicale",
                        "uri": "http://172.17.0.1:5232/",
                        "login": uuid.uuid4().hex,
                        "password": ""}


backends['radicale2'] = {"name": "radicale",
                         "type": "direct",
                         "location": "tests/backends/radicale",
                         "uri": "http://172.17.0.1:5232/",
                         "login": uuid.uuid4().hex,
                         "password": ""}


backends['davical'] = {"name": "davical",
                       "type": "docker",
                       "location": "tests/backends/davical",
                       "uri": "http://172.18.0.1:5232/caldav.php/",
                       "login": "admin",
                       "password": "12345", }


backends['davical2'] = {"name": "davical",
                        "type": "direct",
                        "location": "tests/backends/davical",
                        "uri": "http://172.18.0.1:5232/caldav.php/",
                        "login": "admin",
                        "password": "12345", }


backends['xandikos'] = {"name": "xandikos",
                        "type": "docker",
                        "location": "tests/backends/xandikos",
                        "uri": "http://172.17.0.1:5232/",
                        "login": "user1",
                        "password": "", }


backends['xandikos2'] = {"name": "xandikos",
                         "type": "direct",
                         "location": "tests/backends/xandikos",
                         "uri": "http://172.17.0.1:5232/",
                         "login": "user1",
                         "password": "", }


backends['cyrus'] = {"name": "cyrus",
                     "type": "docker",
                     "location": "tests/backends/cyrus",
                     "uri": "http://172.17.0.1:5232/dav/principals/user/",
                     "login": "test",
                     "password": "test", }


backends['cyrus2'] = {"name": "cyrus",
                      "type": "direct",
                      "location": "tests/backends/cyrus",
                      "uri": "http://172.17.0.1:5232/dav/principals/user/",
                      "login": "test",
                      "password": "test", }
