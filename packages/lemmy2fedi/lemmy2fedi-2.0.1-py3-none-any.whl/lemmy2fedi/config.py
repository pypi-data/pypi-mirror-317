"""Classes and methods to control configuration of Lemmy2Fedi."""

import msgspec
from httpx import AsyncClient
from minimal_activitypub.client_2_server import ActivityPub

from lemmy2fedi import USER_AGENT


class Community(msgspec.Struct):
    """Config values for a specific community."""

    domain_name: str
    name: str
    include_attachments: bool
    include_backlink: bool
    only_with_attachment: bool
    tags: list[str] = []
    sort: str = "Hot"
    limit: int = 10


class Fediverse(msgspec.Struct):
    """Config values for Fediverse account to cross post to."""

    domain_name: str
    api_token: str


class Configuration(msgspec.Struct):
    """Config for bot."""

    communities: list[Community]
    fediverse: Fediverse
    run_continuously: bool
    delay_between_posts: int
    history_db_path: str
    history_prune_age: int = 30  # Prune history records older than this in days
    max_crossposts: int = 1


async def create_default_config() -> Configuration:
    """Create default configuration."""
    domain_name = input("Please enter the url for your Fediverse instance: ")

    async with AsyncClient(http2=True, timeout=30) as client:
        client_id, client_secret = await ActivityPub.create_app(
            instance_url=domain_name,
            user_agent=USER_AGENT,
            client=client,
        )
        auth_url = await ActivityPub.generate_authorization_url(
            instance_url=domain_name,
            client_id=client_id,
            user_agent=USER_AGENT,
        )

        print("Please go to the following URL and follow the prompts to authorize lemmy2fedi to use your account:")
        print(f"{auth_url}")
        auth_code = input("Please provide the authorization token provided by your instance: ")

        auth_token = await ActivityPub.validate_authorization_code(
            client=client,
            instance_url=domain_name,
            authorization_code=auth_code,
            client_id=client_id,
            client_secret=client_secret,
        )

    return Configuration(
        communities=[
            Community(
                domain_name="lemmy.world",
                name="cat",
                include_attachments=True,
                include_backlink=True,
                only_with_attachment=True,
            ),
        ],
        fediverse=Fediverse(
            domain_name=domain_name,
            api_token=auth_token,
        ),
        run_continuously=False,
        delay_between_posts=300,
        history_db_path="history.sqlite",
        max_crossposts=1,
    )
