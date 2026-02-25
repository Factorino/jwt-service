import bcrypt

from app.application.interfaces.auth.password_hasher import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):
    def hash_password(self, password: str) -> bytes:
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def verify_password(self, raw: str, hashed: bytes) -> bool:
        if not raw or not hashed:
            return False

        try:
            return bcrypt.checkpw(raw.encode(), hashed)
        except (ValueError, TypeError):
            return False
