# Docker Minecraft Assistant

a discord bot designed to manage dockerized Minecraft servers.

## Project Overview
This tool provides a secure interface for authorized users to manage Minecraft server instances running in Docker. It eliminates the need for direct SSH or shell access for common administrative tasks, providing a structured and audit-friendly management layer via Discord slash commands.

## Key Features
- **Server Lifecycle Management**: Start, stop, and restart containers with safety checks for active players.
- **Dynamic Container Targeting**: Switch between multiple managed containers on the same host using label-based discovery.
- **Whitelist Management**: Direct RCON integration for managing player access.
- **Proactive Notifications**: Automatic alerts for server ready states and autostop triggers.
- **Security First**: Role-based access control (RBAC) and label-based container isolation.

## Dependencies
- **Docker & Docker Compose**: The host must have Docker installed.
- **Minecraft Server Image**: Optimized for the [itzg/minecraft-server](https://github.com/itzg/docker-minecraft-server) image.
   - *Note: If using a different image, ensure the `rcon-cli` utility is available within the container.*

## Quick Start

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gcsvieira/docker-mc-assistant.git
   cd docker-mc-assistant
   ```

2. **Configure Managed Containers**: Add the mandatory management label to your Minecraft server's `docker-compose.yml`:
   ```yaml
   labels:
     - "mc_assistant.managed=true"
   ```

3. **Deploy Managed Container**: Restart your Minecraft container to apply the label:
   ```bash
   docker compose up -d
   ```

4. **Configure Environment**:
   ```bash
   cp .env_example .env
   # Edit .env with your DISCORD_TOKEN, DISCORD_NOTIFY_CHANNEL_ID and DISCORD_ADMIN_ROLE
   ```

5. **Launch the Assistant**:
   ```bash
   docker compose up -d --build
   ```

## Infrastructure Requirements

### 1. Mandatory Docker Label
The assistant only interacts with containers tagged with:
- **Key**: `mc_assistant.managed`
- **Value**: `true`
This ensures strict isolation and prevents unauthorized interaction with other containers on the host.

### 2. Environment Variables
- **`DISCORD_TOKEN`**: Discord bot token from the [Developer Portal](https://discord.com/developers/applications).
- **`DISCORD_ADMIN_ROLE`**: The exact name of the Discord role required for administrative actions (e.g., `Server Admin`).
- **`DISCORD_NOTIFY_CHANNEL_ID`**: ID of the channel for proactive system notifications.
- **`CONTAINER_NAME`**: Default Minecraft container name to target (defaults to `mc_server`).

### 3. Permissions & Security
- Access to the Docker socket is managed via a secure proxy (`tecnativa/docker-socket-proxy`) by default.
- Administrative commands are strictly restricted to users with the configured `DISCORD_ADMIN_ROLE`.

## Command Reference
- `/server start`: Initiates server startup and notifies upon completion.
- `/server stop`: Gracefully shuts down the container after player verification.
- `/server restart`: Restarts the container after player verification.
- `/server status`: Displays a rich status card with uptime and live player counts.
- `/server manage`: Dynamically switches the management target to another labeled container.
- `/server whitelist [add|remove|list]`: Manages the player whitelist via RCON.

## Technical Architecture
The project is built with a three-layer architecture:
1. **Knowledge Base**: Atomic documentation using the Zettelkasten method in `knowledge-base/`.
2. **Orchestration**: AI-ready project structure with `MAP.md` and `AGENT.md`.
3. **Execution**: Python-based logic utilizing the Docker SDK and Discord.py.

---
*Developed for professional server management environments.*
