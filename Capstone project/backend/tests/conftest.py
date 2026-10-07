import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def client(tmp_path):
    from app.database import get_session
    from app.main import app
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from app.database import Base

    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)

    async def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()
