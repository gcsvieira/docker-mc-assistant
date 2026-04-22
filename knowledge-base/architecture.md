---
id: architecture
type: knowledge
tags: ["#conceptual", "#structure"]
links: ["[[MOC-discord-bot]]"]
---

## 3-Layer Principle
Historically, the project uses a 3-layer architecture to separate concerns.
1. **Directive (What to do)**: SOPs in Markdown.
2. **Orchestration (Decision making)**: The AI Agent.
3. **Execution (Doing the work)**: Deterministic Python scripts in `src/`.

## Core Guidelines
- **Role restrictions**: Commands that alter server runtime state (e.g., `/server stop` and `/server restart`) MUST check if the executing user possesses the `Server Admin` role.
- **Role Verification**: Members are fetched from `discord.Member` properties. Logic: `any(role.name == "Server Admin" for role in interaction.user.roles)`.
- **Docker Interaction**: All Docker logic remains isolated in `src/docker_ops.py` to ensure it remains deterministic.
- **Environmental**: The bot derives the bot token and specific docker `CONTAINER_NAME` off the `.env` configuration file, avoiding hardcoded values.

## Why this works
Pushing complexity into deterministic code (`src/`) allows the orchestration layer to focus on high-level decision making, reducing compounding errors.