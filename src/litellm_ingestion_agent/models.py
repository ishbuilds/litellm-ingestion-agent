"""Pydantic schemas — the executable version of docs/EXTRACTION_CONTRACT.md."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OfferStatus(str, Enum):
    DISCOVERED = "discovered"
    SIGNED_UP = "signed_up"
    ACTIVE = "active"
    EXPIRED = "expired"
    EXHAUSTED = "exhausted"


class AuthType(str, Enum):
    API_KEY = "api_key"
    OAUTH = "oauth"
    UNKNOWN = "unknown"


class TrialTerms(BaseModel):
    credits_usd: Optional[float] = Field(default=None, ge=0)
    max_requests: Optional[int] = Field(default=None, ge=0)
    duration_days: Optional[int] = Field(default=None, ge=0)
    notes: str = ""


class AuthInfo(BaseModel):
    type: AuthType = AuthType.UNKNOWN
    signup_steps: list[str] = Field(default_factory=list)


class TrialOffer(BaseModel):
    provider: str
    model: str
    offer_url: Optional[str] = None
    source_post_url: Optional[str] = None
    source_text: str = ""
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    terms: TrialTerms = Field(default_factory=TrialTerms)
    auth: AuthInfo = Field(default_factory=AuthInfo)
    api_base: Optional[str] = None
    status: OfferStatus = OfferStatus.DISCOVERED
    env_key_name: Optional[str] = None
