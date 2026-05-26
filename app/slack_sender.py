"""Slack message sender — deliver briefing to a Slack channel."""

import os
import logging
from datetime import datetime, timedelta, timezone

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)

KST = timezone(timedelta(hours=9))

_KR_WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]


def send_briefing(text: str) -> bool:
    """Post the briefing message to the configured Slack channel.

    Returns True on success, False on failure.
    """
    token = os.environ["SLACK_BOT_TOKEN"]
    channel = os.environ["SLACK_CHANNEL_ID"]

    client = WebClient(token=token, timeout=30)
    now = datetime.now(KST)
    weekday_kr = _KR_WEEKDAYS[now.weekday()]
    today = f"{now.strftime('%Y-%m-%d')} ({weekday_kr})"

    try:
        result = client.chat_postMessage(
            channel=channel,
            text=f":sunrise: *모닝 브리핑* — {today}\n\n{text}",
            unfurl_links=False,
            unfurl_media=False,
        )
        logger.info(
            "Slack message sent: channel=%s, ts=%s",
            result["channel"],
            result["ts"],
        )
        return True
    except SlackApiError as e:
        logger.error("Slack API error: %s", e.response["error"])
        return False
