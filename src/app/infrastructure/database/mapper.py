from collections.abc import Callable, Iterable

from adaptix import Provider
from adaptix.conversion import get_converter

from app.application.errors.base import DataMapperError


def get_mapper[SrcT, DstT](
    src: type[SrcT],
    dst: type[DstT],
    *,
    recipe: Iterable[Provider] = (),
) -> Callable[[SrcT], DstT]:
    try:
        return get_converter(src, dst, recipe=recipe)
    except Exception as e:
        raise DataMapperError from e
