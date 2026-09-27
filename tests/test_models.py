"""Tests for the TrialOffer contract."""

from litellm_ingestion_agent.models import AuthType, OfferStatus, TrialOffer


def test_offer_defaults():
    offer = TrialOffer(provider="AcmeAI", model="acme-1")
    assert offer.status == OfferStatus.DISCOVERED
    assert offer.terms.credits_usd is None
    assert offer.auth.type == AuthType.UNKNOWN


def test_example_offer_validates():
    offer = TrialOffer(
        provider="AcmeAI",
        model="acme-1",
        offer_url="https://acme.ai/trial",
        terms={
            "credits_usd": 25,
            "max_requests": None,
            "duration_days": 30,
            "notes": "credit card required",
        },
        auth={
            "type": "api_key",
            "signup_steps": ["Sign up", "Verify email", "Copy API key"],
        },
    )
    assert offer.terms.credits_usd == 25
    assert offer.auth.signup_steps[0] == "Sign up"


def test_never_invent_limits():
    # Missing limits stay null — null means "unknown", 0 means "none granted".
    offer = TrialOffer(provider="X", model="y")
    assert offer.terms.max_requests is None
    assert offer.offer_url is None
