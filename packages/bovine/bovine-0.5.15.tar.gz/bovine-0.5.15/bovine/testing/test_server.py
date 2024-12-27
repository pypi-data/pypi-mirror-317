from quart import Quart

from .server import ServerConfig, create_app


def test_create_app():
    config = ServerConfig()

    app = create_app(config)

    assert isinstance(app, Quart)


def test_save_config(tmp_path):
    config = ServerConfig(handle_name="vanilla")

    config.save(tmp_path / "config.toml")

    new_config = ServerConfig.load(tmp_path / "config.toml")

    assert new_config.handle_name == "vanilla"


def test_actor_object():
    config = ServerConfig()

    actor_object = config.create_actor_object()

    assert actor_object["name"] == "Buttercup the exemplary bovine"
