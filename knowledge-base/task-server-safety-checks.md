---
id: task-server-safety-checks
type: task
status: completed
tags: ["#security", "#feature"]
links: ["[[MOC-tasks]]"]
---

# Task: /server stop and /server restart Safety Checks

## Description
Implement safety checks for destructive server commands based on player count.

## Implementation Details
- **Logic**: Check player count via RCON. If > 0, refuse to stop/restart unless overridden.
- **Response**: "There are still player(s) on the server! Are you trying to be mean??"
- **Admin Override**: Users with `Server Admin` role get an override option with buttons ("Do it", "Nevermind").
- **Security**: Added fail-safe to abort if RCON is unreachable.
- **Performance**: Added cooldowns to prevent Docker daemon spam.
