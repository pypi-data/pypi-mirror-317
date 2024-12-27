"""Errors raised by the Fixpoint SDK."""

__all__ = ["FixpointError", "FixpointApiError"]

import json
from typing import Any

import httpx


class FixpointError(Exception):
    """Base class for all Fixpoint errors."""


class FixpointApiError(FixpointError):
    """An error raised when a request to the Fixpoint API fails."""

    status_code: int
    detail: Any

    def __init__(self, msg: str, status_code: int, detail: Any):
        json_msg: str
        try:
            json_msg = json.dumps(detail, indent=2)
        except json.JSONDecodeError:
            json_msg = str(detail)
        new_msg = "\n".join([msg, "", json_msg])
        super().__init__(new_msg)
        self.status_code = status_code
        self.detail = detail


def raise_for_status(resp: httpx.Response) -> None:
    """Raise an exception if the response has a non-2xx status code."""
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        error_detail: Any
        try:
            error_detail = resp.json()
        except Exception:  # pylint: disable=broad-exception-caught
            error_detail = resp.text
        raise FixpointApiError(
            str(exc), detail=error_detail, status_code=resp.status_code
        ) from exc
