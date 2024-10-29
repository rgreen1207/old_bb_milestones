import pytest
from app.models.award import AwardModelDB

@pytest.mark.asyncio


async def get_all():
    response = await BaseActions.get_all(
        AwardModelDB
    )
    print(response)
    print('')

    response = await BaseActions.get_all(
        AwardModelDB,
        'time_created',
        'DESC'
    )
    print(response)
    print('')

    response = await BaseActions.get_all(
        AwardModelDB,
        'time_created',
    )
    print(response)
    print('')

    response = await BaseActions.get_all(
        AwardModelDB,
        'time_created',
        'ASC'
    )
    print(response)
