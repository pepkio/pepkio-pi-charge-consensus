"""Unit tests for pepkio-pi-charge-consensus PepkioClient."""

from __future__ import annotations

from typing import Any

import pytest

from pepkio_pi_charge_consensus.client import PepkioClient
from pepkio_pi_charge_consensus.exceptions import PepkioAPIError


class DummyResponse:
    def __init__(
        self,
        status_code: int,
        json_data: dict[str, Any] | None = None,
        reason_phrase: str = "OK",
    ) -> None:
        self.status_code = status_code
        self._json_data = json_data or {}
        self.reason_phrase = reason_phrase
        self.is_success = 200 <= status_code < 300

    def json(self) -> dict[str, Any]:
        return self._json_data


LYSOZYME_SEQ = "KVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV"  # noqa: E501


def test_client_manifest(monkeypatch: pytest.MonkeyPatch) -> None:
    manifest_data = {
        "tool_id": "pi-charge-consensus",
        "title": "pI Charge Consensus",
        "examples": [
            {
                "name": "lysozyme_single",
                "input": {
                    "tab": "single",
                    "sequence": LYSOZYME_SEQ,
                },
            }
        ],
    }

    def mock_get(url: str, **kwargs: Any) -> DummyResponse:
        assert url == "/api/tools/v1/tools/pi-charge-consensus/manifest"
        return DummyResponse(200, manifest_data)

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._http, "get", mock_get)

    manifest = client.get_manifest()
    assert manifest["tool_id"] == "pi-charge-consensus"

    examples = client.list_examples()
    assert examples == ["lysozyme_single"]

    inp = client.get_example_input("lysozyme_single")
    assert inp["tab"] == "single"
    assert "sequence" in inp

    client.close()


def test_client_run_success(monkeypatch: pytest.MonkeyPatch) -> None:
    run_response = {
        "run_id": "run-12345",
        "status": "completed",
        "result": {
            "tab": "single",
            "sequences": [{"consensus_pi": 8.8, "mw_da": 14700.53}],
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run-12345",
        "permalink": "https://tools.pepkio.com/r/run-12345",
    }

    def mock_post(url: str, json: dict[str, Any] | None = None, **kwargs: Any) -> DummyResponse:
        assert url == "/api/tools/v1/tools/pi-charge-consensus/run"
        assert json is not None
        assert json["input"]["tab"] == "single"
        return DummyResponse(200, run_response)

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._http, "post", mock_post)

    result = client.run({"tab": "single", "sequence": LYSOZYME_SEQ})
    assert result.run_id == "run-12345"
    assert result.status == "completed"
    assert result.result is not None
    assert result.result["sequences"][0]["consensus_pi"] == 8.8
    client.close()


def test_client_run_error_body(monkeypatch: pytest.MonkeyPatch) -> None:
    run_response = {
        "run_id": "run-67890",
        "status": "failed",
        "result": None,
        "error": {"message": "Invalid sequence", "code": "INVALID_INPUT"},
    }

    def mock_post(url: str, **kwargs: Any) -> DummyResponse:
        return DummyResponse(200, run_response)

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._http, "post", mock_post)

    with pytest.raises(PepkioAPIError) as exc_info:
        client.run({"tab": "single", "sequence": "123"})
    assert "Invalid sequence" in str(exc_info.value)
    assert exc_info.value.code == "INVALID_INPUT"
    client.close()


def test_client_run_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_post(url: str, **kwargs: Any) -> DummyResponse:
        return DummyResponse(
            401,
            {"error": {"message": "Invalid API key", "code": "UNAUTHORIZED"}},
            reason_phrase="Unauthorized",
        )

    client = PepkioClient(api_key="invalid_key")
    monkeypatch.setattr(client._http, "post", mock_post)

    with pytest.raises(PepkioAPIError) as exc_info:
        client.run({"tab": "single", "sequence": "KVFER"})
    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value)
    client.close()


def test_client_get_run(monkeypatch: pytest.MonkeyPatch) -> None:
    run_response = {
        "run_id": "run-abc",
        "status": "completed",
        "result": {"tab": "single"},
    }

    def mock_get(url: str, **kwargs: Any) -> DummyResponse:
        assert url == "/api/tools/v1/runs/run-abc"
        return DummyResponse(200, run_response)

    client = PepkioClient(api_key="test_key")
    monkeypatch.setattr(client._http, "get", mock_get)

    result = client.get_run("run-abc")
    assert result.run_id == "run-abc"
    assert result.status == "completed"
    client.close()
