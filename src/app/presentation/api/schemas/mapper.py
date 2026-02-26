from adaptix.conversion import convert

from app.application.errors.base import DataMapperError


def map_to[SrcT, DstT](src: SrcT, dst: type[DstT]) -> DstT:  # pyright: ignore[reportInvalidTypeVarUse]
    try:
        return convert(src, dst)
    except Exception as e:
        raise DataMapperError from e
