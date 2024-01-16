from QorpoApp.dataBase.base import Base, async_session, engine
from sqlalchemy import Column, Integer, Float, BigInteger, Text
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.future import select


class ModelAdmin:

    @classmethod
    async def create(cls, **kwargs):
        async with async_session() as session:
            async with session.begin():
                session.add(cls(**kwargs))
                await session.commit()

    @classmethod
    async def delete_all(cls):
        query = (
            sqlalchemy_delete(cls)
            .execution_options(synchronize_session="fetch")
        )
        async with async_session() as session:
            async with session.begin():
                await session.execute(query)
                await session.commit()

    @classmethod
    async def get_all(cls):
        query = select(cls)
        async with async_session() as session:
            async with session.begin():
                results = await session.execute(query)
                config = results.scalars().all()
                return config


class CurrenciesTable(Base, ModelAdmin):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    currency = Column(Text)
    date_ = Column(BigInteger)
    price = Column(Float)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
