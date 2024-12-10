import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.api.endpoints.main import app

from app.api.endpoints.account import get_current_user
@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}

#
@pytest.mark.anyio
@patch("app.api.endpoints.account.jwt.decode", new_callable=MagicMock)
@patch("app.api.endpoints.account.UserDAO.get_one_or_none", new_callable=AsyncMock)
async def test_get_current_user(mock_get_one_or_none, mock_jwt_decode):
    mock_jwt_decode.return_value = {"sub": 1}
    mock_get_one_or_none.return_value = {"id": 1, "login": "test"}
    result = await get_current_user("valid_token")
    assert result == {"id": 1, "login": "test"}