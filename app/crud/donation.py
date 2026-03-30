from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationCreate]):
    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list[Donation]:
        db_objs = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(Donation.create_date)
        )
        return list(db_objs.scalars().all())


donation_crud = CRUDDonation(Donation)