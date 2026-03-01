from abc import abstractmethod
from typing import Protocol


class Interactor[InputDTO, OutputDTO](Protocol):
    @abstractmethod
    async def execute(self, request: InputDTO) -> OutputDTO: ...
