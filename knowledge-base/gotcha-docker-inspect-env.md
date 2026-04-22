---
id: gotcha-docker-inspect-env
type: knowledge
tags: ["#docker", "#python"]
links: ["[[MOC-debugging]]"]
---

# Gotcha: Docker Inspect Static State

**Symptom:** `get_container_env_var` doesn't show live environment updates.

**Why:** It reads from `container.attrs["Config"]["Env"]`, which is static metadata from creation time, not the live process environment.

**Implementation Note:** `itzg/minecraft-server` uses **seconds** for `AUTOSTOP_TIMEOUT_EST`. The bot uses integer floor division (`// 60`) for display.
