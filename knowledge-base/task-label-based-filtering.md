---
id: task-label-based-filtering
type: task
status: completed
tags: ["#security", "#infrastructure"]
links: ["[[MOC-tasks]]"]
---

# Task: Label-Based Container Filtering

## Description
Improve security and organization by restricting the bot's visibility to only containers tagged with a specific Docker label (e.g., `bot.Assistant.managed=true`).

## Problem
Currently, the bot relies on a name-based whitelist (`ALLOWED_CONTAINERS`). While secure, it's manually intensive and can lead to errors if multiple containers share similar names or if the bot is accidentally pointed to a non-Minecraft container on the host.

## Proposed Solution
Implement mandatory label filtering in the Docker SDK calls.
- **Label**: `bot.Assistant.managed=true`
- **Mechanism**: Use the `filters={"label": "bot.Assistant.managed=true"}` parameter in all container retrieval logic.

## Execution Plan

### Phase 1: Configuration
- [x] Add `MANAGED_LABEL=bot.Assistant.managed` to `.env_example`.
- [x] Define the label value (default `true`) in configuration.

### Phase 2: Implementation (`src/docker_ops.py`)
- [x] Update `get_allowed_containers` to potentially incorporate label-based discovery.
- [x] Update `_get_container()` and listing logic to strictly filter by the managed label.
- [x] Ensure that even if a container name is in the whitelist, it is REJECTED if it lacks the required label.

### Phase 3: Validation
- [x] Label the `enan-mc` container with the managed label.
- [x] Create a "rogue" container with a name in the whitelist but *without* the label.
- [x] Verify the bot can see the first but is completely blind to the second.
