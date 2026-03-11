# Pre-Project Intake
> Complete this BEFORE starting any technical implementation.  
> This document feeds directly into CONTEXT.md, ARCHITECTURE.md, RULES.md, and TEST_SCENARIOS.md.  
> Estimated time to complete: 30–60 minutes. It will save you 5–10x that during implementation.

---

## Section 1: The Problem
*The most important section. Be specific. Vague problems create vague solutions.*

**1.1 What is the core problem or opportunity?**  
[e.g. Sales reps cannot see their SLA performance in real time — they find out they've breached a target only after the fact, which causes escalations.]

**1.2 Who has this problem, and how often?**  
[e.g. 40 sales reps, daily. 3 team managers, weekly during reviews.]

**1.3 What does the current workaround look like?**  
[e.g. Managers pull a manual report from SF every Monday, paste it into Excel, and send it out. Takes ~2 hours per manager.]

**1.4 What does success look like? How will you know this project worked?**  
[e.g. Reps can see their own SLA status without asking anyone. Managers spend <15 minutes on weekly reporting. Zero SLA breach surprises.]

---

## Section 2: Scope

**2.1 What is explicitly IN scope?**  
- [Item 1]
- [Item 2]

**2.2 What is explicitly OUT of scope?**  
*(Document this carefully — this is what prevents scope creep)*  
- [Item 1]
- [Item 2]

**2.3 Are there any phases planned?**  
- Phase 1 (this project): [...]
- Phase 2 (future): [...]

---

## Section 3: People & Roles

**3.1 Who are the stakeholders?**
| Name | Role | Responsibilities in This Project | Availability for Testing |
|------|------|----------------------------------|--------------------------|
| [Name] | [Role] | [e.g. Approves requirements, tests UAT] | [e.g. 2–3 hrs/week] |

**3.2 Who is the decision-maker when there's disagreement?**  
[Name and title]

**3.3 Who needs to be informed (not involved) about progress?**  
[Name, how often, preferred format]

---

## Section 4: Technical Constraints
*Answer even if approximate. "Unknown" is a valid answer — but flag it.*

**4.1 What platform(s) must be used?**  
[e.g. Salesforce, must stay within SF ecosystem — no external hosting]

**4.2 What existing systems must this integrate with?**  
| System | What data flows | Direction | Known constraints |
|--------|----------------|-----------|-------------------|
| [e.g. ERP] | [Order data] | [Into SF] | [API rate limit: 1000 calls/day] |

**4.3 What are the access / permission constraints?**  
[e.g. Dev access to sandbox only — all production changes go through change manager. No direct DB access.]

**4.4 Are there security or data privacy requirements?**  
[e.g. No PII outside SF. GDPR applies — no storing EU customer data in external tools.]

**4.5 What browsers / devices must this work on?**  
[e.g. Chrome and Edge on Windows. Not Safari. Not mobile.]

**4.6 Are there performance requirements?**  
[e.g. Report must load in under 5 seconds. Must support 200 concurrent users.]

---

## Section 5: Requirements

**5.1 Functional Requirements** *(what the system must do)*
| # | Requirement | Priority | Source |
|---|-------------|----------|--------|
| FR-001 | [e.g. User can filter SLA report by date range] | 🔴 Must Have | Sebastian |
| FR-002 | [e.g. System sends email alert when SLA breached] | 🟡 Should Have | Arun |
| FR-003 | [e.g. Export report to Excel] | 🟢 Nice to Have | Diana |

**Priority:** 🔴 Must Have | 🟡 Should Have | 🟢 Nice to Have

**5.2 Non-Functional Requirements** *(how the system must behave)*
| # | Requirement | Priority |
|---|-------------|----------|
| NFR-001 | [e.g. Report must load in <5 seconds] | 🔴 Must Have |
| NFR-002 | [e.g. Admin can toggle automation off without a deployment] | 🟡 Should Have |

**5.3 Are there any existing designs, mockups, or examples to follow?**  
[Yes / No. If yes, describe or attach.]

---

## Section 6: Testing & Acceptance

**6.1 Who will test this?**  
[Names and availability]

**6.2 What does "ready to test" look like?**  
[e.g. Deployed to sandbox, all Must Have requirements implemented, test scenarios document shared]

**6.3 What does "accepted / done" look like?**  
[e.g. All test scenarios passed, signed off by Sebastian and Diana in writing]

**6.4 How long is the testing window?**  
[e.g. 5 business days for UAT]

**6.5 Seed test scenarios** *(draft these now — you'll refine them in TEST_SCENARIOS.md)*
| Scenario | Who Tests It |
|----------|-------------|
| [e.g. Run NBS report for last 30 days — confirm correct data] | Sebastian |
| [e.g. Trigger SLA breach — confirm email alert fires] | Diana |

---

## Section 7: Timeline & Milestones

**7.1 Is there a hard deadline? Why?**  
[e.g. Yes — must be in production before Q2 kickoff on April 1]

**7.2 Draft milestone plan:**
| Milestone | Target Date | Dependencies |
|-----------|-------------|-------------|
| Requirements signed off | [date] | Stakeholder availability |
| Dev complete (sandbox) | [date] | |
| UAT begins | [date] | Test scenarios ready |
| Feedback locked | [date] | |
| Production deployment | [date] | Change manager approval |
| Handover / knowledge transfer | [date] | |

---

## Section 8: Open Questions Before Starting
*List anything you're unsure about. These become your first OPEN_POINTS.*

| # | Question | Who Can Answer | Urgency |
|---|----------|---------------|---------|
| 1 | [e.g. Is there an existing SLA definition document?] | Sebastian | 🔴 High |
| 2 | [e.g. Will testers have sandbox access set up before UAT?] | Diana | 🟡 Medium |

---

## Section 9: Definition of Done
*Write this now. Revisit at the end. Did you actually achieve it?*

This project is complete when:
- [ ] All 🔴 Must Have requirements are implemented and tested
- [ ] All test scenarios are marked ✅ Pass (or ⏭ Skip with stakeholder approval)
- [ ] Production deployment completed and smoke tested
- [ ] Stakeholders have confirmed acceptance in writing
- [ ] Knowledge transfer / documentation handed to [person/team]
- [ ] LESSONS.md updated with at least 3 lessons from this project

---

*Completed by: [Name] | Date: [YYYY-MM-DD]*
