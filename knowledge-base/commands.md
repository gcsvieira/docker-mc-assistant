---
id: commands
type: knowledge
tags: ["#discord", "#commands"]
links: ["[[MOC-discord-bot]]"]
---

# Bot Commands Reference

Detailed list of supported slash commands and their behavior.

## Server Management (`/server`)
| Command | Description | Permission |
| :--- | :--- | :--- |
| `/server start` | Starts the MC container. | Everyone |
| `/server stop` | Stops the MC container. | `Server Admin` |
| `/server restart` | Restarts the MC container. | `Server Admin` |

## Whitelist Management (`/server whitelist`)
| Command | Description | Permission |
| :--- | :--- | :--- |
| `/server whitelist add <player>` | Adds a player to the whitelist. | `Server Admin` |
| `/server whitelist remove <player>` | Removes a player from the whitelist. | `Server Admin` |
| `/server whitelist list` | Lists all whitelisted players. | `Server Admin` |

## Edge Cases
- **Already Active**: If `/server start` is run when the server is up, Assistant reports status and online players.
- **RCON Offline**: If the server is running but RCON is unreachable, Assistant reports the connection error.