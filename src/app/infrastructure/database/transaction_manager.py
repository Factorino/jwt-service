from typing import NoReturn

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.errors.base import NotFoundError, OperationFailedError
from app.application.interfaces.transaction_manager import ITransactionManager
from app.domain.errors.base import AlreadyExistsError, ValidationError


class SATransactionManager(ITransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            self._handle_exception(e)

    async def flush(self) -> None:
        try:
            await self._session.flush()
        except SQLAlchemyError as e:
            self._handle_exception(e)

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as e:
            self._handle_exception(e)

    def _handle_exception(self, exception: SQLAlchemyError) -> NoReturn:
        if isinstance(exception, IntegrityError):
            orig_error: str = str(exception.orig).lower()
            if "uq_" in orig_error or "pk_" in orig_error:
                raise AlreadyExistsError
            if "fk_" in orig_error:
                raise NotFoundError
            if "ck_" in orig_error:
                raise ValidationError

        raise OperationFailedError from exception
