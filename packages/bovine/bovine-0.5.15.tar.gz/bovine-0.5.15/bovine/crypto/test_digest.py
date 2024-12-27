import pytest

from .digest import validate_digest, digest_multibase


@pytest.mark.parametrize(
    "headers",
    [
        {"digest": "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k="},
        {"content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:"},
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:;mooooo"
        },
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:;sound=mooo;mooo"
        },
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:,sha-new=:xx==:"
        },
        {
            "content-digest": "sha-512=:S3whoWr+QjPjztVYoyMrjTHT69+7rL7lKcuL72oBsgxRE396sAM+WNtjrE8cWloUUTlkKSoSDaGCaNGqBBj3qQ==:"
        },
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:,sha-new=:xx==:,sha-512=:S3whoWr+QjPjztVYoyMrjTHT69+7rL7lKcuL72oBsgxRE396sAM+WNtjrE8cWloUUTlkKSoSDaGCaNGqBBj3qQ==:"
        },
    ],
)
def test_validate_digest_success(headers):
    assert validate_digest(headers, b'{"cows": "good"}')


@pytest.mark.parametrize(
    "headers",
    [
        {"digest": "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k="},
        {"content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:"},
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:;mooooo"
        },
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:;sound=mooo;mooo"
        },
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:,sha-new=:xx==:"
        },
        {
            "content-digest": "sha-512=:S3whoWr+QjPjztVYoyMrjTHT69+7rL7lKcuL72oBsgxRE396sAM+WNtjrE8cWloUUTlkKSoSDaGCaNGqBBj3qQ==:"
        },
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:,sha-new=:xx==:,sha-512=:S3whoWr+QjPjztVYoyMrjTHT69+7rL7lKcuL72oBsgxRE396sAM+WNtjrE8cWloUUTlkKSoSDaGCaNGqBBj3qQ==:"
        },
    ],
)
def test_validate_digest_failure(headers):
    assert not validate_digest(headers, b'{"cows": "bad"}')


def test_digest_multibase():
    img_bytes = b"multihash"

    digest = digest_multibase(img_bytes)

    assert digest == "zQmYtUc4iTCbbfVSDNKvtQqrfyezPPnFvE33wFmutw9PBBk"
