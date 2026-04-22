---
id: MOC-debugging
type: moc
links: ["[[MAP]]", "[[MOC-discord-bot]]"]
---

# MOC Debugging Gotchas

A centralized hub for non-obvious bugs, environment quirks, and troubleshooting lessons.

| Gotcha | Category | Description |
| :--- | :--- | :--- |
| [[gotcha-docker-env-recreation]] | Docker | Env vars require recreation, not just restart |
| [[gotcha-python-fstrings]] | Python | f-string vs plain string behavior |
| [[gotcha-docker-inspect-env]] | Docker | Static vs live environment state |
| [[gotcha-python-audioop]] | Python | Missing audioop in Python 3.13+ |
| [[gotcha-shell-differences]] | Environment | Fish vs Bash subprocess behavior |
| [[gotcha-docker-proxy-log-blocking]] | Docker | Infinite log streams block graceful shutdown behind proxies |
| [[gotcha-dotenv-path-discovery]] | Docker | Flattened Docker paths break .env discovery |
