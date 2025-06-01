import asyncio
from typing import List, Dict
from database import Task as TaskDB, User as UserDB, get_session
from models import Task as TaskModel, User as UserModel, CreateTask, CreateUser

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

notifications: Dict[int, List[str]] = {}
active_connections: Dict[int, List[WebSocket]] = {}

async def notify_user(user_id: int, message: str):
    notifications.setdefault(user_id, []).append(message)
    conns = active_connections.get(user_id, []) + active_connections.get(0, [])
    disconnected = []
    for ws in conns:
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        conns.remove(ws)

async def send_notification(msg: str, user_id: int):
    await notify_user(user_id, msg)

@app.websocket("/ws/notifications")
async def global_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.setdefault(0, []).append(websocket)
    try:
        while True:
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        active_connections[0].remove(websocket)


@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(
    user_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session)
    ):
    query = select(TaskDB)
    if user_id is not None:
        query = query.where(TaskDB.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()

@app.get("/tasks/{task_id}", response_model=TaskModel)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    result = await session.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="User not found")
    return task

@app.post("/tasks", response_model=TaskModel)
async def create_task(
    task: CreateTask,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
    ):
    user_result = await session.execute(select(UserDB).where(UserDB.id == task.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User ID does not exist")
    db_task = TaskDB(**task.dict())
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    background_tasks.add_task(send_notification, user_id=db_task.user_id, msg=f"New Task was created with id: {db_task.id}")
    return db_task

@app.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task: CreateTask,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
    ):
    result = await session.execute(select(TaskDB).where(TaskDB.id == task_id))
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)

    await session.commit()
    background_tasks.add_task(send_notification, user_id=db_task.user_id, msg=f"Task was updated with id: {db_task.id}")
    return {"message": "Updated"}

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
    ):
    result = await session.execute(select(TaskDB).where(TaskDB.id == task_id))
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(db_task)
    await session.commit()
    background_tasks.add_task(send_notification, user_id=db_task.user_id, msg=f"Task was deleted with id: {task_id}")
    return {"message": "Deleted"}

@app.get("/users", response_model=List[UserModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UserDB))
    return result.scalars().all()

@app.get("/users/{user_id}", response_model=UserModel)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
    ):
    result = await session.execute(select(UserDB).where(UserDB.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=UserModel)
async def create_user(
    user: CreateUser,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    ):
    db_user = UserDB(**user.dict())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    background_tasks.add_task(send_notification,user_id=db_user.id, msg=f"New User was added with id: {db_user.id}")
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
    ):
    result = await session.execute(select(UserDB).where(UserDB.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(db_user)
    await session.commit()
    background_tasks.add_task(send_notification, user_id=db_user.id, msg=f"User was deleted with id: {user_id}")
    return {"message": "Deleted"}
