"""
Documented Learning & Self-Annealing block:
- Replaced fragile subprocess/CLI docker shelling with official docker-python SDK. 
- Communicates seamlessly with host via mounted docker socket.
"""
import os
import logging
import datetime
import docker
from dotenv import set_key

logger = logging.getLogger('mc_assistant.docker')

# Instantiate our client universally (connects automatically via socket)
# We set an explicit timeout to ensure calls don't hang indefinitely through the proxy.
client = docker.from_env(timeout=5)

# Label-based filtering configuration
MANAGED_LABEL_KEY = os.environ.get("MANAGED_LABEL_KEY", "mc_assistant.managed")
MANAGED_LABEL_VALUE = os.environ.get("MANAGED_LABEL_VALUE", "true")
MANAGED_FILTER = f"{MANAGED_LABEL_KEY}={MANAGED_LABEL_VALUE}"

def get_container_name() -> str:
    return os.environ.get("CONTAINER_NAME", "mc_server")

def get_allowed_containers() -> list[str]:
    """
    Returns names of all containers on the host that have the required MANAGED_LABEL.
    This allows for dynamic discovery without maintaining a manual whitelist.
    """
    try:
        # Fetch all containers with the managed label
        managed_containers = client.containers.list(all=True, filters={"label": MANAGED_FILTER})
        # Return sorted list of names for consistent UI
        return sorted([c.name.lstrip("/") for c in managed_containers])
    except Exception as e:
        logger.error(f"Error discovering managed containers by label: {e}")
        # Fallback to current container name if discovery fails
        current = get_container_name()
        return [current] if current else []

def set_container_name(new_name: str) -> tuple[bool, str]:
    """Validates that the target container has the required label before switching."""
    allowed = get_allowed_containers()
    if new_name not in allowed:
        return False, "not_allowed"
        
    from dotenv import find_dotenv
    env_path = find_dotenv()
    try:
        if env_path:
            set_key(env_path, "CONTAINER_NAME", new_name)
        else:
            # Fallback to current directory if not found
            set_key(".env", "CONTAINER_NAME", new_name)
        os.environ["CONTAINER_NAME"] = new_name
        return True, "success"
    except Exception as e:
        logger.error(f"Error setting container name: {e}")
        return False, "error"

def _get_container():
    """
    Fetches the currently targeted container, enforcing the label check.
    Raises docker.errors.NotFound if the container exists but lacks the label.
    """
    container = client.containers.get(get_container_name())
    if container.labels.get(MANAGED_LABEL_KEY) != MANAGED_LABEL_VALUE:
        logger.warning(f"Access denied to container '{container.name}': Missing label {MANAGED_FILTER}")
        raise docker.errors.NotFound(f"Container found but lacks required label {MANAGED_FILTER}")
    return container

def get_container_env_var(key: str, default: str = "") -> str:
    """
    Reads a single environment variable from the MC container's config metadata.
    Works even when the container is stopped (uses inspect data, not exec).
    Returns `default` if the container is not found or the key doesn't exist.
    """
    try:
        container = _get_container()
        env_list = container.attrs.get("Config", {}).get("Env", []) or []
        for entry in env_list:
            if entry.startswith(f"{key}="):
                return entry.split("=", 1)[1]
        return default
    except Exception:
        return default

def is_container_running() -> bool:
    try:
        container = _get_container()
        return container.status.lower() == "running"
    except docker.errors.NotFound:
        return False
    except Exception:
        return False

def start_mc_server() -> tuple[bool, str]:
    try:
        container = _get_container()
        container.start()
        return True, "Server started successfully."
    except Exception as e:
        return False, f"Failed to start server: {str(e)}"

def stop_mc_server() -> tuple[bool, str]:
    try:
        container = _get_container()
        container.stop()
        return True, "Server stopped successfully."
    except Exception as e:
        return False, f"Failed to stop server: {str(e)}"

def restart_mc_server() -> tuple[bool, str]:
    try:
        container = _get_container()
        container.restart()
        return True, "Server restarted successfully."
    except Exception as e:
        return False, f"Failed to restart server: {str(e)}"

