from abc import ABC
from typing import Any

from sqlalchemy import Result, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.errors.base import OperationFailedError


class SABaseRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def _execute(self, query: Select) -> Result[Any]:
        try:
            return await self._session.execute(query)
        except SQLAlchemyError as e:
            raise OperationFailedError from e
