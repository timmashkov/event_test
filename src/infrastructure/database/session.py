from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from infrastructure.settings.config import base_config


class AlchemySession:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url, echo=False)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def session_scope(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()


vortex = AlchemySession(url=base_config.db_url)
