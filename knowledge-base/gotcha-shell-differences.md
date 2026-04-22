---
id: gotcha-shell-differences
type: knowledge
tags: ["#environment", "#shell"]
links: ["[[MOC-debugging]]"]
---

# Gotcha: Fish vs Bash Subprocesses

**Symptom:** Subprocess commands fail or behave inconsistently between shells.

**Why:** Fish is not POSIX-compliant; common Bash idioms may break.

**Fix:** Use explicit `python3 -c "..."` or direct Python invocations to ensure consistency across different host shells.
