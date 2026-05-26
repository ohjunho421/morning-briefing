"""Morning Briefing — Railway cron entry point.

Runs once per invocation:
1. Fetch Gmail emails (last 24h)
2. Fetch Google Calendar events (today)
3. Summarize via Claude API
4. Send to Slack
"""

import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("morning-briefing")


def _check_env() -> list[str]:
    """Return list of missing required environment variables."""
    required = [
        "GOOGLE_REFRESH_TOKEN",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "ANTHROPIC_API_KEY",
        "SLACK_BOT_TOKEN",
        "SLACK_CHANNEL_ID",
    ]
    return [k for k in required if not os.environ.get(k)]


def run() -> None:
    """Execute the full briefing pipeline."""
    missing = _check_env()
    if missing:
        logger.error("Missing environment variables: %s", ", ".join(missing))
        sys.exit(1)

    # --- 1. Gmail ---
    logger.info("=== Step 1: Fetching Gmail ===")
    try:
        from app.gmail_client import fetch_recent_emails
        emails = fetch_recent_emails(hours=24, max_results=20)
        logger.info("Gmail: %d emails found.", len(emails))
    except Exception:
        logger.exception("Gmail fetch failed.")
        emails = []

    # --- 2. Calendar ---
    logger.info("=== Step 2: Fetching Calendar ===")
    try:
        from app.calendar_client import fetch_today_events
        events = fetch_today_events()
        logger.info("Calendar: %d events found.", len(events))
    except Exception:
        logger.exception("Calendar fetch failed.")
        events = []

    # --- 3. Summarize ---
    logger.info("=== Step 3: Generating briefing via Claude ===")
    try:
        from app.summarizer import build_briefing
        briefing = build_briefing(emails, events)
    except Exception:
        logger.exception("Claude summarization failed.")
        briefing = _fallback_briefing(emails, events)

    # --- 4. Slack ---
    logger.info("=== Step 4: Sending to Slack ===")
    try:
        from app.slack_sender import send_briefing
        ok = send_briefing(briefing)
    except Exception:
        logger.exception("Slack send failed with unexpected error.")
        ok = False

    if ok:
        logger.info("Morning briefing delivered successfully!")
    else:
        logger.error("Failed to deliver briefing to Slack.")
        sys.exit(1)


def _fallback_briefing(emails: list, events: list) -> str:
    """Plain-text fallback when Claude API is unavailable."""
    lines = [":warning: *모닝 브리핑* (Claude 요약 실패 — 원본 데이터)\n"]

    lines.append("*:email: Gmail*")
    if not emails:
        lines.append("새로운 메일이 없습니다.\n")
    else:
        for i, em in enumerate(emails, 1):
            lines.append(f"{i}. {em.get('from', '?')} — {em.get('subject', '?')}")
        lines.append("")

    lines.append("*:calendar: Calendar*")
    if not events:
        lines.append("오늘 일정이 없습니다.")
    else:
        for ev in events:
            lines.append(f"- {ev.get('start', '?')} {ev.get('summary', '?')}")

    return "\n".join(lines)


if __name__ == "__main__":
    run()
