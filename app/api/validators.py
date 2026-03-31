from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject

NAME_ALREADY_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Объект не найден'
PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
FULL_AMOUNT_TOO_LOW = (
    'Нельзя установить значение full_amount '
    'меньше уже вложенной суммы.'
)
PROJECT_HAS_INVESTMENTS = (
    'В проект были внесены средства, не подлежит удалению!'
)


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
    project_id: int | None = None,
) -> None:
    project = await charity_project_crud.get_by_name(name, session)
    if project is not None and project.id != project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_ALREADY_EXISTS,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    return project


def check_project_not_closed(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_CLOSED,
        )


def check_full_amount(
    project: CharityProject,
    full_amount: int,
) -> None:
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FULL_AMOUNT_TOO_LOW,
        )


def check_project_before_delete(project: CharityProject) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_HAS_INVESTMENTS,
        )
