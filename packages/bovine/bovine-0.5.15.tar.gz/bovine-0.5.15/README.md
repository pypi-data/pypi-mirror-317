<!--
SPDX-FileCopyrightText: 2023 Helge
SPDX-FileCopyrightText: 2024 helge

SPDX-License-Identifier: MIT
-->

# Bovine

Bovine is a basic utility library for the Fediverse. It can be used both to build ActivityPub Client applications and ActivityPub Servers. In addition to [ActivityPub](https://activitypub.rocks/) support, it also provides utilities to deal with [webfinger](https://webfinger.net), nodeinfo, and HTTP Signatures.

The [bovine library](https://pypi.org/project/bovine/) can just be installed via pip

```bash
pip install bovine
```

Documentation including tutorials is available at [ReadTheDocs](https://bovine.readthedocs.io/en/latest/).

## A quick Fediverse server with docker compose

Using the [bovine docker image](https://hub.docker.com/r/helgekr/bovine), the following [docker compose file](https://codeberg.org/bovine/bovine/src/branch/main/bovine/resources/docker/docker-compose.yaml), and a service such as [ngrok](https://ngrok.com/) allowing one to expose a local port to the internet, one can create a python shell that allows one to use bovine
to interact with the Fediverse

```yml
services:
  bovine:
    image: helgekr/bovine
    environment:
    - "BOVINE_TEST_HOSTNAME=${NGROK_HOSTNAME}"
    - "BOVINE_TEST_PROTOCOL=https"
    volumes: ["bovine_shared:/bovine"]
    ports: ["5000:80"]
    command: python -mbovine.testing serve --port 80 --reload --save_config=/bovine/config.toml
  repl:
    image: helgekr/bovine
    command: python -mbovine.testing shell --load_config=/bovine/config.toml
    depends_on: [bovine]
    profiles: ["repl"]
    volumes: ["bovine_shared:/bovine"]
volumes:
  bovine_shared:
```

When using ngrok with `ngrok http 5000`, you can directly run the above file via

```bash
NGROK_HOSTNAME=$(curl --silent http://127.0.0.1:4040/api/tunnels  | jq '.tunnels[0].public_url' | sed "s|https://||g" | sed 's|"||g') docker compose run repl
```

otherwise you will have to set the variable `BOVINE_TEST_HOSTNAME` to the appropriate host.

By using

```python
>>> helge = await webfinger("acct:helge@mymath.rocks")
>>> inbox = (await actor.get(helge))["inbox"]
>>> helge
"https://mymath.rocks/endpoints/SYn3cl_N4HAPfPHgo2x37XunLEmhV9LnxCggcYwyec0"
```

one can resolve an acct uri to the actor's uri and
then record its inbox. Then one
can create a message via

```python
>>> mention = {"href": helge, "type": "Mention"}
>>> note = object_factory.note(to={helge}, content="Writing a README thus talking to myself", tag=[mention]).as_public().build()
>>> note
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "attributedTo": "https://8fc-2003-c1-c73c-a901-b426-f511-88e5-77e3.ngrok-free.app/buttercup",
    "to": ["https://mymath.rocks/endpoints/SYn3cl_N4HAPfPHgo2x37XunLEmhV9LnxCggcYwyec0", "https://www.w3.org/ns/activitystreams#Public"],
    "id": "https://8fc-2003-c1-c73c-a901-b426-f511-88e5-77e3.ngrok-free.app/HFL5hpzi",
    "published": "2024-11-24T12:30:54Z",
    "content": "Writing a README thus talking to myself",
}
```

By then running

```python
>>> await actor.post(inbox, activity_factory.create(note).build())
<ClientResponse(https://mymath.rocks/endpoints/SYONtD8yAKPapRuifwDJ8P0OhcuB7ntjkHdxh_OkrWQ) [202 None]>
```

one can post the message. It should then appear in your Fedi client

![Screenshot of the message from buttercup](./buttercup.png)

One can view messages received in the inbox via

```bash
docker compose logs -f
```

Further information on the testing server can be
found in [Using bovine with the fediverse-pasture](https://bovine.readthedocs.io/en/latest/tutorials/pasture/)
in the documentation.

## Feedback

Issues about bovine should be filed as an [issue](https://codeberg.org/bovine/bovine/issues).

## Running BDD Tests

bovine uses the [fediverse-features](https://codeberg.org/helge/fediverse-features#)
to provide BDD tests. These can be run  by first downloading the feature files
via

```bash
poetry run python -mfediverse_features
```

and then running behave

```bash
poetry run behave
```

## Contributing

If you want to contribute, you can start by working on issues labeled [Good first issue](https://codeberg.org/bovine/bovine/issues?q=&type=all&state=open&labels=110885&milestone=0&assignee=0&poster=0). The tech stack is currently based on asynchronous python, using the following components:

- [aiohttp](https://docs.aiohttp.org/en/stable/index.html) for http requests.
- [quart](https://quart.palletsprojects.com/en/latest/) as a webserver.
- [cryptography](https://cryptography.io/en/latest/).
- [pytest](https://docs.pytest.org/en/7.3.x/) for testing.
- [ruff](https://pypi.org/project/ruff/) for linting.
