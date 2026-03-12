from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.memory.models import ActionLog, AppKnowledge, TaskHistory


async def search_tasks(session: AsyncSession, query: str, limit: int = 10) -> list[TaskHistory]:
    result = await session.execute(
        select(TaskHistory)
        .where(TaskHistory.command.contains(query))
        .order_by(TaskHistory.created_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_app_knowledge(session: AsyncSession, package_name: str) -> list[AppKnowledge]:
    result = await session.execute(
        select(AppKnowledge)
        .where(AppKnowledge.package_name == package_name)
        .order_by(AppKnowledge.updated_at.desc())
    )
    return list(result.scalars().all())


async def get_task_actions(session: AsyncSession, task_id: str) -> list[ActionLog]:
    result = await session.execute(
        select(ActionLog)
        .where(ActionLog.task_id == task_id)
        .order_by(ActionLog.step)
    )
    return list(result.scalars().all())
