"""Tests for the on_this_day plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.on_this_day import OnThisDayPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "on_this_day",
    "name": "On This Day",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "event_index": {
                "type": "integer",
                "title": "Event Position",
                "description": "Which event to display (1 = most notable).",
                "default": 1,
                "minimum": 1,
                "maximum": 10
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to refresh (once per day is sufficient).",
                "default": 3600,
                "minimum": 3600
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "selected": [
        {
            "text": "Apollo 11 Moon landing.",
            "year": 1969,
            "pages": [
                {
                    "title": "Apollo_11"
                }
            ]
        },
        {
            "text": "First flight of the Wright Brothers.",
            "year": 1903,
            "pages": [
                {
                    "title": "Wright_Flyer"
                }
            ]
        }
    ]
}
""")


@pytest.fixture
def plugin():
    return OnThisDayPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = OnThisDayPlugin(MANIFEST)
    p.config = json.loads("""
{
    "event_index": 1
}
""")
    return p


class TestOnThisDayPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "on_this_day"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.on_this_day.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "year" in result.data, "missing variable: year"
        assert "text" in result.data, "missing variable: text"
        assert "date" in result.data, "missing variable: date"

    @patch("plugins.on_this_day.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.on_this_day.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

