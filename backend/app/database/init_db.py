import asyncio
import random

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database.schemas import Task, User, Base, StatusEnum, PriorityEnum

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@event.listens_for(engine.sync_engine, "connect")
def enforce_foreign_keys(dbapi_connection, connection_record):
    dbapi_connection.execute("PRAGMA foreign_keys=ON")

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def seed_db(session):
    user_names = ["Alice", "Bob", "Charlie", "Diana"]
    task_titles = ["Setup project", "Write docs", "Fix bugs", "Deploy app"]
    descriptions = [
        "Initial project setup",
        "Documentation writing",
        "Bug fixing and testing",
        "Deployment to production"
    ]

    users = []
    for name in user_names:
        user = User(name=name)
        session.add(user)
        users.append(user)

    await session.flush()

    for _ in range(10):
        user = random.choice(users)
        task = Task(
            title=random.choice(task_titles),
            description=random.choice(descriptions),
            status=random.choice(list(StatusEnum)),
            priority=random.choice(list(PriorityEnum)),
            user_id=user.id
        )
        session.add(task)

    await session.commit()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await seed_db(session)

if __name__ == "__main__":
    asyncio.run(init_db())
