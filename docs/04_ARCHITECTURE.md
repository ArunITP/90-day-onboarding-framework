# Architecture & Technical Decisions
> Document decisions AND the reasoning behind them. This is what saves you when returning to a project or handing it off.

---

## System Overview
[Brief description of how the system fits together once requirements are defined]

```
[Data Source] → [Processing Layer] → [Output / UI]
```

---

## Key Architectural Decisions

| # | Decision | Reason | Alternatives Considered | Date |
|---|----------|--------|------------------------|------|
| AD-001 | [Decision] | [Reason] | [Alternatives] | [Date] |

---

## Constraints
- **Platform:** Salesforce — no external hosting
- **Deployment:** Delta deploy by default; full deploy only on explicit confirmation
- **Access:** Sandbox for all development — no direct production changes

---

## Data Model
| Object | Purpose | Key Fields | Relationships |
|--------|---------|-----------|---------------|
| [Object] | [Purpose] | [Fields] | [Relations] |

---

## Known Technical Debt
| Item | Impact | Plan to Address |
|------|--------|----------------|
| [Item] | [Impact] | [Plan] |

---

## Best Practices & Patterns (from predecessor project)

### LWC Performance — Delta Save
Only send changed fields to the server. Track an `_originalData` snapshot on load; diff against current values before calling Apex. This avoids unnecessary DML on objects with heavy triggers (e.g. Account can take 4–7s per save).

```js
// Pattern: build a map of only changed fields before calling Apex
const changes = {};
for (const [key, value] of Object.entries(currentData)) {
    if (value !== this._originalData[key]) changes[key] = value;
}
if (Object.keys(changes).length === 0) { /* skip DML */ return; }
```

### LWC Performance — Avoid Redundant Wire Calls
Use `@wire` for initial data load only. For user-triggered refreshes (e.g. contact lookup refresh), call an `@AuraEnabled` method directly rather than invalidating the wire cache, which can cause multiple re-renders.

### Apex — IDOR Protection
Never trust a client-supplied record ID as the authority for which record to update. Always resolve the target account/record from a server-side anchor (e.g. resolve `accountId` from `taskId` via Apex query), then cross-validate any additional IDs the client sends match the same anchor. Mismatches should throw `AuraHandledException` and rollback all DML via savepoint.

### Apex — Working Days Calculation
Use a reusable `BusinessHoursUtility.cls` that calculates business minutes between two datetimes (09:00–18:00 Mon–Fri). Avoid hardcoding weekday logic in Flow XML — call via `@InvocableMethod` so the calculation is testable and reusable.

### Deployment — Sequential Packages for Production
For complex metadata with interdependencies (Apex references fields, Flows reference Apex), deploy in strict order:
1. Objects & Fields & Labels
2. Layouts & Quick Actions
3. Apex Classes
4. Flows (deploy as Draft first)
5. Lightning UI (LWC, Aura, FlexiPage)
6. Permission Sets

### Apex — Avoid `Schema.getGlobalDescribe()`
Use `Schema.describeSObjects(['ObjectApiName'])` instead. `getGlobalDescribe()` is a known performance anti-pattern that loads the full org schema.

### Apex — ID Prefix Comparison
Never use `Id.startsWith('006')` to determine SObject type. Use `Id.getSObjectType()` — it is more readable and not brittle against org-specific prefixes.
