import hashlib

from seed.data import USERS
from seed.utils import ensure
from app.models.user import User

# Demo password for all seeded users (not production auth)
DEFAULT_PASSWORD = "officer123"


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


async def seed(db) -> int:
    n = 0
    hashed = _hash(DEFAULT_PASSWORD)
    for row in USERS:
        _, created = await ensure(
            db, User,
            unique={"username": row["username"]},
            defaults={
                "email": row["email"],
                "hashed_password": hashed,
                "full_name": row["full_name"],
                "role": row["role"],
                "station": row["station"],
                "is_active": True,
            },
        )
        n += int(created)
    return n
