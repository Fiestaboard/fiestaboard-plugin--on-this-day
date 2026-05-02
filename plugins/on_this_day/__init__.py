"""Display a notable historical event that happened on today's date."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/{month}/{day}"
USER_AGENT = "FiestaBoard On This Day Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--on-this-day)"


class OnThisDayPlugin(PluginBase):
    """On This Day plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "on_this_day"

    def fetch_data(self) -> PluginResult:
        import datetime
        try:
            today = datetime.date.today()
            month = today.month
            day = today.day
            event_index = int(self.config.get("event_index") or 1) - 1

            url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/{month}/{day}"
            response = requests.get(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            events = data.get("selected", data.get("onthisday", []))
            if not events:
                return PluginResult(available=False, error="No events found for today")

            if event_index >= len(events):
                event_index = 0
            event = events[event_index]
            year = str(event.get("year", ""))
            text = str(event.get("text", ""))[:22]
            date_str = today.strftime("%B %-d")

            return PluginResult(
                available=True,
                data={
                    "year": year,
                    "text": text,
                    "date": date_str,
                },
            )
        except Exception as e:
            logger.exception("Error fetching on-this-day event")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
