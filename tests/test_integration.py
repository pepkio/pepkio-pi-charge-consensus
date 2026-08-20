"""Integration tests against live Pepkio API endpoints."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

from pepkio_pi_charge_consensus.client import PepkioClient
from pepkio_pi_charge_consensus.config import resolve_api_key, resolve_base_url

# Search parent directories for .env if available
env_path = Path(__file__).resolve()
for parent in [env_path.parent, env_path.parent.parent, env_path.parent.parent.parent]:
    dotenv_file = parent / ".env"
    if dotenv_file.exists():
        load_dotenv(dotenv_file)
        break


@pytest.fixture
def client() -> PepkioClient:
    base_url = resolve_base_url()
    api_key = resolve_api_key(base_url=base_url)
    if not api_key:
        pytest.skip(
            f"No API key set for base_url={base_url}. Set PEPKIO_API_KEY or LOCAL_PEPKIO_API_KEY."
        )
    return PepkioClient(api_key=api_key, base_url=base_url)


def test_integration_manifest(client: PepkioClient) -> None:
    manifest = client.get_manifest()
    assert isinstance(manifest, dict)
    assert manifest.get("tool_id") == "pi-charge-consensus"
    assert "examples" in manifest


def test_integration_run_lysozyme_single(client: PepkioClient) -> None:
    inp = client.get_example_input("lysozyme_single")
    result = client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("tab") == "single"
    assert "sequences" in result.result
    seqs = result.result["sequences"]
    assert len(seqs) > 0
    assert "consensus_pi" in seqs[0]
    assert seqs[0]["consensus_pi"] > 0


def test_integration_run_insulin_b_batch(client: PepkioClient) -> None:
    inp = client.get_example_input("insulin_b_batch")
    result = client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("tab") == "batch"
    assert "sequences" in result.result
    seqs = result.result["sequences"]
    assert len(seqs) > 0
