"""
This package contains a simple ActivityPub server for
testing purposes. See [Bovine - Tutorial-Server][https://bovine.readthedocs.io/en/latest/tutorials/server/].

"""

import os
import secrets
import json
import tomli_w
import tomllib

from dataclasses import dataclass, asdict

from quart import Quart, request, send_file

from bovine import BovineActor
from bovine.activitystreams import Actor
from bovine.crypto import build_validate_http_signature, generate_rsa_public_private_key
from bovine.crypto.types import CryptographicIdentifier
from bovine.utils import webfinger_response_json

from .config import public_key as config_public_key, private_key as config_private_key


@dataclass
class ServerConfig:
    protocol: str = "http"
    hostname: str = "bovine"
    handle_name: str = "buttercup"
    public_key: str = config_public_key
    private_key: str = config_private_key

    @property
    def actor_id(self) -> str:
        """Returns the uri of the actor:

        ```pycon
        >>> ServerConfig().actor_id
        'http://bovine/actor'

        ```
        """
        return f"{self.protocol}://{self.hostname}/actor"

    @property
    def icon(self) -> str:
        """Returns the uri of the icon:

        ```pycon
        >>> ServerConfig().icon
        'http://bovine/cow'

        ```
        """
        return f"{self.protocol}://{self.hostname}/cow"

    @property
    def webfinger_response(self):
        """The expected response for a webfinger lookup

        ```pycon
        >>> ServerConfig().webfinger_response
        {'subject': 'acct:buttercup@bovine',
            'links': [{'rel': 'self',
                'type': 'application/activity+json',
                'href': 'http://bovine/actor'}]}

        ```
        """

        return webfinger_response_json(
            f"acct:{self.handle_name}@{self.hostname}", self.actor_id
        )

    def make_id(self):
        return f"{self.protocol}://{self.hostname}/" + secrets.token_urlsafe(6)

    def create_actor_object(self) -> dict:
        return Actor(
            id=self.actor_id,
            preferred_username=self.handle_name,
            name="Buttercup the exemplary bovine",
            inbox=f"{self.protocol}://{self.hostname}/inbox",
            outbox=self.actor_id,
            public_key=self.public_key,
            public_key_name="main-key",
            icon={"mediaType": "image/png", "type": "Image", "url": self.icon},
        ).build()

    def create_actor(self) -> BovineActor:
        """Returns the BovineActor"""
        return BovineActor(
            actor_id=self.actor_id,
            public_key_url=f"{self.actor_id}#main-key",
            secret=self.private_key,
        )

    def save(self, filename):
        with open(filename, "wb") as fp:
            tomli_w.dump(asdict(self), fp, multiline_strings=True)

    @staticmethod
    def load(filename):
        with open(filename, "rb") as fp:
            data = tomllib.load(fp)
        return ServerConfig(**data)

    @staticmethod
    def from_env():
        protocol = os.environ.get("BOVINE_TEST_PROTOCOL", "http")
        hostname = os.environ.get("BOVINE_TEST_HOSTNAME", "bovine")
        handle_name = os.environ.get("BOVINE_TEST_NAME", "buttercup")

        public_key, private_key = generate_rsa_public_private_key()

        return ServerConfig(
            protocol=protocol,
            hostname=hostname,
            handle_name=handle_name,
            public_key=public_key,
            private_key=private_key,
        )


def create_app(config: ServerConfig) -> Quart:
    app = Quart(__name__)
    actor = config.create_actor()
    actor_object = config.create_actor_object()

    @app.before_serving
    async def startup():
        await actor.init()

    async def fetch_public_key(url):
        result = await actor.get(url)
        return CryptographicIdentifier.from_public_key(result["publicKey"])

    verify = build_validate_http_signature(fetch_public_key)

    @app.get("/.well-known/webfinger")
    async def webfinger():
        return config.webfinger_response

    @app.get("/actor")
    async def get_actor():
        return actor_object, 200, {"content-type": "application/activity+json"}

    @app.post("/inbox")
    async def post_inbox():
        controller = await verify(request)
        if not controller:
            return "ERROR", 401

        data = await request.get_json()
        print(f"Received in inbox from {controller}")
        print(json.dumps(data, indent=2))
        print()
        return "success", 202

    @app.get("/cow")
    async def cow():
        path = "/".join(__file__.split("/")[:-1] + ["resources", "logo.png"])
        return await send_file(path)

    return app
