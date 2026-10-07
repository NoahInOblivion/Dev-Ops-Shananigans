import pytest


pytestmark = pytest.mark.anyio


async def test_health_and_root(client):
    assert (await client.get("/health")).json() == {"status": "ok"}
    assert (await client.get("/")).json()["service"] == "taskboard"


async def test_list_tasks_starts_empty(client):
    response = await client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_task_rejects_blank_title(client):
    response = await client.post("/api/tasks", json={"title": "  "})
    assert response.status_code == 422


async def test_stats_include_each_status(client):
    await client.post("/api/tasks", json={"title": "Ship"})
    await client.post("/api/tasks", json={"title": "Review", "status": "DONE"})
    response = await client.get("/api/tasks/stats")
    assert response.status_code == 200
    assert response.json() == {"total": 2, "TODO": 1, "IN_PROGRESS": 0, "DONE": 1}


async def test_update_task_status_persists(client):
    task_id = (await client.post("/api/tasks", json={"title": "Ship"})).json()["id"]
    response = await client.put(f"/api/tasks/{task_id}", json={"status": "IN_PROGRESS"})
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"
    assert (await client.get("/api/tasks")).json()[0]["status"] == "IN_PROGRESS"


async def test_delete_task_and_missing_task(client):
    task_id = (await client.post("/api/tasks", json={"title": "Delete me"})).json()["id"]
    assert (await client.delete(f"/api/tasks/{task_id}")).status_code == 204
    assert (await client.delete(f"/api/tasks/{task_id}")).status_code == 404
