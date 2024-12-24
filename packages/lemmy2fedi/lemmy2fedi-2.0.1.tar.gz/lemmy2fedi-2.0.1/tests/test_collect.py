# ruff: noqa: D100, D103, S101

import pytest
from httpx import AsyncClient
from httpx import HTTPStatusError
from pytest_httpx import HTTPXMock

from lemmy2fedi.app import read_community


@pytest.mark.asyncio
async def test_successful_read() -> None:
    client = AsyncClient(http2=True)

    result = await read_community(instance="lemmy.world", name="cat", client=client)

    assert result is not None


@pytest.mark.asyncio
@pytest.mark.httpx_mock(can_send_already_matched_responses=True)
async def test_unsuccessful_read(httpx_mock: HTTPXMock) -> None:
    client = AsyncClient(http2=True)

    httpx_mock.add_response(status_code=404)

    with pytest.raises(HTTPStatusError):
        _result = await read_community(instance="lemmy.world", name="cat", client=client)
