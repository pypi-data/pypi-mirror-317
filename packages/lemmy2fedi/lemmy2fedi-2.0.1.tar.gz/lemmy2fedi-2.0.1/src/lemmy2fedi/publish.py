"""Classes and methods to publish posts to a fediverse server."""

from hashlib import sha256
from tempfile import TemporaryFile
from typing import Any

import httpx
from httpx import AsyncClient
from loguru import logger as log
from minimal_activitypub import Status
from minimal_activitypub import Visibility
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ActivityPubError
from minimal_activitypub.client_2_server import NetworkError
from stamina import retry

from lemmy2fedi.config import Fediverse
from lemmy2fedi.control import PostRecorder


async def cross_post(
    activity_pub: ActivityPub,
    post: dict[str, Any],
    media_ids: list[str] | None = None,
    tags: list[str] | None = None,
) -> None:
    """Publish lemmy post to Fediverse instance."""
    max_len = activity_pub.max_status_len
    status_text = post.get("name", "")
    if body := post.get("body"):
        status_text += f"\n\n{body}"
    if (shared_url := post.get("url")) and (not media_ids or len(media_ids) == 0):
        status_text += f"\n\n{shared_url}"

    link_text = f"\n\nOriginally found at {post.get('ap_id', '')}"
    log.debug(f"{link_text=}")

    tags_text = ""
    if tags:
        tags_text = "\n"
        for tag in tags:
            tags_text += f"#{tag} "
        tags_text = tags_text[:-1]
    log.debug(f"{tags_text=}")

    if len(status_text) + len(link_text) + len(tags_text) > max_len:
        status_text = status_text[0 : (max_len - len(link_text) - len(tags_text))]

    log.debug(
        f"Posting '{status_text}{tags_text}{link_text}' with visibility={Visibility.UNLISTED.value} and {media_ids=}"
    )
    try:
        posted_status: Status = await activity_pub.post_status(
            status=f"{status_text}{tags_text}{link_text}",
            visibility=Visibility.UNLISTED,
            media_ids=media_ids,
        )
        log.opt(colors=True).info(f"Status <cyan>{post.get('name')}</> posted at: <cyan>{posted_status.get('url')}</>")
    except ActivityPubError as error:
        log.debug(f"Encountered error when cross posting status: {error}")


async def post_media(
    activity_pub: ActivityPub,
    post: Status,
    client: AsyncClient,
    post_recorder: PostRecorder,
) -> str | None:
    """Publish media attachments an return the media_id."""
    log.debug(f"post_media({activity_pub=}, {post=}, {client=})")
    try:
        get_response = await client.get(url=str(post.get("url")))
        log.debug(f"Successfully downloaded file from {post.get('url')}")
        mime_type = str(get_response.headers.get("content-type"))
        log.debug(f"File has {mime_type=}")
    except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.NetworkError) as error:
        log.debug(f"Encountered error getting attachment ({post.get('url')}): {error=}")
        return None

    if activity_pub.supported_mime_types and mime_type not in activity_pub.supported_mime_types:
        log.debug("URL is not in supported mime-types... Skipping!")
        return None

    attachment_hash = sha256(get_response.content).hexdigest()
    if post_recorder.is_duplicate(identifiers=[attachment_hash]):
        log.debug(f"Attachment {post.get('url')} has same checksum as an attachment that has already been posted.")
        return None

    with TemporaryFile() as temp_file:
        temp_file.write(get_response.content)
        temp_file.seek(0)
        log.debug("Temporary file successfully written")

        try:
            media = await activity_pub.post_media(file=temp_file, mime_type=mime_type)
            log.debug(f"Successfully posted with response: {media}")
        except ActivityPubError as error:
            log.debug(f"Encountered error when posting media: {error}")
            return None

    post_recorder.log_post(attachment_hash=attachment_hash)

    return str(media["id"])


@retry(on=NetworkError, attempts=3)
async def connect(auth: Fediverse, client: AsyncClient) -> tuple[ActivityPub, str]:
    """Connect to fediverse instance server and initialise some values."""
    activity_pub = ActivityPub(
        instance=auth.domain_name,
        access_token=auth.api_token,
        client=client,
    )
    await activity_pub.determine_instance_type()

    user_info = await activity_pub.verify_credentials()

    log.info(f"Successfully authenticated as @{user_info['username']} on {auth.domain_name}")

    return activity_pub, user_info["username"]
