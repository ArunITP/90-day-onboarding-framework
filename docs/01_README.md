# Project Brain — Template Pack
*A structured system for AI-assisted project development*

---

## How to Start a New Project

1. **Copy this entire folder** into your new project root
2. **Complete `_templates/PRE_PROJECT_INTAKE.md`** — do this BEFORE writing any code
3. **Fill in `_project/CONTEXT.md`** from your intake answers
4. **Set up `_project/STATUS.md`** with your initial task list
5. **Populate `_project/RULES.md`** with project-specific conventions
6. **Start building** — paste CONTEXT.md + RULES.md at the top of every AI agent session

---

## File Reference

```
_project/
  CONTEXT.md          ← Paste into every AI session first. Project overview + people + stack.
  STATUS.md           ← Daily driver. Task tracker, milestones, risks.
  OPEN_POINTS.md      ← Stakeholder-blocking questions. Review before every meeting.
  TEST_SCENARIOS.md   ← Exportable to Google Sheets for stakeholder testing.
  ARCHITECTURE.md     ← Technical decisions + constraints + data model.
  RULES.md            ← Paste into every AI session. Non-negotiable standards.
  DEPLOYMENT.md       ← Pre/post deploy checklists + history.
  LESSONS.md          ← Tagged lessons. Repurpose across projects.
  UPDATES/
    YYYY-MM-DD.md     ← One file per stakeholder update (drafted by Claude).

_templates/
  PRE_PROJECT_INTAKE.md   ← Complete before implementation starts.
  UPDATE_TEMPLATE.md      ← Used to draft stakeholder Slack/email updates.
```

---

## Daily Workflow

**Start of session:**
1. Open STATUS.md → pick your task
2. Paste CONTEXT.md + RULES.md into your AI agent

**End of session:**
1. Update STATUS.md (mark tasks done, update notes)
2. Log any new open points in OPEN_POINTS.md
3. Log any lessons in LESSONS.md

**Before a stakeholder update:**
1. Ask Claude: *"Draft a stakeholder update using STATUS.md, OPEN_POINTS.md, and UPDATE_TEMPLATE.md"*
2. Review, adjust, send

**Before deployment:**
1. Complete DEPLOYMENT.md pre-checklist
2. Update after deployment with outcome + Change Log entry

---

## Exporting Test Scenarios to Google Sheets
Ask Claude: *"Convert TEST_SCENARIOS.md into a CSV I can import to Google Sheets"*

---

## Cross-Project Reuse
- Copy `LESSONS.md` snippets tagged `[Reusable]` into new projects
- Copy relevant `RULES.md` sections as your baseline for the next project
- `ARCHITECTURE.md` patterns can be referenced when making decisions in similar projects
