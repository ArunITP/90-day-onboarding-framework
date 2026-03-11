# Deployment Steps

---

## Deployment History
| Version | Date | Deployed By | Environment | Outcome | Notes |
|---------|------|-------------|-------------|---------|-------|
| — | — | — | — | — | No deployments yet |

---

## Default Rule
Always use **delta deployment** (only changed files). Never run a full deploy unless explicitly requested and confirmed by the user.

---

## Pre-Deployment Checklist
- [ ] All tasks for this release are marked ✅ Done in STATUS.md
- [ ] All test scenarios in TEST_SCENARIOS.md are ✅ Pass (or ⏭ Skip with justification)
- [ ] All Open Points related to this release are resolved
- [ ] Stakeholder sign-off received (Slack/email)
- [ ] Target org authenticated (`sf org list`)
- [ ] [Project-specific step]

---

## Deployment Commands

### Delta deploy — specific changed files (default)
```bash
sf deploy metadata \
  --source-dir force-app/main/default/classes/MyClass.cls \
  --source-dir force-app/main/default/classes/MyClass.cls-meta.xml \
  --wait 10
```

### Manifest-based deploy (controlled scope)
```bash
sfdx force:source:deploy -x manifest/package.xml -w 10 -u YOUR_ORG_ALIAS
```

### Full deploy — use only when explicitly requested and confirmed
```bash
sfdx force:source:deploy -p force-app -w 10 -u YOUR_ORG_ALIAS
```

### Destructive deploy (remove metadata from org)
```bash
sfdx force:source:deploy \
  -x manifest/package-empty.xml \
  --postdestructivechanges manifest/destructiveChanges.xml \
  -w 10 -u YOUR_ORG_ALIAS
```

### Run Apex tests
```bash
sfdx force:apex:test:run -n MyTestClass -r human -w 10 -u YOUR_ORG_ALIAS
```

---

## Production — Sequential Package Order
For complex metadata with dependencies, deploy in this order to avoid failures:

| Step | Contents |
|------|---------|
| 1 | Objects, Custom Fields, Labels, Validation Rules |
| 2 | Layouts, Quick Actions |
| 3 | Apex Classes |
| 4 | Flows (deploy as Draft) |
| 5 | LWC, Aura, FlexiPage |
| 6 | Permission Sets |

---

## Post-Deployment Checklist
- [ ] Smoke test: [specific test to run immediately after deployment]
- [ ] Confirm key flows are active
- [ ] Check debug logs for errors
- [ ] Notify stakeholders
- [ ] Update STATUS.md Change Log

---

## Rollback Plan
**Trigger:** Critical failure in smoke test.
**Steps:**
1. Deactivate any newly activated Flows
2. Redeploy previous version of affected components
3. Notify stakeholders

---

## Notes for CI / Agent Usage
- Always run commands from project root
- Pass `-u YOUR_ORG_ALIAS` to avoid interactive prompts
- Do NOT use `sf project deploy start` — may trigger interactive prompts
- Prefer `sfdx force:source:deploy` for reliability
