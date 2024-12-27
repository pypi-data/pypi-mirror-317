import pytest

import json
import jsonschema

from .media import create_image, create_video, create_audio


def should_skip():
    try:
        import cv2  # noqa

        return False
    except Exception:
        print("EXCEPTION SKIPPING TESTS")
        return True


@pytest.mark.skipif(should_skip(), reason="Needs cv2 installed")
def test_image_load():
    uri = "http://local.test/image.jpg"
    result = create_image(
        "./resources/test/cow.jpg", uri, alt_text="A beautiful cow"
    ).build()

    assert result["type"] == "Image"
    assert result["url"] == uri
    assert result["width"] == 200
    assert result["mediaType"] == "image/jpeg"
    assert result["name"] == "A beautiful cow"

    with open("./resources/media.schema.json") as fp:
        schema = json.load(fp)

    jsonschema.validate(result, schema)


@pytest.mark.skipif(should_skip(), reason="Needs cv2 installed")
def test_create_video():
    uri = "http://local.test/video.mp4"
    result = create_video(
        "./resources/test/cow_eating.mp4", uri, alt_text="A beautiful cow eating"
    ).build()

    assert result["type"] == "Video"
    assert result["url"] == uri
    assert result["width"] == 256
    assert result["mediaType"] == "video/mp4"
    assert result["name"] == "A beautiful cow eating"

    with open("./resources/media.schema.json") as fp:
        schema = json.load(fp)

    jsonschema.validate(result, schema)


@pytest.mark.skipif(should_skip(), reason="Needs cv2 installed")
def test_create_multi_video():
    result = create_video(
        ["./resources/test/cow_eating.mp4", "./resources/test/cow_eating_hd.mp4"],
        ["http://local.test/video.mp4", "http://local.test/video_hd.mp4"],
        alt_text="A beautiful cow eating",
    ).build()

    assert result["type"] == "Video"
    assert result["name"] == "A beautiful cow eating"

    assert isinstance(result["url"], list)

    with open("./resources/media.schema.json") as fp:
        schema = json.load(fp)

    jsonschema.validate(result, schema)


@pytest.mark.skipif(should_skip(), reason="Needs cv2 installed")
def test_create_audio():
    uri = "http://local.test/audio.mp3"
    result = create_audio(
        "./resources/test/cow_moo.mp3", uri, alt_text="A cow mooing"
    ).build()

    assert result["type"] == "Audio"
    assert result["url"] == uri
    assert result["mediaType"] == "audio/mpeg"
    assert result["name"] == "A cow mooing"

    with open("./resources/media.schema.json") as fp:
        schema = json.load(fp)

    jsonschema.validate(result, schema)
