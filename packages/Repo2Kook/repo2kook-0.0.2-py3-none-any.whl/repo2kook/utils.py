import base64
import hashlib
import hmac
import json as jsonlib

import httpx
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.types import Message
from uvicorn.server import logger

from .config import settings


def format_card(card, variables):
    if isinstance(card, dict):
        return {k: format_card(v, variables) for k, v in card.items()}
    elif isinstance(card, list):
        return [format_card(elem, variables) for elem in card]
    elif isinstance(card, str):
        return card.format(**variables)
    else:
        return card


def verify_signature(payload_body, secret_token, signature_header) -> None:
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise HTTPException(
            status_code=403, detail="x-hub-signature-256 header is missing!"
        )
    hash_object = hmac.new(
        secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")


def gen_sign(timestamp, secret):
    # 拼接 timestamp 和 secret
    string_to_sign = "{}\n{}".format(timestamp, secret)
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


async def send_to_kook(
    kook_channel_id: str, card: dict | list, variables: dict
) -> None:
    """Send card message to Kook."""

    card = format_card(card, variables)

    json = {
        "type": 10,
        "target_id": kook_channel_id,
        "content": jsonlib.dumps(card),
    }

    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(
            f"{settings.kook_api_base_url}/message/create",
            json=json,
            headers={"Authorization": f"Bot {settings.kook_token}"},
        )

        if res.status_code != 200:
            logger.error(f"Failed to send message to Kook: {res.text}")
            raise HTTPException(
                status_code=500, detail="Failed to send message to Kook"
            )


def truncate(text: str, length: int = 80) -> str:
    """Truncate text to a certain length.

    Args:
        text: text to truncate
        length: length to truncate to

    Returns:
        Truncated text.
    """
    if text is None:
        return ""
    if len(text) > length:
        return text[: length - 3] + "..."
    return text


async def get_body(request: Request) -> bytes:
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    body = await request.body()
    request._receive = receive
    return body
