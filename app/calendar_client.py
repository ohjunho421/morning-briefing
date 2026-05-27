"""Google Calendar API client — fetch today's events."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from googleapiclient.discovery import build

from app.auth import get_google_credentials

logger = logging.getLogger(__name__)

KST = timezone(timedelta(hours=9))


def fetch_today_events() -> list[dict[str, Any]]:
    """Return today's calendar events sorted by start time.

    Each item: {"summary", "start", "end", "location", "all_day"}
    """
    creds = get_google_credentials()
    service = build("calendar", "v3", credentials=creds, cache_discovery=False)

    now_kst = datetime.now(KST)
    start_of_day = now_kst.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    time_min = start_of_day.isoformat()
    time_max = end_of_day.isoformat()

    logger.info("Calendar query: %s ~ %s", time_min, time_max)
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    if not events:
        logger.info("No events found for today.")
        return []

    results: list[dict[str, Any]] = []
    for ev in events:
        start_raw = ev.get("start") or {}
        end_raw = ev.get("end") or {}
        all_day = "date" in start_raw

        if all_day:
            start_str = start_raw.get("date", "")
            end_str = end_raw.get("date", "")
        else:
            start_str = _format_time(start_raw.get("dateTime", ""))
            end_str = _format_time(end_raw.get("dateTime", ""))

        results.append({
            "summary": ev.get("summary", "(no title)"),
            "start": start_str,
            "end": end_str,
            "location": ev.get("location", ""),
            "all_day": all_day,
        })

    logger.info("Fetched %d events.", len(results))
    return results


def _format_time(iso_str: str) -> str:
    """Convert ISO datetime to 'HH:MM' in KST."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str).astimezone(KST)
        return dt.strftime("%H:%M")
    except (ValueError, TypeError):
        return iso_str
