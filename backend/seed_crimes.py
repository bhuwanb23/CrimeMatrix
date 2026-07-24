"""Backward-compatible entrypoint — prefer `python -m seed`. """
import sys
from seed.run import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
