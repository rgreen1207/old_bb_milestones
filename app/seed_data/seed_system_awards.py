from app.models.award import AwardModelDB

award_uuid_list = [
    "f8e53c5f0b9f46f08e5975d31d91f76a55a82be2f9c54da89b0b9f",
    "367c041785fa4fc9b8d2bfa49e4428d1a8dbb77318a64257b6f646",
    "54a8e604b19b4f77a24d1b3d8499571b97dc3ef9849c40a3b9e4a3",
    "06e8e7ff157147d1a8b736f64e24fc9e070d45a2a4914dc995c734",
    "e891d1e649cc4ed1aa5e4299b3941b61832f44d9b3b347b5a30d7b",
    "2016c75fe1574f189a6e6785b2db3efeb22869e4e7e549f5b8d84b",
    "f88d99d803b74f8eae87e7cb9b6d6fbf1b74c3e738d74f8ebe8e34",
    "87c749b7e4374e00bfb0d1c9d628f3a5b3b790eb43af4eb1b6f7bb"
    ]

award_names = ["Ivory", "White Gold", "Indigo", "Tiburon", "Emerald", "Ruby", "Aviator", "Iconic"]
award_values = [150, 250, 500, 1000, 2500, 5000, 10000, 25000]
award_descriptions = ["Experience Menu Only", "Experience Menu Only", "Experience Menu Only", "Build Your Own Experience (BYOE), Typically Domestic Travel", "Build Your Own Experience (BYOE), Typically Domestic Travel", "Build Your Own Experience (BYOE), International Travel", "Build Your Own Experience (BYOE), International Travel", "Build Your Own Experience (BYOE), International Travel"]

async def system_awards():
    award_seed_data = []
    for i, award in enumerate(award_uuid_list):
        award_seed_data.append(AwardModelDB(
            uuid=award,
            name=award_names[i],
            description=award_descriptions[i],
            hero_image=1,
            channel=1,
            award_type=1,
            value=award_values[i]
        )
    )
    return award_seed_data