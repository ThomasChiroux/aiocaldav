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

backends = {}

# local radicale server
backends['radicale'] = {"name": "radicale",
                        "type": "docker",
                        "location": "tests/backends/radicale",
                        "uri": "http://172.17.0.1:5232/"}

backends['radicale2'] = {"name": "radicale",
                         "type": "direct",
                         "location": "tests/backends/radicale",
                         "uri": "http://172.17.0.1:5232/"}

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
