"""SQLite persistence for trial offers. Zero-ops local storage."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import OfferStatus, TrialOffer

DEFAULT_DB = Path.home() / ".litellm-ingestion-agent" / "trials.db"


class TrialStore:
    def __init__(self, path: Path | str = DEFAULT_DB) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS offers ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL)"
            )

    def save(self, offer: TrialOffer) -> int:
        """Persist an offer; returns its id."""
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO offers (data) VALUES (?)", (offer.model_dump_json(),)
            )
            return int(cur.lastrowid)

    def list(self, status: OfferStatus | None = None) -> list[tuple[int, TrialOffer]]:
        """All offers, optionally filtered by status, oldest first."""
        with self._connect() as conn:
            rows = conn.execute("SELECT id, data FROM offers ORDER BY id").fetchall()
        out: list[tuple[int, TrialOffer]] = []
        for row in rows:
            offer = TrialOffer.model_validate_json(row["data"])
            if status is None or offer.status == status:
                out.append((row["id"], offer))
        return out

    def set_status(self, offer_id: int, status: OfferStatus) -> None:
        """Transition an offer's status; raises KeyError if missing."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT data FROM offers WHERE id = ?", (offer_id,)
            ).fetchone()
            if row is None:
                raise KeyError(f"no offer with id {offer_id}")
            offer = TrialOffer.model_validate_json(row["data"])
            offer.status = status
            conn.execute(
                "UPDATE offers SET data = ? WHERE id = ?",
                (offer.model_dump_json(), offer_id),
            )
