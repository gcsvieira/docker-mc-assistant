---
id: MAP
type: index
updated: 2026-04-21
---

# Map of Content (MAP)

The single source of truth for the project's high-level structure.

## Primary Hubs (MOCs)

| MOC | Description | Last Updated |
| :--- | :--- | :--- |
| [[MOC-tasks]] | Active development and todos | 2026-04-21 |
| [[MOC-discord-bot]] | Core bot logic and architecture | 2026-04-21 |
| [[MOC-debugging]] | Troubleshooting and gotchas | 2026-04-21 |

## Project Index
- [[AGENT]] — Agent instructions and structural rules.
- [[discord_bot]] — Main entry point for bot documentation.

## Code Registry (src)

| src path | Primary MOC | Notes |
| :--- | :--- | :--- |
| src/bot.py | [[MOC-discord-bot]] | Main entry point |
| src/commands/ | [[MOC-discord-bot]] | Slash command definitions |
| src/ops/ | [[MOC-discord-bot]] | Docker, RCON, and background tasks |
| src/ui/ | [[MOC-discord-bot]] | Strings, embeds, views, and logger |
