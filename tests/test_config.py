"""Tests for LiteLLM config generation."""

from litellm_ingestion_agent.litellm_config import build_config
from litellm_ingestion_agent.models import OfferStatus, TrialOffer


def test_build_config_only_active_offers():
    active = TrialOffer(
        provider="AcmeAI",
        model="acme-1",
        status=OfferStatus.ACTIVE,
        env_key_name="ACMEAI_API_KEY",
    )
    dead = TrialOffer(provider="OldAI", model="old-1", status=OfferStatus.EXPIRED)
    cfg = build_config([active, dead])
    assert len(cfg["model_list"]) == 1
    entry = cfg["model_list"][0]
    assert entry["model_name"] == "AcmeAI/acme-1"
    assert entry["litellm_params"]["api_key"] == "os.environ/ACMEAI_API_KEY"
    assert "OldAI" not in str(cfg)


def test_api_base_included_when_present():
    offer = TrialOffer(
        provider="AcmeAI",
        model="acme-1",
        status=OfferStatus.SIGNED_UP,
        api_base="https://api.acme.ai/v1",
    )
    cfg = build_config([offer])
    params = cfg["model_list"][0]["litellm_params"]
    assert params["api_base"] == "https://api.acme.ai/v1"
    # Raw keys are never written — only env references.
    assert "sk-" not in str(cfg)
