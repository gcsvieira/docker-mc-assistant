import re

# The log line emitted by the AUTO_STOP mechanism when it kills the Java process.
# Expected format: "[2026-04-05T17:33:35+00:00] [Autostop] Stopping Java process"
AUTOSTOP_PATTERN = "[Autostop] Stopping Java process"

def is_autostop_line(line: str) -> bool:
    """Returns True if the given log line is the AUTO_STOP shutdown signal."""
    return AUTOSTOP_PATTERN in line

def parse_player_list(rcon_output: str) -> dict:
    match = re.search(r"There are (?:currently )?(\d+) of a max of (\d+)", rcon_output)
    if not match:
        return {'current': 0, 'max': 20, 'players': []}
    
    current = int(match.group(1))
    max_count = int(match.group(2))
    
    players = []
    if current > 0 and ":" in rcon_output:
        names_str = rcon_output.split(":", 1)[1].strip()
        if names_str:
            players = [p.strip() for p in names_str.split(",") if p.strip()]
            
    return {'current': current, 'max': max_count, 'players': players}

def build_playing_sentence(players: list[str]) -> str:
    count = len(players)
    if count == 0:
        return "but no one is playing right now!"
    elif count == 1:
        return f"{players[0]} is already playing on it!"
    elif count == 2:
        return f"{players[0]} and {players[1]} are playing on it!"
    else:
        last = players[-1]
        rest = ", ".join(players[:-1])
        return f"{rest} and {last} are playing on it!"

def parse_whitelist(rcon_output: str) -> list[str]:
    if "there are no whitelisted players" in rcon_output.lower():
        return []
        
    if ":" in rcon_output:
        names_str = rcon_output.split(":", 1)[1].strip()
        if names_str:
            return [p.strip() for p in names_str.split(",") if p.strip()]
    return []

def build_whitelist_sentence(players: list[str]) -> str:
    count = len(players)
    if count == 0:
        return "No players are currently whitelisted!"
    elif count == 1:
        return f"Only {players[0]} is whitelisted!"
    elif count == 2:
        return f"{players[0]} and {players[1]} are whitelisted!"
    else:
        last = players[-1]
        rest = ", ".join(players[:-1])
        return f"{rest} and {last} are whitelisted!"

def format_whitelist_action(action: str, player: str, rcon_output: str) -> str:
    out_lower = rcon_output.lower()
    if action == 'add':
        if 'already' in out_lower:
            return f"{player} is already on the whitelist!"
        else:
            return f"{player} was added to the whitelist!"
    elif action == 'remove':
        if 'not' in out_lower:
            return f"{player} is not on the whitelist!"
        else:
            return f"{player} was removed from the whitelist!"
    return f"Result: {rcon_output}"

def is_player_joined_line(line: str) -> bool:
    """Returns True if the log line indicates a player successfully logged in or joined."""
    # Matches common patterns like "] <username> joined the game" and "logged in with entity id"
    return " joined the game" in line or "logged in with entity id" in line
