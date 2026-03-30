from datetime import datetime

from app.models.base import CharityBase


def close_object(obj: CharityBase) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.utcnow()


def invest_resources(
    target: CharityBase,
    sources: list[CharityBase],
) -> None:
    for source in sources:
        if target.fully_invested:
            break

        available_amount = source.full_amount - source.invested_amount
        required_amount = target.full_amount - target.invested_amount
        transfer_amount = min(available_amount, required_amount)

        if transfer_amount <= 0:
            continue

        source.invested_amount += transfer_amount
        target.invested_amount += transfer_amount

        if source.invested_amount == source.full_amount:
            close_object(source)

        if target.invested_amount == target.full_amount:
            close_object(target)