"""Shared Google OAuth2 credentials — single source for Gmail + Calendar."""

import os
import logging

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)


def get_google_credentials(scopes: list[str]) -> Credentials:
    """Build and refresh credentials from Railway environment variables.

    Raises RuntimeError with an actionable message on auth failure.
    """
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=scopes,
    )

    try:
        creds.refresh(Request())
    except RefreshError as e:
        logger.error(
            "Google OAuth refresh failed. The refresh token may be expired or revoked. "
            "Re-authorize and update GOOGLE_REFRESH_TOKEN in Railway. Detail: %s", e
        )
        raise RuntimeError(
            "Google refresh token expired or revoked — re-authorize OAuth"
        ) from e

    return creds
