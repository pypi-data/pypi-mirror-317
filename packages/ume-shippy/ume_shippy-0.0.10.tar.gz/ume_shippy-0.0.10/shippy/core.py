import os
import sys

def env_or_die(name: str) -> str:
    """Retrieve an environment variable or exit the script with an error message if it's not set."""
    value = os.getenv(name)
    if value is None:
        print(f"Error: Required environment variable '{name}' is not set.", file=sys.stderr)
        sys.exit(1)
    return value