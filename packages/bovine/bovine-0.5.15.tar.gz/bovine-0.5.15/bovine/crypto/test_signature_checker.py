# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

import pytest
from unittest.mock import AsyncMock

from .signature_checker import SignatureChecker


@pytest.mark.parametrize(
    "headers",
    [
        {"digest": "sha-256=xxxxx"},
        {"content-digest": "sha-new=:xx==:"},
        {"content-digest": "sha-256=:xx==:"},
        {"content-digest": "sha-256=:xx=:"},
        {"content-digest": "invalid"},
        {
            "content-digest": "sha-256=:MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=:,sha-new=:xx==:,sha-512=:xx==:"
        },
    ],
)
def test_validate_digest_failure(headers):
    checker = SignatureChecker(key_retriever=AsyncMock())

    assert not checker.validate_digest(headers, b'{"cows": "good"}')
