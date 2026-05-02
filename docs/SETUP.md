# On This Day Setup Guide

Display a notable historical event that happened on today's date.

## Overview

The On This Day plugin queries the Wikimedia On-This-Day API to surface a notable historical event that occurred on today's month and day. No API key required.

- API reference: https://api.wikimedia.org/wiki/Feed_API/Reference/On_this_day

### Prerequisites

No API key required.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **On This Day**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `on_this_day` plugin variables:
   ```
   {{{ on_this_day.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `on_this_day.year` | Year the event occurred | `1969` |
| `on_this_day.text` | Short description of the event | `Moon landing` |
| `on_this_day.date` | Today's date (Month Day) | `May 1` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `event_index` | Event Position | Which event to display (1 = most notable). | `1` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to refresh (once per day is sufficient). | `3600` |

## Troubleshooting

- **No events** — some dates have fewer events; try a lower event position.
- **Network error** — verify connectivity to `api.wikimedia.org`.

