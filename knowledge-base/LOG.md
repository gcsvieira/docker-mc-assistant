---
id: LOG
type: knowledge
tags: ["#history", "#log"]
links: ["[[MOC-discord-bot]]"]
---

# Implementation Log

Historical record of challenges and solutions during development.

## Setup Sequence (2026-04-21)
1. **File Gen UI Bugs**: Generating files via standard UI diff tools blocked workflow.
    - *What Worked*: Executed `python3 -c "..."` scripts inside `bash` using terminal access to silently lay down python source codes.
2. **Python 3.14 Audioop Error**: `discord.py` relies on `audioop`. Python 3.13+ completely deleted `audioop`.
    - *What Worked*: Successfully pip installed `audioop-lts` to backdoor the missing dependency.
3. **F-String Escapes**: The python payload generation from bash misinterpreted newlines in f-strings.
    - *What Worked*: Stripped multi-line format structures out of f-strings directly inside Python logic.
4. **Environment Perms**: Diagnosed fish-shell VS bash-shell discrepancies.
    - *What Worked*: Stuck rigidly to specific sub-processes or direct python commands.
