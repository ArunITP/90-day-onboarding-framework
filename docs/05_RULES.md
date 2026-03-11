# Project Rules
> Paste this into every AI agent session alongside CONTEXT.md.  
> These are non-negotiable standards for this project.

---

## Deployment Rules
- [ ] Always deploy to **sandbox first** — never directly to production
- [ ] Run all test scenarios in TEST_SCENARIOS.md before promoting to production
- [ ] Document pre and post deployment steps in DEPLOYMENT.md before every release
- [ ] Tag every deployment in the Change Log in STATUS.md
- [ ] [Project-specific rule, e.g. "Use Change Sets, not ANT or SFDX for this org"]

---

## Naming Conventions
| Asset Type | Convention | Example |
|-----------|-----------|---------|
| Apex Classes | PascalCase | `SLACalculatorService` |
| Flows | Snake_Case descriptive | `NBS_SLA_Tracker_v1` |
| Custom Fields | Underscore, no spaces | `SLA_Breach_Date__c` |
| LWC Components | camelCase | `slaReportViewer` |
| Files / Docs | kebab-case | `deployment-steps-v2.md` |
| [Add your type] | [Convention] | [Example] |

---

## Coding Standards
- Never hardcode IDs, org URLs, or picklist values — use Custom Metadata or Labels
- Every Apex class must have a corresponding test class with >75% coverage
- All automation must have an active/inactive toggle (Custom Setting or Custom Metadata)
- Comment all non-obvious logic inline: *why*, not *what*
- [Add project-specific standards]

---

## AI Agent Rules
When using Claude, Cursor, or Langdock on this project:
- Always read CONTEXT.md first before writing any code
- Do not suggest changes to 🔒 Locked items in STATUS.md
- If unsure about a requirement, add to OPEN_POINTS.md — do not assume
- Prefer the simplest solution that meets the requirement
- All generated code goes through sandbox testing before being considered complete

---

## Communication Rules
- Stakeholder updates use the template in `_templates/UPDATE_TEMPLATE.md`
- Open Points must be logged before raising them with stakeholders (never ad hoc)
- Test scenarios must be added to TEST_SCENARIOS.md before sharing with testers
