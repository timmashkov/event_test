from uuid import UUID

from sqlalchemy import select, update

from domain.user.schema import GetUserByLogin, UserJwtToken
from infrastructure.database.session import vortex
from .models import User


async def find_user(data: GetUserByLogin):
    """Поиск юзера"""
    async with vortex.engine.connect() as session:
        stmt = select(
            User.id,
            User.login,
            User.password,
            User.email,
        ).where(User.login == data.login)
        result = await session.execute(stmt)
        answer = result.mappings().first()
        return answer


async def change_token(data: UserJwtToken):
    """Смена токена"""
    async with vortex.engine.connect() as session:
        stmt = (
            update(User)
            .where(User.id == data.id)
            .values(token=data.token)
            .returning(User.id, User.token)
        )
        result = await session.execute(stmt)
        await session.commit()
        answer = result.mappings().first()
        return answer


async def find_token(cmd: UUID | str) -> str | None:
    """Поиск токена"""
    async with vortex.engine.connect() as session:
        stmt = select(User.token).where(User.id == cmd)
        result = await session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer
