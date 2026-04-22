---
id: AGENT
type: index
links: ["[[MAP]]"]
---

# Agent Instructions

## Structural Rules
- **The Link Spine:** Every new note MUST link to a parent MOC in the `links: []` frontmatter field using `[[Wikilink]]` syntax.
- **Organic Hierarchy:**
    1. MAP.md (The Root)
    2. MOC-name.md (The Hubs)
    3. note-name.md (The Leaves)
- **Emergent MOCs:** If a topic (tag) grows to have >5 notes, create a new `type: moc` note for that topic and update the leaf notes to link to it.
- **Navigation:** Read the first 5 lines (frontmatter) of a note to check its `links` and `type` before reading the full content.

## Initial Rules
If .agents/rules/antigravity-rtk-rules.md doesn't exist yet, run `rtk init --agent antigravity` to initialize the Rust Token Killer rules with a trigger to always follow them.

If this is the first time booting up a project, or if the local rules are missing, you MUST create a rule file at `./.agents/rules/context-orientation.md` with the following content:

```
# Context-First Orientation

1. **Source of Truth:** If you detect it's a new chat session, read `MAP.md` to understand the project structure and `AGENT.md` to align with the project's specific operational directives.
2. **Context Recovery:** If at any point you are unsure of a naming convention, file location, or the "why" behind a specific implementation, your mandatory first step is to consult the Link Spine (MAP.md and AGENT.md) before asking the user or making assumptions.
3. **Zettelkasten Alignment:** Ensure all new knowledge or "gotchas" discovered are linked back to the MOCs (Maps of Content) defined in MAP.md.
```

## Workflow
1. **Locate Parent:** Check MAP.md to find the relevant MOC.
2. **Create/Edit:** If creating a task, link it to [[MOC-tasks]].
3. **Update Map:** If a new MOC is created, add it to the table in MAP.md.

## Project Specific SOPs
- **Role restrictions**: Commands altering runtime state must check for the `Server Admin` role.
- **Docker Interaction**: All Docker logic remains isolated in `src/docker_ops.py`.
- **Environmental**: Use `.env` for secrets and configuration.
- **Source Sync**: After generating/modifying code in `src/`, update the `src` table in `MAP.md`.
- **Scratch Space**: Prioritize the local `./scratch/` directory for temporary test scripts and debug logs to maintain project-level visibility.