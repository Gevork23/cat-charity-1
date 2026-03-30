from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import invest_resources

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    summary='Get All Donations',
    description='Показать список всех пожертвований.',
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    summary='Create Donation',
    description='Создать пожертвование.',
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(donation, session)
    open_projects = await charity_project_crud.get_not_fully_invested(session)
    invest_resources(new_donation, open_projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation