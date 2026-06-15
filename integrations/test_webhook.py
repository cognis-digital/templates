"""Tests for the webhook forwarder's validation logic."""

from __future__ import annotations

import pytest

from webhook import _parse_header, _validate_url


class TestValidateUrl:
    def test_valid_https(self) -> None:
        assert _validate_url("https://example.com/hook") == "https://example.com/hook"

    def test_valid_http(self) -> None:
        assert _validate_url("http://localhost:9200/ingest") == "http://localhost:9200/ingest"

    def test_rejects_ftp(self) -> None:
        with pytest.raises(ValueError, match="http"):
            _validate_url("ftp://example.com/x")

    def test_rejects_no_scheme(self) -> None:
        with pytest.raises(ValueError):
            _validate_url("example.com/hook")

    def test_rejects_empty(self) -> None:
        with pytest.raises(ValueError):
            _validate_url("")


class TestParseHeader:
    def test_simple_header(self) -> None:
        assert _parse_header("Authorization: Bearer tok") == ("Authorization", "Bearer tok")

    def test_value_with_colon(self) -> None:
        """Values that contain colons should be kept intact."""
        name, value = _parse_header("X-Target: http://host:8080/path")
        assert name == "X-Target"
        assert value == "http://host:8080/path"

    def test_no_colon_raises(self) -> None:
        with pytest.raises(ValueError, match="Name: Value"):
            _parse_header("BadHeaderNoColon")

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="empty name"):
            _parse_header(": SomeValue")
