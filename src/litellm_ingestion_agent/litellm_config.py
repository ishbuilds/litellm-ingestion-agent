"""TrialOffer list -> LiteLLM config.yaml. Secrets by reference only."""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import OfferStatus, TrialOffer

_ACTIVE = {OfferStatus.ACTIVE, OfferStatus.SIGNED_UP}


def build_config(offers: list[TrialOffer]) -> dict:
    """Build a LiteLLM config dict from active offers."""
    model_list = []
    for offer in offers:
        if offer.status not in _ACTIVE:
            continue
        params: dict = {"model": offer.model}
        if offer.api_base:
            params["api_base"] = offer.api_base
        key_name = offer.env_key_name or f"{offer.provider.upper().replace(' ', '_')}_API_KEY"
        params["api_key"] = f"os.environ/{key_name}"  # resolved by LiteLLM at load
        model_list.append(
            {"model_name": f"{offer.provider}/{offer.model}", "litellm_params": params}
        )
    return {"model_list": model_list}


def write_config(offers: list[TrialOffer], path: Path | str = "litellm.config.yaml") -> Path:
    """Write the LiteLLM YAML config; returns the path written."""
    path = Path(path)
    path.write_text(yaml.safe_dump(build_config(offers), sort_keys=False))
    return path
