"""
This package contains helpers for dealing with digest headers
in the various Fediverse settings.

See [RFC 9530 Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html)
for the current relevant RFC.
"""

import http_sf
import hashlib
import logging

from .helper import content_digest_sha256
from .multibase import multibase_58btc_encode

logger = logging.getLogger(__name__)


def validate_digest(headers: dict, body: bytes) -> bool:
    """Validates the digest. First checks the `digest` header
    then the `content-digest` header.

    ```pycon
    >>> validate_digest({"digest": "sha-256=Kch/yJ/aOjLud24QANj5EK/SfmpAubIsE9BbRcaT5D4="},
    ...     b'mooo')
    True

    >>> validate_digest({"digest": "SHA-256=Kch/yJ/aOjLud24QANj5EK/SfmpAubIsE9BbRcaT5D4="},
    ...     b'mooo')
    True

    >>> validate_digest({"content-digest": 'sha-256=:R9+ukoir89XSJSq/sL1qyWYmN9ZG5t+dXSdLwzbierw=:'},
    ...     b'moo')
    True

    ```

    :param headers: The headers of the request
    :param body: The body of the request, currently a warning is raised if body is of type str
    :return: True if digest is present and valid
    """

    if "digest" in headers:
        request_digest = headers["digest"]
        request_digest = request_digest[:4].lower() + request_digest[4:]
        digest = content_digest_sha256(body)
        if request_digest != digest:
            logger.warning("Different digest")
            return False

        return True

    if "content-digest" in headers:
        try:
            parsed = http_sf.parse(
                headers["content-digest"].encode("utf-8"), tltype="dict"
            )
        except Exception as e:
            logger.warning(
                "Failed to parse header %s with %s",
                headers["content-digest"],
                repr(e),
            )
            return False

        if len(set(parsed.keys()) - {"sha-256", "sha-512"}) > 0:
            logger.warning(
                "Got unsupported hash method in %s", headers["content-digest"]
            )

        valid = False

        if "sha-256" in parsed:
            if parsed["sha-256"][0] == hashlib.sha256(body).digest():
                valid = True
            else:
                return False

        if "sha-512" in parsed:
            if parsed["sha-512"][0] == hashlib.sha512(body).digest():
                valid = True
            else:
                return False

        return valid

    return False


def digest_multibase(obj: bytes) -> str:
    """
    Implements the multibase multihash digest, see [here](https://github.com/multiformats/multihash).
    This was proposed to use in the Fediverse in
    [FEP-ef61: Portable Objects](https://codeberg.org/fediverse/fep/src/branch/main/fep/ef61/fep-ef61.md).

    ```pycon
    >>> digest_multibase(b"multihash")
    'zQmYtUc4iTCbbfVSDNKvtQqrfyezPPnFvE33wFmutw9PBBk'

    ```
    """

    return multibase_58btc_encode(b"\x12\x20" + hashlib.sha256(obj).digest())
