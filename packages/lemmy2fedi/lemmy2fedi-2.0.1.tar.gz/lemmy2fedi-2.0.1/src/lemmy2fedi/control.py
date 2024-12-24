"""Classes and methods to control the working of Lemmy2Fedi."""

import sqlite3
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Final
from typing import TypeVar

from loguru import logger as log

CACHE_MAX_AGE_DEFAULT_30_DAYS: Final[int] = 30

PR = TypeVar("PR", bound="PostRecorder")


class PostRecorder:
    """Record posts, check for duplicates, and deletes old records of posts."""

    LAST_POST_TS: Final[str] = "last-post-timestamp"

    def __init__(self: PR, history_db_path: str) -> None:
        """Initialise PostRecord instance.

        :param history_db_path: Location where history db should be stored. Default to current directory (.)
        """
        self.history_db_file = history_db_path

        self.history_db = sqlite3.connect(database=self.history_db_file)

        # Make sure DB tables exist
        self.history_db.execute(
            "CREATE TABLE IF NOT EXISTS history "
            "(created_ts FLOAT NOT NULL PRIMARY KEY, id TEXT, url TEXT, ap_id TEXT, hash TEXT)"
            " WITHOUT ROWID"
        )
        self.history_db.execute("CREATE INDEX IF NOT EXISTS index_ts ON history(created_ts)")
        self.history_db.execute("CREATE INDEX IF NOT EXISTS index_id ON history(id)")
        self.history_db.execute("CREATE INDEX IF NOT EXISTS index_url ON history(url)")
        self.history_db.execute("CREATE INDEX IF NOT EXISTS index_ap_id ON history(ap_id)")
        self.history_db.execute("CREATE INDEX IF NOT EXISTS index_hash ON history(hash)")

        self.history_db.execute("CREATE TABLE IF NOT EXISTS settings " "(key TEXT PRIMARY KEY, value) " "WITHOUT ROWID")
        self.history_db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (:key, :value)",
            {"key": PostRecorder.LAST_POST_TS, "value": 0},
        )
        self.history_db.commit()

    def is_duplicate(self: PR, identifiers: list[str]) -> bool:
        """Check identifier can be found in log file of content posted to Mastodon."""
        log.debug(f"Checking {identifiers=}")
        for identifier in identifiers:
            cursor = self.history_db.execute(
                "SELECT * FROM history WHERE id=:id OR url=:url OR ap_id=:ap_id OR hash=:hash",
                {"id": identifier, "url": identifier, "ap_id": identifier, "hash": identifier},
            )
            if cursor.fetchone():
                log.debug(f"'{identifier}' already in DB -> duplicate detected")
                return True

        log.debug(f"'{identifiers}' not in DB -> NO duplicate")
        return False

    def log_post(
        self: PR,
        id: str | None = None,
        url: str | None = None,
        ap_id: str | None = None,
        attachment_hash: str | None = None,
    ) -> None:
        """Log details about posts that have been published."""
        timestamp = datetime.now(tz=UTC).timestamp()
        self.history_db.execute(
            "INSERT INTO history (id, url, ap_id, hash, created_ts) VALUES (?, ?, ?, ?, ?)",
            (id, url, ap_id, attachment_hash, timestamp),
        )
        self.history_db.commit()

    def get_setting(
        self: PR,
        key: str,
    ) -> Any:
        """Retrieve a setting from database."""
        cursor = self.history_db.execute(
            "SELECT value FROM settings WHERE key=:key",
            {"key": key},
        )
        row = cursor.fetchone()
        if row is None:
            return ""

        return row[0]

    def save_setting(
        self: PR,
        key: str,
        value: int | str | float,
    ) -> None:
        """Save a setting to database."""
        self.history_db.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (:key, :value)",
            {"key": key, "value": value},
        )

        self.history_db.commit()

    def prune(self, max_age_in_days: int) -> None:
        """Prune entries from db that are older than max_age_in_days."""
        log.debug(f"{max_age_in_days=}")
        max_age_ts = (datetime.now(tz=UTC) - timedelta(days=max_age_in_days)).timestamp()
        self.history_db.execute(
            "DELETE FROM history WHERE created_ts<:max_age_ts",
            {"max_age_ts": max_age_ts},
        )
        self.history_db.commit()

    def close_db(self: PR) -> None:
        """Close db connection."""
        if self.history_db:
            self.history_db.close()

    def __enter__(self):
        """Magic method to enable the use of an 'with PostRecoder(...) as ...' block."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Magic method defining what happens when 'with ...' block finishes.
        Close cache db.
        """
        self.close_db()
