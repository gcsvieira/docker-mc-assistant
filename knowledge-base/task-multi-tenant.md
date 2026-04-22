---
id: task-multi-tenant
type: task
status: planned
tags: ["#architecture", "#security"]
links: ["[[MOC-tasks]]"]
---

# Task: Multi-Tenant Architecture (PostgreSQL)

## Description
Support multiple servers by mapping different Discord instances to specific container names.

## Planned Details
- **Storage**: Use PostgreSQL to store container mapping slots.
- **Security**: 
    - Restrict `/server container_name` mapping to the Bot Owner.
    - Implement Docker Label checks (e.g., `Assistant.managed=true`) to prevent unauthorized interaction with host containers.
