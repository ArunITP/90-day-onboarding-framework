# Project Context
> Paste this file first into any new AI agent session (Claude, Cursor, Langdock) to establish shared understanding.

---

## Project Overview
**Project Name:** 90 Day Onboarding Framework
**One-line Goal:** [What does success look like when this is done?]
**Start Date:** 2026-03-03
**Target Completion:** [YYYY-MM-DD]
**Current Phase:** Discovery / Requirements

---

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Platform | Salesforce |
| Database | SF Objects |
| Deployment | SFDX CLI — Sandbox → Production |
| AI Tools Used | Claude, Cursor |

---

## Key People
| Name | Role | Involvement |
|------|------|-------------|
| Arun Kumar | Developer / Owner | Builds, deploys, maintains |
| [Stakeholder] | [Role] | Testing, approvals |

---

## Environments
| Alias | Purpose |
|-------|---------|
| 90day-sandbox | Development & testing (see [SANDBOX_AUTH.md](SANDBOX_AUTH.md)) |
| Production | Go-live target |

---

## What Problem Are We Solving?
[2–3 sentences. What was broken or missing before this project?]

---

## What Is In Scope
- [Specific deliverable 1]
- [Specific deliverable 2]

## What Is Out of Scope
- [Explicitly excluded item 1]

---

## Predecessor Project Reference
The **sf-pilot2acm-handover** project (Pilot-to-ACM Handover Wizard) was completed in Feb 2026 in the same Salesforce org. It introduced `Customer_360__c`, SLA task automation, and related LWC components. This project does not extend the wizard but may reference its data model or org configuration. See `data/` folder for test data inherited from that project.

---

## AI Agent Instructions
When working on this project:
- Always refer to `05_RULES.md` for coding and deployment standards
- Always check `07_OPEN_POINTS.md` before making assumptions
- Update `06_STATUS.md` at the end of each session
- Do not change anything marked 🔒 Locked in STATUS.md
- Default to **delta deployment** — never full deploy unless explicitly confirmed
