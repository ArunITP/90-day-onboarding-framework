# Test Scenarios
> Structured for direct export to Google Sheets.
> Each row = one test scenario. Keep steps numbered within a single cell using line breaks when exporting.

---

## Export Instructions
To export to Google Sheets:
1. Ask Claude: *"Export TEST_SCENARIOS.md to a CSV file ready for Google Sheets"*
2. Import the CSV into Google Sheets (File → Import)
3. Share with testers — they fill in Status, Actual Result, and Notes columns

---

## Scenarios

| ID | Area / Module | Scenario Title | Preconditions | Steps | Expected Result | Actual Result | Status | Tester | Notes |
|----|--------------|----------------|--------------|-------|-----------------|---------------|--------|--------|-------|
| TS-001 | [Area] | [Title] | [Preconditions] | 1. Step one 2. Step two | [Expected] | | ⬜ Not Tested | | |

**Status Values:** ⬜ Not Tested | 🔄 In Progress | ✅ Pass | ❌ Fail | ⏭ Skip

---

## Summary
| Total | Not Tested | In Progress | Pass | Fail | Skip |
|-------|-----------|-------------|------|------|------|
| 0 | 0 | 0 | 0 | 0 | 0 |

*Update this summary manually or ask Claude to recalculate from the table above.*

---

## Reference: Predecessor Project Test Scenarios
The `sf-pilot2acm-handover` project has **56 documented E2E test scenarios** (covering Flow triggers, wizard steps, delta save, permissions, edge cases, and security). These are available in:
- `data/1_PROJECT_REFERENCE.md` — full scenario list with expected results
- `data/TEST_SCENARIOS.csv` — spreadsheet-ready format

These may be useful as a reference when designing test scenarios for this project, particularly if the org configuration or objects overlap.
