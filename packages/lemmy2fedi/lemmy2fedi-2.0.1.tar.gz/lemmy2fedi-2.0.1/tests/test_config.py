# ruff: noqa: D100, D103, S101


from lemmy2fedi.config import Community
from lemmy2fedi.config import Configuration
from lemmy2fedi.config import Fediverse


def test_community() -> None:
    community = Community(
        domain_name="test.lemmy",
        name="lemmy-community",
        include_attachments=True,
        include_backlink=False,
        only_with_attachment=True,
    )

    assert community.tags == []
    assert community.sort == "Hot"
    assert community.limit == 10


def test_fediverse() -> None:
    fediverse = Fediverse(domain_name="fediverse.instance", api_token="token")  # noqa: S106

    assert fediverse is not None


def test_configuration() -> None:
    community = Community(
        domain_name="test.lemmy",
        name="lemmy-community",
        include_attachments=True,
        include_backlink=False,
        only_with_attachment=True,
    )
    fediverse = Fediverse(domain_name="fediverse.instance", api_token="token")  # noqa: S106

    config = Configuration(
        communities=[community],
        fediverse=fediverse,
        run_continuously=False,
        delay_between_posts=3600,
        history_db_path="/tmp/history.sqlite",  # noqa: S108
    )

    assert config.history_prune_age == 30
    assert config.max_crossposts == 1
