from tortoise import Tortoise


async def init_database():
    await Tortoise.init(
        db_url='postgres://postgres:postgres@127.0.0.1:5432/db_promotions',
        modules={'models': ['app.models']}
    )

    await Tortoise.generate_schemas()
