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
backends['radicale'] = {"type": "docker",
                        "location": "tests/backends/radicale",
                        "uri": "http://172.17.0.1:5232/",
                        "login": "toto",
                        "password": "tutu", }
