from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.memory.models import Base

engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_task(session: AsyncSession, task_data: dict):
    from app.memory.models import TaskHistory
    task = TaskHistory(**task_data)
    session.add(task)
    await session.commit()
    return task


async def save_action(session: AsyncSession, action_data: dict):
    from app.memory.models import ActionLog
    action = ActionLog(**action_data)
    session.add(action)
    await session.commit()
    return action


async def get_recent_tasks(session: AsyncSession, limit: int = 10) -> list:
    from sqlalchemy import select
    from app.memory.models import TaskHistory
    result = await session.execute(
        select(TaskHistory).order_by(TaskHistory.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())
