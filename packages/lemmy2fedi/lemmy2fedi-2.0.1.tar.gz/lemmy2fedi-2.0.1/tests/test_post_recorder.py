# ruff: noqa: D100, D103, S101

import pytest

from lemmy2fedi.control import PostRecorder

DB_FILE_NAME = "history.sqlite"


@pytest.fixture(scope="session")
def db_file(tmpdir_factory):
    fn = tmpdir_factory.mktemp("pytest").join(DB_FILE_NAME)
    return fn


def test_is_duplicate(db_file) -> None:
    recorder = PostRecorder(history_db_path=db_file)
    recorder.log_post(id="id", url="url", ap_id="ap_id", attachment_hash="hash")

    # test First identifier found
    assert recorder.is_duplicate(identifiers=["id", "url2", "ap_id3", "hash4"])

    # test last identifier found
    assert recorder.is_duplicate(identifiers=["id1", "url2", "ap_id3", "hash"])

    # test 'middle' identifier found
    assert recorder.is_duplicate(identifiers=["id1", "url", "ap_id3", "hash4"])

    # test none of the identifiers found
    assert not recorder.is_duplicate(identifiers=["id1", "url2", "ap_id3", "hash4"])


def test_settings(db_file) -> None:
    with PostRecorder(history_db_path=db_file) as recorder:
        recorder.log_post(id="id", url="url", ap_id="ap_id", attachment_hash="hash")
        recorder.save_setting(key="test_setting", value="test_value")

        # Test setting found
        assert recorder.get_setting(key="test_setting") == "test_value"

        # Test setting not found
        setting = recorder.get_setting(key="test_setting2")
        assert setting == ""


def test_prune(db_file) -> None:
    recorder = PostRecorder(history_db_path=db_file)
    recorder.prune(max_age_in_days=0)


def test_close_db(db_file) -> None:
    recorder = PostRecorder(history_db_path=db_file)
    recorder.log_post(id="id", url="url", ap_id="ap_id", attachment_hash="hash")
    recorder.close_db()
