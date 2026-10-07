from time import perf_counter

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import Base, engine, get_session
from .metrics import REQUEST_COUNT, REQUEST_LATENCY
from .models import Task, TaskStatus
from .schemas import TaskCreate, TaskRead, TaskUpdate

Base.metadata.create_all(engine)
app = FastAPI(title="TaskBoard API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.middleware("http")
async def metrics_middleware(request, call_next):
    started = perf_counter()
    response = await call_next(request)
    path = request.url.path
    REQUEST_COUNT.labels(request.method, path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, path).observe(perf_counter() - started)
    return response


@app.get("/")
async def root():
    return {"service": "taskboard", "version": app.version}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/api/tasks", response_model=list[TaskRead])
async def list_tasks(session: Session = Depends(get_session)):
    return session.scalars(select(Task).order_by(Task.id)).all()


@app.post("/api/tasks", response_model=TaskRead, status_code=201)
async def create_task(payload: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**payload.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/api/tasks/stats")
async def task_stats(session: Session = Depends(get_session)):
    counts = dict(session.execute(select(Task.status, func.count(Task.id)).group_by(Task.status)).all())
    return {"total": sum(counts.values()), **{status.value: counts.get(status.value, 0) for status in TaskStatus}}


def get_task(task_id: int, session: Session) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/api/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, payload: TaskUpdate, session: Session = Depends(get_session)):
    task = get_task(task_id, session)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = get_task(task_id, session)
    session.delete(task)
    session.commit()
