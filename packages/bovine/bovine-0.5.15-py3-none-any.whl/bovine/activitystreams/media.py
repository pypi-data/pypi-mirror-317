"""
This optional package contains methods to create
objects used for media attachments. To use these
methods please run

```bash
pip install bovine[media]
```

As work on a media attachment is in progress, the
methods in this package might still change.
"""

try:
    from PIL import Image
    import cv2
    import audioread
    import isodate
except Exception:
    print("Please install media dependencies via pip install bovine[media]")

from dataclasses import dataclass
from datetime import timedelta
from typing import List

from bovine.activitystreams.object_factory import Object
from bovine.crypto.digest import digest_multibase


def file_props(filename: str):
    """
    Properties of a file

    ```pycon
    >>> file_props("./resources/test/cow.jpg")
    ('zQmVm2NjMCsrzFWFRbhQJwHNzZH8gesampoGpZcsSii12VL', 15356)

    ```
    """
    with open(filename, "rb") as fp:
        image_bytes = fp.read()

    file_size = len(image_bytes)
    digest = digest_multibase(image_bytes)

    return digest, file_size


def iso8601_duration(seconds):
    """
    Converts seconds to iso 8601 duration

    ```pycon
    >>> iso8601_duration(3789)
    'PT1H3M9S'

    ```
    """

    return isodate.duration_isoformat(timedelta(seconds=seconds))


def create_image(image_source: str, image_uri: str, alt_text: str | None = None):
    """
    Creates an Image object for the file

    ```pycon
    >>> create_image(
    ...     "./resources/test/cow.jpg",
    ...     "http://local.test/image.jpg",
    ...     alt_text="A beautiful cow").build()
    {'@context': ['https://www.w3.org/ns/activitystreams',
            'https://www.w3.org/ns/credentials/v2',
            {'size': 'https://joinpeertube.org/ns#size'}],
        'type': 'Image',
        'name': 'A beautiful cow',
        'url': 'http://local.test/image.jpg',
        'width': 200,
        'height': 164,
        'mediaType': 'image/jpeg',
        'digestMultibase': 'zQmVm2NjMCsrzFWFRbhQJwHNzZH8gesampoGpZcsSii12VL',
        'size': 15356}

    ```
    """

    digest, file_size = file_props(image_source)
    image = Image.open(image_source)

    return Object(
        type="Image",
        url=image_uri,
        height=image.height,
        width=image.width,
        media_type=image.get_format_mimetype(),
        name=alt_text,
        digest_multibase=digest,
        file_size=file_size,
    )


@dataclass
class VideoInformation:
    digest: str
    file_size: int

    duration: str
    width: int
    height: int

    @staticmethod
    def from_video_source(video_source):
        digest, file_size = file_props(video_source)

        video = cv2.VideoCapture(video_source)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps

        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return VideoInformation(
            digest=digest,
            file_size=file_size,
            duration=iso8601_duration(duration),
            width=width,
            height=height,
        )


def make_link(info, video_uri):
    return {
        "type": "Link",
        "size": info.file_size,
        "digest": info.digest,
        "width": info.width,
        "height": info.height,
        "href": video_uri,
        "mediaType": "video/mp4",
    }


def create_video(
    video_source: str | List[str], video_uri: str, alt_text: str | None = None
):
    """
    Creates a video object
    ```
    >>> create_video(
    ...     "./resources/test/cow_eating.mp4",
    ...     "http://local.test/video.mp4",
    ...     alt_text="A beautiful cow eating").build()
    {'@context':
        ['https://www.w3.org/ns/activitystreams',
        'https://www.w3.org/ns/credentials/v2',
        {'size': 'https://joinpeertube.org/ns#size'}],
        'type': 'Video',
        'name': 'A beautiful cow eating',
        'url': 'http://local.test/video.mp4',
        'width': 256,
        'height': 144,
        'mediaType': 'video/mp4',
        'digestMultibase': 'zQmSzK5qEe5tpjwGMhmjx9RvVoPkWhEmCwxP2s7wPMpKMoK',
        'size': 54373,
        'duration': 'PT3S'}

    ```

    This method also supports two video sources:

    ```
    >>> create_video(
    ...     ["./resources/test/cow_eating.mp4", "./resources/test/cow_eating_hd.mp4"],
    ...     ["http://local.test/video.mp4", "http://local.test/video_hd.mp4"],
    ...     alt_text="A beautiful cow eating").build()
    {'@context': ['https://www.w3.org/ns/activitystreams',
            'https://www.w3.org/ns/credentials/v2',
            {'size': 'https://joinpeertube.org/ns#size'}],
        'type': 'Video',
        'name': 'A beautiful cow eating',
        'url': [{'type': 'Link',
            'size': 54373,
            'digest': 'zQmSzK5qEe5tpjwGMhmjx9RvVoPkWhEmCwxP2s7wPMpKMoK',
            'width': 256,
            'height': 144,
            'href': 'http://local.test/video.mp4',
            'mediaType': 'video/mp4'},
        {'type': 'Link',
            'size': 2271723,
            'digest': 'zQme2X4rgWuRdmAtGGMSEbdoeRQ2NAL2VptcdRGTYDZbSKG',
            'width': 1920,
            'height': 1080,
            'href': 'http://local.test/video_hd.mp4',
            'mediaType': 'video/mp4'}],
        'duration': 'PT3S'}

    ```
    """

    if isinstance(video_source, list):
        video_infos = [VideoInformation.from_video_source(vs) for vs in video_source]
        links = [make_link(vi, vu) for vi, vu in zip(video_infos, video_uri)]
        digest, file_size, width, height, media_type = [None] * 5
        duration = video_infos[0].duration
    else:
        links = video_uri
        info = VideoInformation.from_video_source(video_source)
        digest, file_size = info.digest, info.file_size
        width, height = info.width, info.height
        duration = info.duration
        media_type = "video/mp4"

    return Object(
        type="Video",
        url=links,
        width=width,
        height=height,
        name=alt_text,
        digest_multibase=digest,
        file_size=file_size,
        duration=duration,
        media_type=media_type,
    )


def create_audio(audio_source: str, audio_uri: str, alt_text: str | None = None):
    """
    Creates an audio object
    ```pycon
    >>> create_audio("./resources/test/cow_moo.mp3",
    ...     "http://local.test/audio.mp3",
    ...     alt_text="A cow mooing").build()
    {'@context': ['https://www.w3.org/ns/activitystreams',
            'https://www.w3.org/ns/credentials/v2',
            {'size': 'https://joinpeertube.org/ns#size'}],
        'type': 'Audio',
        'name': 'A cow mooing',
        'url': 'http://local.test/audio.mp3',
        'mediaType': 'audio/mpeg',
        'digestMultibase': 'zQmSXTyLCPqoiGoUUwKRMKgFdddaAUkvQNr29nhB6tahb9Z',
        'size': 67709,
        'duration': 'PT2.1S'}

    ```
    """

    digest, file_size = file_props(audio_source)
    with audioread.audio_open(audio_source) as f:
        duration = f.duration
    # FIXME Wrong duration format

    return Object(
        type="Audio",
        url=audio_uri,
        name=alt_text,
        digest_multibase=digest,
        file_size=file_size,
        duration=iso8601_duration(duration),
        media_type="audio/mpeg",
    )
