"""CrimeMatrix database seed package.

Run from the backend directory:

    python -m seed
    python -m seed --only users,suspects,crimes
    python -m seed --list

Each module seeds one table and exports: async def seed(db) -> int
"""

__all__ = ["SEED_STEPS", "run_all"]


def __getattr__(name):
    if name in ("SEED_STEPS", "run_all"):
        from seed.run import SEED_STEPS, run_all
        return SEED_STEPS if name == "SEED_STEPS" else run_all
    raise AttributeError(name)
