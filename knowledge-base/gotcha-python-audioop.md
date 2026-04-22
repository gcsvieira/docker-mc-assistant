---
id: gotcha-python-audioop
type: knowledge
tags: ["#python", "#dependencies"]
links: ["[[MOC-debugging]]"]
---

# Gotcha: Python 3.13+ Missing audioop

**Symptom:** `ModuleNotFoundError: No module named 'audioop'` when importing `discord.py`.

**Why:** Python 3.13 removed `audioop` from the standard library.

**Fix:** Install the backport:
```bash
pip install audioop-lts
```
