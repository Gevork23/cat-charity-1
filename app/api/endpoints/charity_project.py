from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount,
    check_name_duplicate,
    check_project_before_delete,
    check_project_exists,
    check_project_not_closed,
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import close_object, invest_resources

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Get All Charity Projects',
    description='Показать список всех целевых проектов.',
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Create Charity Project',
    description='Создать целевой проект.',
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    open_donations = await donation_crud.get_not_fully_invested(session)
    invest_resources(new_project, open_donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Update Charity Project',
    description='Редактировать целевой проект.\n\n'
    'Закрытый проект нельзя редактировать;\n'
    'нельзя установить требуемую сумму меньше уже вложенной.',
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    check_project_not_closed(project)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session, project_id)

    if obj_in.full_amount is not None:
        check_full_amount(project, obj_in.full_amount)

    project = await charity_project_crud.update(project, obj_in, session)

    if (
        project.invested_amount == project.full_amount
        and not project.fully_invested
    ):
        close_object(project)

    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Delete Charity Project',
    description='Удалить целевой проект.\n\n'
    'Нельзя удалить проект, в который уже были инвестированы средства.',
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    check_project_before_delete(project)
    await charity_project_crud.remove(project, session)
    await session.commit()
    return project
