---
id: gotcha-docker-proxy-log-blocking
type: note
links: ["[[MOC-debugging]]"]
---

# Gotcha: Docker Proxy Log Stream & Connection Deadlocks

## The Problem
When using `docker-python` behind a TCP proxy like `tecnativa/docker-socket-proxy`, two types of hangs can prevent graceful shutdown:

1.  **Log Streaming**: `follow=True` blocks the thread and doesn't interrupt on SIGTERM.
2.  **Connection Deadlock**: The `docker-python` client keeps a connection pool (Keep-Alive). If the pool isn't closed, HAProxy waits for these connections to finish before it can exit, while the bot waits for HAProxy to respond.

## Symptoms
- Both the bot and the proxy exit with **Code 137** (SIGKILL) after a 10s delay.
- HAProxy logs show: `[WARNING] missing timeouts for backend 'docker-events'`.
- `asyncio.run()` hangs while waiting for executor threads or connection pool cleanup.
- Shutdown logs are completely missing from the console.

## Solution

### 1. The PID 1 Fix (Critical)
In Docker, if a process runs as PID 1, it doesn't receive standard signal handlers. If the bot doesn't "hear" the `SIGTERM`, it will never start its cleanup.
- **Fix**: Add `init: true` to your `docker-compose.yml`. This injects `tini` as PID 1, which correctly forwards signals to Python.

### 2. Implementation Improvements
- **Poll instead of Stream**: Use `logs(tail=100)` in an async loop with `await asyncio.sleep()`.
- **Set Client Timeouts**: Use `docker.from_env(timeout=5)` (set slightly lower than the Docker grace period).
- **Explicit Signal Handlers**: Add `signal.signal(signal.SIGTERM, ...)` in Python to force an immediate cleanup and `sys.exit(0)`.
- **Explicit Cleanup**: Call `docker_client.close()` in a `finally` block and in the bot's `close()` method.
- **Proxy Configuration**: Reduce `TIMEOUT_CLIENT` and `TIMEOUT_SERVER` to `30s` in the proxy template to force-close idle connections during shutdown.
