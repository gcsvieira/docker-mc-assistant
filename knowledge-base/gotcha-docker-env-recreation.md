---
id: gotcha-docker-env-recreation
type: knowledge
tags: ["#docker", "#troubleshooting"]
links: ["[[MOC-debugging]]"]
---

# Gotcha: Docker Env Var Recreation

**Symptom:** Updating `docker-compose.yml` env vars doesn't reflect after a container restart.

**Why:** Docker bakes env vars into the container at **creation time**. `docker start` re-runs the existing container with its frozen config.

**Fix:** Recreate the container:
```bash
docker compose up --force-recreate -d
```

**Key Insight:** A stopped container retains its old config until explicitly recreated.