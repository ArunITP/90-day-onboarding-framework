# Lessons Learned
> Capture lessons as they happen — not just at the end of the project.
> Tag each lesson so it's searchable across projects.
> Be blunt. Future-you will thank present-you.

---

## Tags Reference
`[SF]` Salesforce-specific
`[AI]` AI-assisted development
`[Process]` Project management / workflow
`[Testing]` Test design or execution
`[Stakeholder]` Managing expectations or feedback
`[Deploy]` Deployment-related
`[LWC]` Lightning Web Component specific
`[Apex]` Apex specific

---

## Lessons (carried over from sf-pilot2acm-handover)

| # | Tags | Lesson | Context | Date |
|---|------|--------|---------|------|
| L-001 | `[SF]` `[Deploy]` | Deploy metadata in strict dependency order for production: Objects → Layouts → Apex → Flows → LWC → Permission Sets. A single-package deploy fails when Apex references a field not yet committed. | Learned during pilot project production preparation | Feb 2026 |
| L-002 | `[SF]` `[Deploy]` | Always deploy Flows as **Draft** first. Activating immediately on deploy can fire the flow on unintended records before you've verified behavior in the target org. | Flow was triggering on test records before stakeholder testing was complete | Feb 2026 |
| L-003 | `[Apex]` | Never trust client-supplied record IDs. Resolve target records server-side and cross-validate. A crafted request can otherwise update unrelated records (IDOR). | Security review found that client-passed `accountId` was used without server-side validation in `saveHandoverData` | Feb 2026 |
| L-004 | `[LWC]` | Delta save: track an `_originalData` snapshot on load and only send changed fields to Apex. Objects with heavy automations (e.g. Account) can add 4–7s per save — sending unchanged fields wastes time and governor limits. | Account DML was slow in the handover wizard; delta save eliminated unnecessary calls | Feb 2026 |
| L-005 | `[Apex]` | Never use `Id.startsWith('006')` to check SObject type — use `Id.getSObjectType()`. Prefix-based checks are brittle and unreadable. | Found in 4 places during code review | Feb 2026 |
| L-006 | `[Apex]` | Avoid `Schema.getGlobalDescribe()` — it loads the entire org schema and is a known performance anti-pattern. Use `Schema.describeSObjects(['ObjectApiName'])` instead. | Code review finding | Feb 2026 |
| L-007 | `[SF]` | Task object custom fields often cannot be deployed via metadata API in all org configurations. Document them and create manually in each new org. | Deployment blocker during pilot project | Feb 2026 |
| L-008 | `[Testing]` | Write test data loading instructions at the same time as building the feature — not after. Reconstructing the exact field values, record type IDs, and load order later is time-consuming and error-prone. | Test data for the pilot project had to be reverse-engineered | Feb 2026 |
| L-009 | `[AI]` | Paste CONTEXT.md + RULES.md at the start of every Cursor/Claude session. Without it, the agent makes architecture decisions that contradict project constraints. | Happened during pilot — agent generated code violating established patterns | Feb 2026 |
| L-010 | `[Stakeholder]` | Lock feedback by a hard date and communicate it explicitly. Stakeholders will keep adding minor changes indefinitely without a deadline. | Pilot project experienced scope creep from ongoing minor requests | Feb 2026 |
| L-011 | `[LWC]` | Remove all `console.log` and `console.error` calls before deploying to production. They create noise in debug logs and expose internal data. | Found 8 calls across 3 LWC components during security review | Feb 2026 |
| L-012 | `[Process]` | If a UI field is removed from a form, update the validation logic, the JS handler, and the help text at the same time. Leaving stale validation on a removed field will break form submission silently. | IHC Scheduled field was removed from ACM popup but validation still referenced it — blocked all ACM form completions | Feb 2026 |

---

## Reusable Patterns

### Working Days Calculation (Apex)
**Use when:** Any feature that requires SLA dates excluding weekends (e.g. task due dates).
**Approach:** Create a `BusinessHoursUtility.cls` with an `@InvocableMethod` that takes a start datetime and number of working days, and returns the due datetime. Call from Flow via the invocable — keeps logic in testable Apex rather than hardcoded in Flow XML.

### IDOR-Safe Apex Service Method
**Use when:** Client-side component passes record IDs to an `@AuraEnabled` Apex method.
**Approach:**
```apex
// 1. Resolve the anchor record from a trusted ID (e.g. taskId)
Task t = [SELECT WhatId FROM Task WHERE Id = :taskId];
Id accountId = /* resolve from WhatId */;
// 2. Cross-validate the client-supplied ID resolves to the same account
Customer_360__c c360 = [SELECT Account__c FROM Customer_360__c WHERE Id = :customer360Id];
if (c360.Account__c != accountId) throw new AuraHandledException('Mismatch');
// 3. Only then perform DML
```