def wait_for_server_ready(timeout: int = 300, since: datetime.datetime = None) -> bool:
    """
    Polls the container logs and waits for the 'Done' message.
    Returns True if found, False if timeout or error.
    - since: Only check logs after this timestamp.
    """
    try:
        container = _get_container()
        start_time = datetime.datetime.now()
        
        # If since is not provided, we only check logs from 'now'
        if since is None:
            since = datetime.datetime.now(datetime.timezone.utc)
            
        while (datetime.datetime.now() - start_time).total_seconds() < timeout:
            if not is_container_running():
                return False
                
            # Get the last few lines since our marker
            logs = container.logs(since=since, tail=100).decode("utf-8", errors="replace")
            
            # Minecraft "Ready" pattern: [Server thread/INFO]: Done (2.5s)! For help, type "help"
            if "Done (" in logs and "!" in logs:
                return True
            
            import time
            time.sleep(2)
                
        return False
    except Exception as e:
        logger.error(f"Error waiting for server ready: {e}")
        return False

def check_for_autostop(since: datetime.datetime = None) -> tuple[bool, bool]:
    """
    Checks recent logs for the AUTO_STOP shutdown line.
    Returns (triggered, has_players_joined).
    - since: Only check logs after this timestamp.
    """
    from .rcon import is_autostop_line, is_player_joined_line, parse_player_list
    
    try:
        container = _get_container()
        # We check both running and exited because autostop might have already killed the process
        if container.status.lower() not in ["running", "exited"]:
            return False, False

        # Use since if provided to avoid catching old triggers
        logs_raw = container.logs(since=since, tail=100).decode("utf-8", errors="replace")
        lines = logs_raw.splitlines()
        
        triggered = any(is_autostop_line(line) for line in lines)
        has_players = any(is_player_joined_line(line) for line in lines)
        
        # If not in logs, check current status if running
        if not has_players and is_container_running():
            success, output = run_mc_command("list")
            if success:
                parsed = parse_player_list(output)
                if parsed.get('current', 0) > 0:
                    has_players = True

        return triggered, has_players
    except Exception as e:
        logger.error(f"[Autostop] Error checking for autostop: {e}")
        return False, False

def watch_for_autostop(on_autostop) -> None:
    """
    DEPRECATED: Use check_for_autostop() in an async loop instead.
    Tails the MC container logs indefinitely, waiting for the AUTO_STOP shutdown line.
    """
    triggered, has_players = check_for_autostop()
    if triggered:
        on_autostop(has_players)

def run_mc_command(command: str) -> tuple[bool, str]:
    try:
        container = _get_container()
        # Execute natively in container through sdk
        exit_code, output = container.exec_run(["rcon-cli"] + command.split())
        output_str = output.decode("utf-8", errors="replace").strip() if output else ""
        return exit_code == 0, output_str
    except Exception as e:
        return False, f"Failed to execute command: {str(e)}"

def get_server_status_info() -> dict:
    try:
        container = _get_container()
        container.reload() # Refresh states
        
        state = container.attrs.get("State", {})
        status_str = state.get("Status", "unknown")
        status = "ACTIVE" if status_str.lower() == "running" else "STOPPED"

        uptime_str = "0min"
        if status == "ACTIVE":
            started_at_str = state.get("StartedAt")
            if started_at_str:
                try:
                    time_str = started_at_str[:19] + "+00:00"
                    started_at = datetime.datetime.fromisoformat(time_str)
                    now = datetime.datetime.now(datetime.timezone.utc)
                    diff = now - started_at

                    hours, remainder = divmod(diff.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)

                    parts = []
                    if diff.days > 0:
                        parts.append(f"{diff.days}d")
                    if hours > 0:
                        parts.append(f"{hours}h")
                    parts.append(f"{minutes}min")
                    uptime_str = "".join(parts) if parts else "0min"
                except Exception:
                    uptime_str = "Unknown"
                    
        return {"status": status, "uptime": uptime_str}
    except docker.errors.NotFound:
        return {"status": "UNKNOWN", "uptime": "0min"}
    except Exception:
        return {"status": "UNKNOWN", "uptime": "0min"}