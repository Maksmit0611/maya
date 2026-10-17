"""Create a keyless local sample project after database migrations."""

import asyncio

from sqlalchemy import select

from app.core.config import get_settings
from app.core.db import make_session_factory
from app.models import Brief, Project, ProjectMember, Room


async def seed() -> None:
    settings = get_settings()
    engine, factory = make_session_factory(settings.database_url)
    async with factory() as session:
        existing = await session.scalar(
            select(Project).where(Project.owner_id == "dev-user").limit(1)
        )
        if existing:
            print(f"Seed project already exists: {existing.id}")
        else:
            project = Project(owner_id="dev-user", name="MAYA sample home")
            session.add(project)
            await session.flush()
            session.add(ProjectMember(project_id=project.id, user_id="dev-user", role="owner"))
            room = Room(project_id=project.id, name="Sunlit living room", room_type="living room")
            session.add(room)
            await session.flush()
            session.add(
                Brief(
                    project_id=project.id,
                    room_id=room.id,
                    version=1,
                    content={
                        "style": "Warm contemporary",
                        "budget": "Not specified",
                        "constraints": "Keep existing floor",
                    },
                    created_by="dev-user",
                )
            )
            await session.commit()
            print(f"Seeded project: {project.id}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
