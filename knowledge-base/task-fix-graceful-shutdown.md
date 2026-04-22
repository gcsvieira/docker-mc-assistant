---
id: task-fix-graceful-shutdown
type: task
status: completed
links: ["[[MOC-tasks]]", "[[MOC-debugging]]"]
---

# Task: Fix Graceful Shutdown with Docker Proxy

## Problem
The bot and the `docker-socket-proxy` were both exiting with code 137 (SIGKILL). The bot was hanging on infinite log streams and an unclosed connection pool, while the proxy was waiting for those connections to clear without a timeout.

## Fix
Implemented a multi-layered graceful shutdown strategy:
1.  **Polling**: Refactored log watching to use a non-blocking polling mechanism.
2.  **Explicit Cleanup**: Added `finally` blocks and overridden `close()` method to close the `docker-py` connection pool.
3.  **Signal Forwarding (Final Fix)**: Added `init: true` to `docker-compose.yml` to ensure signals reach the Python process.
4.  **Timeouts**: 
    - Reduced Docker client timeout to 5s.
    - Reduced HAProxy timeouts to 30s.
    - Increased Docker `stop_grace_period` to 15s.

## Implementation Details
- **docker-compose.yml**: Added `init: true` and `PYTHONUNBUFFERED=1`.
- **src/docker_ops.py**: Set global client timeout to 5s.
- **src/bot.py**: Implemented `handle_exit_signal` and tracked/cancelled background tasks.

## Verification
- Verified that both containers now stop quickly (~3s) and exit with **Code 0**.