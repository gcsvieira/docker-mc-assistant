---
id: task-whitelist-management
type: task
status: completed
tags: ["#feature", "#rcon"]
links: ["[[MOC-tasks]]"]
---

# Task: Whitelist Management

## Description
Add commands to manage the server's whitelist via Discord.

## Implementation Details
- **Commands**: `/server whitelist add`, `/server whitelist remove`, `/server whitelist list`.
- **Validation**: Check if player exists and if server is running.
- **Fail-safe**: Abort if RCON is unreachable with an appropriate error message.
