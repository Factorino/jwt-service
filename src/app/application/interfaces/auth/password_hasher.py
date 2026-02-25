from abc import abstractmethod
from typing import Protocol


class IPasswordHasher(Protocol):
    @abstractmethod
    def hash_password(self, password: str) -> bytes: ...

    @abstractmethod
    def verify_password(self, raw: str, hashed: bytes) -> bool: ...

