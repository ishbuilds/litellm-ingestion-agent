"""CLI: add-post, list, set-status, export-config."""

from __future__ import annotations

import json
import sys

import typer

from . import __version__
from .extract import extract_offer
from .litellm_config import write_config
from .models import OfferStatus
from .store import TrialStore

app = typer.Typer(help="Manage LLM trial accounts and export LiteLLM config.")


@app.command("add-post")
def add_post(
    text: str = typer.Argument(..., help="Raw post text, or '-' to read stdin."),
    source_url: str = typer.Option(None, help="URL of the original post."),
    model: str = typer.Option("gpt-4o-mini", help="LLM used for extraction."),
    yes: bool = typer.Option(False, "--yes", help="Save without confirmation."),
):
    """Extract a trial offer from post text and store it."""
    raw = sys.stdin.read() if text == "-" else text
    offer = extract_offer(raw, model=model, source_url=source_url)
    typer.echo(json.dumps(offer.model_dump(mode="json"), indent=2, default=str))
    if not yes and not typer.confirm("Save this offer?"):
        raise typer.Abort()
    offer_id = TrialStore().save(offer)
    typer.echo(f"Saved as offer #{offer_id}.")


@app.command("list")
def list_offers(status: OfferStatus = typer.Option(None, help="Filter by status.")):  # noqa: B008
    """List stored trial offers with limits at a glance."""
    for offer_id, offer in TrialStore().list(status):
        t = offer.terms
        typer.echo(
            f"#{offer_id} [{offer.status.value}] {offer.provider} / {offer.model} "
            f"(credits={t.credits_usd}, requests={t.max_requests}, days={t.duration_days})"
        )


@app.command("set-status")
def set_status(offer_id: int, status: OfferStatus):
    """Update an offer's status."""
    TrialStore().set_status(offer_id, status)
    typer.echo(f"Offer #{offer_id} -> {status.value}")


@app.command("export-config")
def export_config(output: str = typer.Option("litellm.config.yaml")):
    """Export active offers to a LiteLLM config file."""
    offers = [offer for _, offer in TrialStore().list()]
    path = write_config(offers, output)
    typer.echo(f"Wrote {path}")


@app.command("version")
def version():
    """Print the version."""
    typer.echo(__version__)


if __name__ == "__main__":
    app()
