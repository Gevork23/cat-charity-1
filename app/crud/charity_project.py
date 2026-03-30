from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    async def get_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> CharityProject | None:
        db_obj = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return db_obj.scalars().first()

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        db_objs = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
        )
        return list(db_objs.scalars().all())


charity_project_crud = CRUDCharityProject(CharityProject)