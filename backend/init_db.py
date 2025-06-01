import asyncio
import random
from database import engine, Base, async_session, User, Task, StatusEnum, PriorityEnum

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
