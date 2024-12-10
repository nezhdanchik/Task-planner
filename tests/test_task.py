import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, MagicMock, AsyncMock

from api.schemas.user_schema import UserOut
from app.api.schemas.user_schema import UserCreate
from app.api.endpoints.account import get_current_user
from app.api.endpoints.main import app
from db.database import created_at, updated_at


@pytest.mark.anyio
@patch("app.api.endpoints.task.TaskDAO.create", new_callable=AsyncMock)
async def test_create_task(mock_create_task):
    app.dependency_overrides[get_current_user] = lambda: UserOut(id=1,
                                                                 login="test",
                                                                 name="test_name",
                                                                 created_at='2021-10-10 10:10:10',
                                                                 updated_at='2021-10-10 10:10:10')
    mock_create_task.return_value = {"id": 1, "title": "test_task"}
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test",
            cookies={"access_token": "valid_token"}
    ) as ac:
        response = await ac.post("/task/", json={
            "title": "test_task",
            "description": "test_description",
            "priority": "low",
        })
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "test_task"}
