---
id: gotcha-dotenv-path-discovery
type: note
links: ["[[MOC-debugging]]"]
---

# Gotcha: Dotenv Path Discovery in Flattened Docker Images

## The Problem
When using manual path calculation to find a `.env` file (e.g., `os.path.dirname(os.path.dirname(__file__))`), the logic often breaks when moving from a development environment to a Docker container.

### Example Failure
- **Development**: `src/ops.py` -> `..` -> `.env` (Works!)
- **Docker**: `/app/ops.py` (flattened) -> `..` -> `/.env` (Fails! Should be `/app/.env`)

## Symptoms
- Environment variables updated via code (e.g., `set_key`) do not persist.
- File writes occur in unexpected locations (like the root directory `/`) or fail due to permissions.
- Bot defaults to fallback values instead of saved configuration.

## Solution
Use `python-dotenv`'s built-in `find_dotenv()` function. It searches the current and parent directories automatically, making it resilient to directory flattening.

```python
from dotenv import find_dotenv, set_key
env_path = find_dotenv()
set_key(env_path, "KEY", "VALUE")
```

Additionally, always use `load_dotenv(override=True)` if you want your `.env` file changes to take precedence over environment variables already set in the shell or Docker process.
