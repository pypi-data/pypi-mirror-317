"""High level logic for lemmy2feed."""

import asyncio
import sys
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Optional

import httpx
import msgspec.json
import msgspec.toml
import stamina
import typer
from httpx import AsyncClient
from loguru import logger as log
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import NetworkError

from lemmy2fedi import __version__
from lemmy2fedi.config import Configuration
from lemmy2fedi.config import create_default_config
from lemmy2fedi.control import PostRecorder
from lemmy2fedi.publish import connect
from lemmy2fedi.publish import cross_post
from lemmy2fedi.publish import post_media

stamina.instrumentation.set_on_retry_hooks([])


@log.catch
async def main(config_path: Path, max_posts: int | None) -> None:
    """Read communities and post to fediverse account."""
    log.info(f"Welcome to Lemmy2Fedi({__version__})")

    if config_path.exists():
        with config_path.open(mode="rb") as config_file:
            config_content = config_file.read()
            config = msgspec.toml.decode(config_content, type=Configuration)

    else:
        config = await create_default_config()
        with config_path.open(mode="wb") as config_file:
            config_file.write(msgspec.toml.encode(config))
        print("Please review your config file, adjust as needed, and run lemmy2fedi again.")
        sys.exit(0)

    async with AsyncClient(http2=True, timeout=30) as client:
        try:
            instance: ActivityPub
            my_username: str
            instance, my_username = await connect(auth=config.fediverse, client=client)
        except NetworkError as error:
            log.info(f"Unable to connect to your Fediverse account with {error=}")
            log.opt(colors=True).info("<red><bold>Can't continue!</bold></red> ... Exiting")
            sys.exit(1)

        with PostRecorder(history_db_path=config.history_db_path) as recorder:
            statuses_posted: int = 0
            while True:
                for _i in range(config.max_crossposts):
                    await cross_post_lemmy(client=client, config=config, instance=instance, recorder=recorder)
                    statuses_posted += 1
                    if max_posts and (statuses_posted >= max_posts):
                        break

                recorder.prune(max_age_in_days=config.history_prune_age)

                if not config.run_continuously:
                    break

                if max_posts and (statuses_posted >= max_posts):
                    log.debug(f"We've created {statuses_posted} statuses. Stopping now.")
                    break

                wait_until = datetime.now(tz=UTC) + timedelta(seconds=config.delay_between_posts)
                log.opt(colors=True).info(
                    f"<dim>Waiting until {wait_until:%Y-%m-%d %H:%M:%S %z} "
                    f"({config.delay_between_posts}s) before checking again.</>"
                )
                await asyncio.sleep(delay=config.delay_between_posts)


async def cross_post_lemmy(
    client: AsyncClient,
    config: Configuration,
    instance: ActivityPub,
    recorder: PostRecorder,
) -> None:
    """Check lemmy for posts and cross post."""
    for community in config.communities:
        log.debug(f"Processing posts from {community=}")
        try:
            posts = await read_community(
                instance=community.domain_name,
                name=community.name,
                client=client,
                sort=community.sort,
                limit=community.limit,
            )
        except (httpx.ConnectError, httpx.HTTPError) as error:
            log.opt(colors=True).error(
                f"<red>Could not read community</> "
                f"<cyan>{community.domain_name}/c/{community.name}</><red> - got {error}</>"
            )
            break

        for post_dict in posts["posts"]:
            post = post_dict.get("post", {})

            if not recorder.is_duplicate(identifiers=[post.get("id"), post.get("url"), post.get("ap_id")]):
                media_id: str | None = None
                if post.get("url"):
                    media_id = await post_media(activity_pub=instance, post=post, client=client, post_recorder=recorder)

                if community.only_with_attachment and not media_id:
                    log.opt(colors=True).info(
                        f"<dim><red>Skipping</red> <cyan>{post.get('name')}</cyan> "
                        f"because it has no supported attachment - {post.get('ap_id', '')}</dim>"
                    )
                    recorder.log_post(id=post.get("id"))
                    continue

                media_ids: list[str] = []
                if media_id:
                    media_ids.append(media_id)

                await cross_post(activity_pub=instance, post=post, media_ids=media_ids, tags=community.tags)

                recorder.log_post(id=post.get("id"), url=post.get("url"), ap_id=post.get("ap_id"))

                return


def async_shim(
    config_path: Annotated[Path, typer.Argument(help="path to config file")],
    logging_config_path: Annotated[
        Optional[Path], typer.Option("-l", "--logging-config", help="Full Path to logging config file")
    ] = None,
    max_posts: Annotated[
        Optional[int], typer.Option(help="maximum number of posts and reblogs before quitting")
    ] = None,
) -> None:
    """Start async part."""
    if logging_config_path and logging_config_path.is_file():
        with logging_config_path.open(mode="rb") as log_config_file:
            logging_config = msgspec.toml.decode(log_config_file.read())

        for handler in logging_config.get("handlers"):
            if handler.get("sink") == "sys.stdout":
                handler["sink"] = sys.stdout

        log.configure(**logging_config)

    asyncio.run(main(config_path=config_path, max_posts=max_posts))


def typer_shim() -> None:
    """Run actual code."""
    try:
        typer.run(async_shim)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    typer.run(async_shim)


@stamina.retry(on=(httpx.ConnectError, httpx.HTTPError), attempts=3)
async def read_community(instance: str, name: str, client: AsyncClient, sort: str = "Hot", limit: int = 10) -> Any:
    """Read lemmy community posts with sort on Hot."""
    url = f"https://{instance}/api/v3/post/list?limit={limit}&sort={sort}&community_name={name}"
    response = await client.get(url=url)
    log.debug(f"{instance}/c/{name} - {response.status_code} - {response.headers=}")
    response.raise_for_status()

    msgspec_response = msgspec.json.decode(response.content)

    return msgspec_response
