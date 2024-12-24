import json
import urllib.parse as urlparse

from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.exceptions import HTTPException
from uvicorn.server import logger

from .config import settings
from .models import IssueCommentEvent, IssueEvent, PREvent, PushEvent
from .templates import issue_card, issue_comment_card, pull_request_card, push_card
from .utils import send_to_kook, truncate

router = APIRouter()


# @router.post("/webhook")
# @router.post("/open-apis/bot/v2/hook/{lark_webhook_token}")
@router.post("/kook/{kook_channel_id}")
async def webhook(
    request: Request,
    kook_channel_id: str = None,
    background_tasks: BackgroundTasks = None,
):
    headers = request.headers

    if headers.get("content-type", None) == "application/json":
        body = await request.body()
        return await webhook_urlencoded(
            request,
            kook_channel_id=kook_channel_id,
            payload=body.decode("utf-8"),
            background_tasks=background_tasks,
        )
    elif headers.get("content-type", None) == "application/x-www-form-urlencoded":
        # decode from urlencoded
        body = await request.body()
        payload = dict(urlparse.parse_qsl(body.decode("utf-8")))
        return await webhook_urlencoded(
            request,
            kook_channel_id=kook_channel_id,
            payload=payload.get("payload", None),
            background_tasks=background_tasks,
        )
    else:
        raise HTTPException(status_code=400, detail="content-type is not supported!")


async def webhook_urlencoded(
    request: Request,
    kook_channel_id: str = None,
    payload: str = None,
    background_tasks: BackgroundTasks = None,
):
    headers = request.headers

    if kook_channel_id is None:
        raise HTTPException(status_code=400, detail="kook_channel_id cannot be None")

    x_github_event = headers.get("X-GitHub-Event", None)
    if x_github_event is None:
        return {"message": "X-GitHub-Event is None"}

    logger.debug(f"X-GitHub-Event: {x_github_event}")
    logger.debug(f"kook_channel_id: {kook_channel_id}")
    match x_github_event:
        case "push":
            params = PushEvent(**json.loads(payload))

            background_tasks.add_task(
                send_to_kook,
                kook_channel_id=kook_channel_id,
                card=push_card,
                variables={
                    "commiter": params.pusher.name,
                    "repository": params.repository.full_name,
                    "author": params.head_commit.author.name,
                    "branch": params.ref,
                    "time": params.head_commit.timestamp.split("T")[0].replace(
                        "-", "/"
                    ),
                    "commit_url": params.head_commit.url,
                    "message": truncate(params.head_commit.message),
                },
            )
        case "issues":
            params = IssueEvent(**json.loads(payload))

            background_tasks.add_task(
                send_to_kook,
                kook_channel_id=kook_channel_id,
                card=issue_card,
                variables={
                    "action": params.action.capitalize(),
                    "repository": params.repository.full_name,
                    "title": params.issue.title,
                    "message": truncate(params.issue.body),
                    "issue_url": params.issue.html_url,
                    "state": params.issue.state.capitalize(),
                    "time": params.issue.updated_at.split("T")[0].replace("-", "/"),
                    "user": params.issue.user.login,
                    "number": params.issue.number,
                },
            )
        case "issue_comment":
            params = IssueCommentEvent(**json.loads(payload))

            background_tasks.add_task(
                send_to_kook,
                kook_channel_id=kook_channel_id,
                card=issue_comment_card,
                variables={
                    "action": params.action.capitalize(),
                    "user": params.comment.user.login,
                    "number": params.issue.number,
                    "repository": params.repository.full_name,
                    "state": params.issue.state.capitalize(),
                    "time": params.comment.created_at.split("T")[0].replace("-", "/"),
                    "title": params.issue.title,
                    "message": truncate(params.comment.body),
                    "comment_url": params.comment.html_url,
                },
            )
        case "pull_request":
            params = PREvent(**json.loads(payload))

            background_tasks.add_task(
                send_to_kook,
                kook_channel_id=kook_channel_id,
                card=pull_request_card,
                variables={
                    "action": params.action.capitalize(),
                    "user": params.pull_request.user.login,
                    "number": params.number,
                    "repository": params.repository.full_name,
                    "state": params.pull_request.state.capitalize(),
                    "time": params.pull_request.updated_at.split("T")[0].replace(
                        "-", "/"
                    ),
                    "title": params.pull_request.title,
                    "head": params.pull_request.head.ref,
                    "base": params.pull_request.base.ref,
                    "pr_url": params.pull_request.html_url,
                    # "assignee": params.pull_request.assignee.login
                },
            )
        case _:
            pass

    return {"message": "recieved"}
