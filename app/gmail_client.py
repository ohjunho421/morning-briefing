"""Gmail API client — fetch recent emails using OAuth2 refresh token."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from googleapiclient.discovery import build

from app.auth import get_google_credentials

logger = logging.getLogger(__name__)

KST = timezone(timedelta(hours=9))

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def fetch_recent_emails(hours: int = 24, max_results: int = 20) -> list[dict[str, Any]]:
    """Return list of emails from the last *hours* hours.

    Each item: {"from", "subject", "snippet", "date"}
    """
    creds = get_google_credentials(SCOPES)
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    after_epoch = int((datetime.now(KST) - timedelta(hours=hours)).timestamp())
    query = f"after:{after_epoch}"

    logger.info("Gmail query: %s", query)
    resp = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )

    messages = resp.get("messages", [])
    if not messages:
        logger.info("No emails found in the last %d hours.", hours)
        return []

    results: list[dict[str, Any]] = []
    for msg_meta in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_meta["id"], format="metadata",
                 metadataHeaders=["From", "Subject", "Date"])
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        results.append({
            "from": headers.get("From", "(unknown)"),
            "subject": headers.get("Subject", "(no subject)"),
            "snippet": msg.get("snippet", ""),
            "date": headers.get("Date", ""),
        })

    logger.info("Fetched %d emails.", len(results))
    return results
