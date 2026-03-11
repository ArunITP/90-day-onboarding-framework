# Pilot-to-ACM Handover - Project Reference

This document consolidates test scenarios, test data loading instructions, and deployment history into a single reference.

**Table of Contents:**
- [Part 1: E2E Test Scenarios](#part-1-e2e-test-scenarios)
- [Part 2: Test Data Loading Instructions](#part-2-test-data-loading-instructions)
- [Part 3: Deployment History](#part-3-deployment-history)

---

# Part 1: E2E Test Scenarios

## Testing Instructions

### How to Use This Document
1. **Before Testing:** Set up test data as described in "Test Data Setup" section
2. **During Testing:** Execute each scenario, record observed results
3. **After Testing:** Mark pass/fail, document any follow-up items
4. **Test Records:** Link to actual Salesforce records used for traceability

### Column Definitions
| Column | Description |
|--------|-------------|
| **Stage** | Unique identifier for the test case |
| **Trigger** | What initiates the scenario |
| **Scenario** | Detailed step-by-step test conditions |
| **Expected Result** | Precise expected outcomes - verify each item |
| **Observed Result** | Actual outcome (if matches expected, write "As expected") |
| **Test Records** | Salesforce record links used for this test |
| **Test Passed?** | ✅ YES / ❌ NO / ⏸️ BLOCKED |
| **Follow-Up** | Issues, notes, adjustments needed |

---

## Test Data Setup

### Required Test Records

Create the following records before testing:

| Record Type | Name | Key Fields |
|-------------|------|------------|
| Account | "Handover Test Account" | Service_Country__c = 'DE', NumberOfEmployees = 150, plOpenJobs__c = '20-49', OwnerId = ACM User, GTM_Motion_Account__c populated |
| Contact | "Strategic Test Contact" | FirstName = 'Strategic', LastName = 'Contact', Email, Phone, Title = 'CEO' |
| Contact | "Operational Test Contact" | FirstName = 'Operational', LastName = 'Contact', Email, Phone, Title = 'Manager' |
| Account | "Parent Test Account" | Service_Country__c = 'DE' |
| Opportunity | "Test Opportunity" | AccountId = Handover Test Account, Stage = 'Prospecting' (for closing later), Record Type = 'Sales' or 'Sales Transactional', not_a_new_customer__c = false, Owner.GTM_Motion_User__c = 'Subscription New Business' |

### User Setup
- **AE User:** Opportunity Owner with `Handover_Wizard_Access` permission set, GTM_Motion_User__c = 'Subscription New Business'
- **ACM User:** Account Owner with `Handover_Wizard_Access` permission set

---

## Test Scenarios

### Category: Flow Trigger - SLA 1 (Contract Received)

#### FLOW-1: Contract Received - Basic Flow Trigger

| Field | Value |
|-------|-------|
| **Stage** | FLOW-1 |
| **Trigger** | Opportunity Stage = "Contract Received" |
| **Scenario** | Update Opportunity Stage to "Contract received"<br>• Pilot_Opportunity__c formula = true<br>• Opportunity Owner.GTM_Motion_User__c = 'Subscription New Business'<br>• Stage changed FROM any other stage TO 'Contract received' |
| **Expected Result** | **Customer_360__c record created:**<br>• Account__c = Opportunity.AccountId<br>• Type__c = 'Pilot Handover'<br>• Documentation_Status__c = 'Not Started'<br><br>**AE Task created:**<br>• Subject from $Label.Handover_AE_Task_Subject<br>• WhatId = Linked via ON_Opportunity__c or Opportunity.Id<br>• Linked_Opportunity__c = Opportunity reference<br>• Related_Account__c = Account.Id<br>• OwnerId = Opportunity.OwnerId<br>• ActivityDate = Today + 1 working day (excludes weekends)<br>• Priority = 'High'<br>• Status = 'Open' |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | SLA 1: 1 working day for AE. Filter uses Pilot_Opportunity__c formula + GTM Motion |

---

#### FLOW-2: Contract Received on Friday (Working Days)

| Field | Value |
|-------|-------|
| **Stage** | FLOW-2 |
| **Trigger** | Opportunity Stage = "Contract Received" (Friday) |
| **Scenario** | Update Opportunity Stage to "Contract Received" on a Friday<br>• Verify AE Task due date uses working days |
| **Expected Result** | • AE Task ActivityDate = Monday (1 working day, skips weekend)<br>• Working days calculation excludes Saturday/Sunday |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | AE Task now uses working days (not calendar days) |

---

#### FLOW-3: Contract Received with Existing C360

| Field | Value |
|-------|-------|
| **Stage** | FLOW-3 |
| **Trigger** | Opportunity Stage = "Contract Received" (Existing C360) |
| **Scenario** | Update Opportunity Stage to "Contract received"<br>• Account already has Customer_360__c record with Status = 'In Progress'<br>• Pilot_Opportunity__c = true |
| **Expected Result** | • NEW Customer_360__c record IS created (Flow has no duplicate check)<br>• AE Task created<br>• NOTE: Duplicate C360 records may exist - wizard handles by finding latest non-completed record |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Flow creates new C360 each trigger - wizard finds correct record via query |

---

### Category: Flow Trigger - SLA 2 (Closed Won)

#### FLOW-4: Closed Won - ACM Task Creation

| Field | Value |
|-------|-------|
| **Stage** | FLOW-4 |
| **Trigger** | Opportunity Stage = "Closed Won" |
| **Scenario** | Update Opportunity Stage to "Closed Won"<br>• Pilot_Opportunity__c formula = true<br>• Opportunity Owner.GTM_Motion_User__c = 'Subscription New Business'<br>• Stage changed FROM any other stage TO 'Closed Won' |
| **Expected Result** | **ACM Task created:**<br>• Subject from $Label.Handover_ACM_Task_Subject ('Internal Handover Call planen')<br>• OwnerId = Account.OwnerId (ACM)<br>• WhatId = Opportunity.Id<br>• Related_Account__c = Account.Id<br>• ActivityDate = Today + 3 working days<br>• Priority = 'High'<br>• Status = 'Open'<br><br>• NO new Customer_360__c created by Closed Won path |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | SLA 2: 3 working days for ACM. Task links to Opportunity not Account |

---

#### FLOW-5: Closed Won on Friday (Working Days)

| Field | Value |
|-------|-------|
| **Stage** | FLOW-5 |
| **Trigger** | Opportunity Stage = "Closed Won" (Friday) |
| **Scenario** | Update Opportunity Stage to "Closed Won" on a Friday<br>• Verify ACM Task due date uses working days |
| **Expected Result** | • ACM Task ActivityDate = Wednesday (3 working days: Mon, Tue, Wed)<br>• Working days calculation excludes Saturday/Sunday |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Verify weekend exclusion in due date |

---

#### FLOW-6: Closed Won without Prior Contract Received

| Field | Value |
|-------|-------|
| **Stage** | FLOW-6 |
| **Trigger** | Opportunity Stage = "Closed Won" (No C360 exists) |
| **Scenario** | Update Opportunity directly to "Closed Won" (edge case)<br>• Account does NOT have existing Customer_360__c record |
| **Expected Result** | • Flow should handle gracefully<br>• Either: Create C360 + both tasks, OR log warning and skip ACM task<br>• Document actual behavior |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Edge case - document expected behavior |

---

#### FLOW-7: Account Management Opportunity (Negative Test)

| Field | Value |
|-------|-------|
| **Stage** | FLOW-7 |
| **Trigger** | Non-Pilot Opportunity (Negative Test) |
| **Scenario** | Test Flow filter exclusions:<br>• Option A: Opportunity Owner.GTM_Motion_User__c != 'Subscription New Business'<br>• Option B: Pilot_Opportunity__c formula = false (wrong record type or not_a_new_customer__c = true)<br>• Move such Opp to Contract Received or Closed Won |
| **Expected Result** | • NO Customer_360__c record created<br>• NO AE Task created<br>• NO ACM Task created<br>• Flow entry conditions not met |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Negative test - verify filter on GTM_Motion_User__c and Pilot_Opportunity__c formula |

---

### Category: Wizard Launch

#### WIZ-1: First Time Launch

| Field | Value |
|-------|-------|
| **Stage** | WIZ-1 |
| **Trigger** | Click "Prepare Handover" button |
| **Scenario** | Click "Prepare Handover" Quick Action on AE Task<br>• Task Status = 'Open'<br>• Customer_360__c Status = 'Not Started' |
| **Expected Result** | • New browser tab opens with Handover Wizard<br>• Original Task record page modal closes automatically<br>• Wizard loads at Step 1 (Pre-check)<br>• Customer_360__c Status updated to 'In Progress'<br>• Timestamp_Step_PreCheck_Started__c populated |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### WIZ-2: Resume from Notes Section

| Field | Value |
|-------|-------|
| **Stage** | WIZ-2 |
| **Trigger** | Click "Prepare Handover" (Resume) |
| **Scenario** | Click "Prepare Handover" on Task<br>• Customer_360__c Status = 'In Progress'<br>• Current_Wizard_Step__c = 'Notes'<br>• Customer_Goals__c has saved data |
| **Expected Result** | • Wizard opens at Step 2 (Notes)<br>• Previously saved Notes data displayed<br>• Pre-check data preserved<br>• No timestamp fields overwritten |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Resume capability test |

---

#### WIZ-3: Launch on Completed Task

| Field | Value |
|-------|-------|
| **Stage** | WIZ-3 |
| **Trigger** | Click "Prepare Handover" (Completed) |
| **Scenario** | Click "Prepare Handover" on Task<br>• Task Status = 'Completed' |
| **Expected Result** | • Wizard should show completed state or redirect to C360 record<br>• User cannot re-edit completed handover |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Verify completed state handling |

---

#### WIZ-4: Launch from Opportunity

| Field | Value |
|-------|-------|
| **Stage** | WIZ-4 |
| **Trigger** | Click "Prepare Handover" on Opportunity |
| **Scenario** | Click "Prepare Handover" Quick Action on Opportunity<br>• AE Task exists (Type = 'Pilot Handover AE')<br>• Task Status = 'Open'<br>• Customer_360__c Status = 'Not Started' or 'In Progress' |
| **Expected Result** | • Aura component resolves AE Task via `resolveHandoverTask`<br>• New browser tab opens with Handover Wizard (same as Task launch)<br>• Wizard loads using the resolved Task ID<br>• On completion, user is redirected back to Opportunity record |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Reuses same wizard - only entry point differs. Button visibility controlled via dynamic layouts |

---

#### WIZ-5: Launch from Opportunity - No Task Exists

| Field | Value |
|-------|-------|
| **Stage** | WIZ-5 |
| **Trigger** | Click "Prepare Handover" on Opportunity (no AE Task) |
| **Scenario** | Click "Prepare Handover" on Opportunity<br>• No Task with Type = 'Pilot Handover AE' linked to this Opportunity |
| **Expected Result** | • Error message displayed in modal:<br>"Kein Handover-Task gefunden. Bitte stellen Sie sicher, dass die Opportunity den Status 'Contract received' erreicht hat."<br>• Wizard does NOT open |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Negative test for Opportunity launch |

---

#### WIZ-6: Launch from Opportunity - Completed Task

| Field | Value |
|-------|-------|
| **Stage** | WIZ-6 |
| **Trigger** | Click "Prepare Handover" on Opportunity (completed) |
| **Scenario** | Click "Prepare Handover" on Opportunity<br>• AE Task exists with Status = 'Completed'<br>• C360 Documentation_Status__c = 'Completed' |
| **Expected Result** | • Completed state displayed (same as WIZ-3)<br>• Link to completed C360 record<br>• User cannot re-edit |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Same completed-state handling as Task launch |

---

### Category: Pre-check Section

#### PRE-1: Field Display

| Field | Value |
|-------|-------|
| **Stage** | PRE-1 |
| **Trigger** | Field Display |
| **Scenario** | Open wizard at Pre-check section<br>• Account has all fields populated:<br>  - NumberOfEmployees = 150<br>  - plOpenJobs__c = '20-49'<br>  - ParentId populated<br>  - Strategical_Key_Contact__c linked<br>  - Key_Contact__c linked |
| **Expected Result** | • Account Name displayed with hyperlink<br>• Ultimate Parent Account displayed (read-only)<br>• Parent Account in lookup field (editable)<br>• Employees field shows 150 (editable)<br>• Open Jobs dropdown shows '20-49' (editable)<br>• GTM Motion displayed (read-only)<br>• Estimated Wallet Size displayed (read-only, EUR currency format)<br>• Strategic Contact details displayed (read-only)<br>• Operational Contact details displayed (read-only) |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### PRE-2: Edit Employees Field

| Field | Value |
|-------|-------|
| **Stage** | PRE-2 |
| **Trigger** | Edit Employees |
| **Scenario** | Change NumberOfEmployees from 150 to 300<br>• Click "Entwurf speichern" |
| **Expected Result** | • Account.NumberOfEmployees updated to 300<br>• Success toast displayed<br>• Save takes ~4-7 seconds due to Account triggers |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Performance note: Account DML is slow due to triggers |

---

#### PRE-3: Edit Open Jobs Field

| Field | Value |
|-------|-------|
| **Stage** | PRE-3 |
| **Trigger** | Edit Open Jobs |
| **Scenario** | Change plOpenJobs__c from '20-49' to '50-99'<br>• Click "Weiter" |
| **Expected Result** | • Account.plOpenJobs__c updated to '50-99'<br>• Wizard navigates to Notes section<br>• Customer_360__c.Current_Wizard_Step__c = 'Notes'<br>• Timestamp_Step_PreCheck_Completed__c populated<br>• Timestamp_Step_Notes_Started__c populated |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### PRE-4: Change Parent Account

| Field | Value |
|-------|-------|
| **Stage** | PRE-4 |
| **Trigger** | Change Parent Account |
| **Scenario** | Use lookup to select different Parent Account<br>• Click "Weiter" |
| **Expected Result** | • Account.ParentId updated to new selection<br>• Ultimate Parent Account display updates (if formula recalcs) |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### PRE-5: Change Strategic Contact

| Field | Value |
|-------|-------|
| **Stage** | PRE-5 |
| **Trigger** | Change Strategic Contact |
| **Scenario** | Use contact lookup to select different Strategic Contact<br>• Click refresh button next to contact details |
| **Expected Result** | • Account.Strategical_Key_Contact__c updated<br>• Contact details (Name, Email, Phone, Title) refreshed from new Contact record |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### PRE-6: Change Operational Contact

| Field | Value |
|-------|-------|
| **Stage** | PRE-6 |
| **Trigger** | Change Operational Contact |
| **Scenario** | Use contact lookup to select different Operational Contact<br>• Click refresh button |
| **Expected Result** | • Account.Key_Contact__c updated<br>• Operational contact details refreshed |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### PRE-7: No Changes Navigation (Delta Save)

| Field | Value |
|-------|-------|
| **Stage** | PRE-7 |
| **Trigger** | No Changes Navigation |
| **Scenario** | Open Pre-check section<br>• Make NO changes<br>• Click "Weiter" |
| **Expected Result** | • Navigation is instant (no DML performed)<br>• No loading spinner visible<br>• Toast shows 'Keine Änderungen zu speichern' or navigates silently |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Delta save: skip DML when no changes |

---

### Category: Notes Section

#### NOTE-1: Required Fields - All Empty

| Field | Value |
|-------|-------|
| **Stage** | NOTE-1 |
| **Trigger** | Required Fields Validation |
| **Scenario** | Navigate to Notes section<br>• Leave ALL fields empty<br>• Click "Weiter" |
| **Expected Result** | • Validation error displayed<br>• ALL empty required fields highlighted with red border:<br>  - Customer Goals (Kundenziele)<br>  - Risks (Risiken & Red Flags)<br>  - Relationship Rating<br>  - Relationship Reason<br>  - Key Logistics<br>  - Do's<br>  - Don'ts<br>• Does NOT navigate to Review |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | All 7 fields required |

---

#### NOTE-2: Required Fields - Partial Fill

| Field | Value |
|-------|-------|
| **Stage** | NOTE-2 |
| **Trigger** | Partial Field Validation |
| **Scenario** | Fill only Customer Goals and Risks<br>• Leave other fields empty<br>• Click "Weiter" |
| **Expected Result** | • Validation error for missing fields:<br>  - Relationship Rating<br>  - Relationship Reason<br>  - Key Logistics<br>  - Do's<br>  - Don'ts<br>• Filled fields retain their values<br>• Does NOT navigate |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### NOTE-3: Fill All Required Fields

| Field | Value |
|-------|-------|
| **Stage** | NOTE-3 |
| **Trigger** | Complete Notes Form |
| **Scenario** | Fill all Notes fields:<br>• Customer Goals = 'Test goals text'<br>• Risks = 'Test risks text'<br>• Relationship Rating = 8<br>• Relationship Reason = 'Reason text'<br>• Key Logistics = 'Logistics text'<br>• Do's = 'Do this'<br>• Don'ts = 'Dont do this'<br>• Click "Weiter" |
| **Expected Result** | • All data saved to Customer_360__c:<br>  - Customer_Goals__c = 'Test goals text'<br>  - Risks__c = 'Test risks text'<br>  - Relationship_Rating__c = 8<br>  - Relationship_Reason__c = 'Reason text'<br>  - Key_Logistics__c = 'Logistics text'<br>  - Dos__c = 'Do this'<br>  - Donts__c = 'Dont do this'<br>• Navigate to Review section<br>• Timestamp_Step_Notes_Completed__c populated<br>• Timestamp_Step_Review_Started__c populated |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### NOTE-4: Back Navigation

| Field | Value |
|-------|-------|
| **Stage** | NOTE-4 |
| **Trigger** | Back Navigation |
| **Scenario** | At Notes section with data<br>• Click "Zurück" |
| **Expected Result** | • Navigate back to Pre-check<br>• Notes data preserved in UI<br>• No data loss |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### NOTE-5: Save Draft and Resume

| Field | Value |
|-------|-------|
| **Stage** | NOTE-5 |
| **Trigger** | Save Draft on Notes |
| **Scenario** | Fill some Notes fields<br>• Click "Entwurf speichern"<br>• Close browser tab<br>• Reopen wizard |
| **Expected Result** | • Partial data saved to Customer_360__c<br>• On reopen: Notes section displayed with saved data<br>• Current_Wizard_Step__c = 'Notes' |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

### Category: Review Section

#### REV-1: Data Display

| Field | Value |
|-------|-------|
| **Stage** | REV-1 |
| **Trigger** | Review Data Display |
| **Scenario** | Navigate to Review section<br>• All Pre-check and Notes data filled |
| **Expected Result** | **Pre-check Summary displayed:**<br>• Ultimate Parent Account<br>• Parent Account Name<br>• GTM Motion<br>• Employees (formatted with thousand separators)<br>• Open Jobs<br>• Estimated Wallet Size (EUR format)<br><br>**Contact Summary:**<br>• Strategic Contact: Name, Email, Title<br>• Operational Contact: Name, Email, Title<br><br>**Notes Summary:**<br>• Customer Goals<br>• Risks<br>• Relationship Rating (X / 10 format)<br>• Relationship Reason<br>• Key Logistics<br>• Do's<br>• Don'ts |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### REV-2: Submit Handover

| Field | Value |
|-------|-------|
| **Stage** | REV-2 |
| **Trigger** | Submit Handover |
| **Scenario** | At Review section<br>• Click "Handover abschließen" |
| **Expected Result** | **Customer_360__c updated:**<br>• Documentation_Status__c = 'Completed'<br>• Timestamp_Documentation_Completed__c = Now<br>• ACM_Assignment_Date__c = Today<br><br>**AE Task updated:**<br>• Status = 'Completed'<br><br>**Note:** ACM Task is NOT created here - it is created by the "Closed Won" Flow<br><br>• Success toast displayed<br>• Browser tab closes after 1.5s |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | ACM Task decoupled - created by Flow at Closed Won |

---

#### REV-3: Submit Before Closed Won

| Field | Value |
|-------|-------|
| **Stage** | REV-3 |
| **Trigger** | Submit Handover (Opp not yet Closed Won) |
| **Scenario** | AE submits handover documentation<br>• Opportunity still at "Contract Received" stage<br>• ACM Task does not exist yet |
| **Expected Result** | • C360 status = 'Completed'<br>• AE Task = 'Completed'<br>• NO ACM Task yet (will be created when Opp moves to Closed Won)<br>• This is valid - AE can complete handover before deal officially closes |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Valid scenario - handover can precede Closed Won |

---

#### REV-4: Back from Review

| Field | Value |
|-------|-------|
| **Stage** | REV-4 |
| **Trigger** | Back from Review |
| **Scenario** | At Review section<br>• Click "Zurück" |
| **Expected Result** | • Navigate back to Notes section<br>• All Review summary data preserved |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

### Category: ACM Task Flow

#### ACM-1: ACM Task Created (via Closed Won Flow)

| Field | Value |
|-------|-------|
| **Stage** | ACM-1 |
| **Trigger** | ACM Task Verification |
| **Scenario** | After Opportunity moves to "Closed Won"<br>• Login as ACM (Account Owner)<br>• Note: ACM Task is created by Flow, independent of wizard submission |
| **Expected Result** | • Task visible in ACM's task list<br>• Task Subject from $Label.Handover_ACM_Task_Subject ('Internal Handover Call planen')<br>• Task OwnerId = Account.OwnerId<br>• Task WhatId = Opportunity.Id (linked to Opportunity)<br>• Task Related_Account__c = Account.Id<br>• Task Due Date = Closed Won date + 3 working days<br>• NOTE: No Description field set by Flow |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | ACM Task created by Flow at Closed Won. Links to Opp via WhatId |

---

#### ACM-2: Complete Handover Button

| Field | Value |
|-------|-------|
| **Stage** | ACM-2 |
| **Trigger** | Open IHC Completion Form |
| **Scenario** | As ACM, open the IHC Task<br>• Click "Complete Handover" Quick Action |
| **Expected Result** | • Popup window opens<br>• Form displays:<br>  - Intro text in German<br>  - IHC Completed timestamp (required)<br>  - Documentation Quality picklist (required)<br>  - Quality Comments textarea (optional) |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | IHC Scheduled timestamp removed - not collected |

---

#### ACM-3: IHC Form - Empty Submit

| Field | Value |
|-------|-------|
| **Stage** | ACM-3 |
| **Trigger** | Empty Form Validation |
| **Scenario** | Click "Aufgabe abschließen" with empty fields |
| **Expected Result** | • Validation error displayed<br>• All 2 required fields highlighted:<br>  - IHC Completed<br>  - Documentation Quality<br>• Does NOT submit |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Only 2 required fields now (scheduled removed) |

---

#### ACM-4: IHC Form - Valid Completed Date

| Field | Value |
|-------|-------|
| **Stage** | ACM-4 |
| **Trigger** | Completed Date Validation |
| **Scenario** | Enter:<br>• IHC Completed = valid datetime<br>• Quality = OK<br>• Click submit |
| **Expected Result** | • Form submits successfully<br>• Task marked as Completed<br>• Timestamp saved to Task |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Date validation simplified (no scheduled/completed comparison) |

---

#### ACM-5: IHC Form - Valid Submit

| Field | Value |
|-------|-------|
| **Stage** | ACM-5 |
| **Trigger** | Valid IHC Submission |
| **Scenario** | Enter:<br>• IHC Completed = 2025-01-15 11:30<br>• Quality = 'Minor Gaps'<br>• Comments = 'Some fields needed clarification'<br>• Click "Aufgabe abschließen" |
| **Expected Result** | **Task updated:**<br>• Status = 'Completed'<br>• Timestamp_Internal_HO_Call_Completed__c = 2025-01-15 11:30<br>• Handover_Documentation_Quality__c = 'Minor Gaps'<br>• Handover_Quality_Comments__c = 'Some fields needed clarification'<br><br>• Success toast displayed<br>• Popup closes<br>• Page refreshes |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | IHC Scheduled not saved (removed from form) |

---

#### ACM-6: IHC Quality Options

| Field | Value |
|-------|-------|
| **Stage** | ACM-6 |
| **Trigger** | Quality Picklist Values |
| **Scenario** | Open IHC completion form<br>• Check Documentation Quality picklist |
| **Expected Result** | • Options available:<br>  - OK<br>  - Minor Gaps (filled in Internal Handover)<br>  - Major Gaps (filled in Internal Handover) |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

### Category: Time Tracking

#### TIME-1: Pre-check Time Tracking

| Field | Value |
|-------|-------|
| **Stage** | TIME-1 |
| **Trigger** | Time Tracking - Pre-check |
| **Scenario** | Open wizard at Pre-check<br>• Wait 2+ minutes<br>• Click "Weiter" to Notes |
| **Expected Result** | • Customer_360__c.Time_Spent_PreCheck_Minutes__c incremented by ~2<br>• Time tracked in background (non-blocking) |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### TIME-2: Notes Time Tracking

| Field | Value |
|-------|-------|
| **Stage** | TIME-2 |
| **Trigger** | Time Tracking - Notes |
| **Scenario** | At Notes section<br>• Wait 3+ minutes<br>• Click "Weiter" to Review |
| **Expected Result** | • Customer_360__c.Time_Spent_Notes_Minutes__c incremented by ~3 |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### TIME-3: Accumulated Time

| Field | Value |
|-------|-------|
| **Stage** | TIME-3 |
| **Trigger** | Accumulated Time Tracking |
| **Scenario** | At Pre-check, wait 2 min, go to Notes<br>• Go back to Pre-check, wait 1 min<br>• Go to Notes again |
| **Expected Result** | • Time_Spent_PreCheck_Minutes__c = ~3 (accumulated)<br>• Time for both sessions added |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### TIME-4: Time < 1 Minute Threshold

| Field | Value |
|-------|-------|
| **Stage** | TIME-4 |
| **Trigger** | Time Threshold |
| **Scenario** | Open section, immediately navigate away<br>• Time spent < 60 seconds |
| **Expected Result** | • No time saved (threshold is 1 minute)<br>• No error occurs |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Skip saving if < 1 minute |

---

### Category: Delta Save Performance

#### DELTA-1: Account Only Change

| Field | Value |
|-------|-------|
| **Stage** | DELTA-1 |
| **Trigger** | Account-only Delta Save |
| **Scenario** | At Pre-check:<br>• Change only Employees<br>• DO NOT change C360 fields<br>• Save |
| **Expected Result** | • Only Account DML executed<br>• Customer_360__c NOT updated (no changes) |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### DELTA-2: C360 Only Change

| Field | Value |
|-------|-------|
| **Stage** | DELTA-2 |
| **Trigger** | C360-only Delta Save |
| **Scenario** | At Notes:<br>• Change only Customer_Goals__c<br>• Save |
| **Expected Result** | • Only Customer_360__c DML executed<br>• Account NOT updated |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### DELTA-3: No Changes Save

| Field | Value |
|-------|-------|
| **Stage** | DELTA-3 |
| **Trigger** | No Changes Save |
| **Scenario** | Make no changes<br>• Click Save Draft |
| **Expected Result** | • Toast: 'Keine Änderungen zu speichern'<br>• No DML executed<br>• Instant response |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### DELTA-4: Multiple Field Changes

| Field | Value |
|-------|-------|
| **Stage** | DELTA-4 |
| **Trigger** | Multiple Field Delta Save |
| **Scenario** | Change:<br>• Account.NumberOfEmployees<br>• Account.plOpenJobs__c<br>• Customer_360__c.Customer_Goals__c<br>• Save |
| **Expected Result** | • Both Account and Customer_360__c updated<br>• Only changed fields in each object |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

### Category: Permissions

#### PERM-1: User Without Permission Set

| Field | Value |
|-------|-------|
| **Stage** | PERM-1 |
| **Trigger** | Access Without Permission |
| **Scenario** | Login as user without Handover_Wizard_Access<br>• Try to access wizard |
| **Expected Result** | • Error displayed<br>• Cannot view Customer_360__c records<br>• Cannot execute Apex methods |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### PERM-2: User With Permission Set

| Field | Value |
|-------|-------|
| **Stage** | PERM-2 |
| **Trigger** | Access With Permission |
| **Scenario** | Login as user with Handover_Wizard_Access<br>• Access wizard |
| **Expected Result** | • Full access to wizard<br>• Can read/write all fields<br>• Quick Actions visible |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

### Category: Edge Cases

#### EDGE-1: Long Text Fields

| Field | Value |
|-------|-------|
| **Stage** | EDGE-1 |
| **Trigger** | Long Text Input |
| **Scenario** | Enter 5000+ characters in Customer Goals<br>• Save |
| **Expected Result** | • Data truncated to field max length OR<br>• Validation error if exceeds limit |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Check field max lengths |

---

#### EDGE-2: Special Characters

| Field | Value |
|-------|-------|
| **Stage** | EDGE-2 |
| **Trigger** | Special Character Input |
| **Scenario** | Enter special characters in all text fields:<br>• Umlauts: äöüß<br>• Symbols: €@&<>"<br>• Emojis: 🎯 |
| **Expected Result** | • All characters saved correctly<br>• Displayed correctly in Review |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### EDGE-3: Browser Tab Close (Unsaved Changes)

| Field | Value |
|-------|-------|
| **Stage** | EDGE-3 |
| **Trigger** | Browser Close with Unsaved Data |
| **Scenario** | Fill Pre-check, navigate to Notes<br>• Close browser tab without saving<br>• Reopen wizard |
| **Expected Result** | • Data from last save point restored<br>• Unsaved Notes changes lost<br>• beforeunload warning shown if dirty |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Unsaved changes warning |

---

#### EDGE-4: Concurrent Edit

| Field | Value |
|-------|-------|
| **Stage** | EDGE-4 |
| **Trigger** | Concurrent Edit |
| **Scenario** | Two users open same handover simultaneously<br>• Both make changes<br>• Both save |
| **Expected Result** | • Last save wins<br>• No data corruption<br>• Consider: should we add locking? |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### EDGE-5: Empty Account Lookups

| Field | Value |
|-------|-------|
| **Stage** | EDGE-5 |
| **Trigger** | Empty Lookups |
| **Scenario** | Account has no:<br>• ParentId<br>• Strategical_Key_Contact__c<br>• Key_Contact__c |
| **Expected Result** | • Fields display as empty/placeholder<br>• No errors<br>• User can add via lookup |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

#### EDGE-6: Clear Lookup Fields

| Field | Value |
|-------|-------|
| **Stage** | EDGE-6 |
| **Trigger** | Clear Parent Account / Contact Lookups |
| **Scenario** | Account has ParentId and both contact lookups populated<br>• Clear the Parent Account lookup (set to empty)<br>• Clear the Strategic Contact lookup<br>• Click "Weiter" or "Entwurf speichern" |
| **Expected Result** | • Account.ParentId set to null<br>• Account.Strategical_Key_Contact__c set to null<br>• Changes persisted (not silently ignored)<br>• Delta save correctly distinguishes "field not sent" from "field explicitly cleared" |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Fixed: lookup clearing was previously silently ignored due to `!= null` guard |

---

#### EDGE-7: "Weiter" Save Toast Notification

| Field | Value |
|-------|-------|
| **Stage** | EDGE-7 |
| **Trigger** | Save Confirmation on "Weiter" |
| **Scenario** | At Pre-check or Notes section:<br>• Make field changes<br>• Click "Weiter" |
| **Expected Result** | • Success toast "Daten gespeichert" displayed before navigation<br>• Wizard navigates to next step<br>• If NO user changes were made (timestamp-only save), NO toast shown — silent navigation |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Toast conditioned on `hasChanges` flag to avoid misleading feedback |

---

### Category: Security

#### SEC-1: IDOR Protection - Cross-Account Rejection

| Field | Value |
|-------|-------|
| **Stage** | SEC-1 |
| **Trigger** | Crafted Save Request with Mismatched C360 |
| **Scenario** | (Developer Console / API test) Craft a `saveHandoverData` call:<br>• Valid `taskId` linked to Account A<br>• `customer360Id` belonging to Account B<br>• `employees` = 999 |
| **Expected Result** | • Request rejected with AuraHandledException<br>• Message: "Die angegebene Handover-Dokumentation gehört nicht zu dieser Aufgabe."<br>• Account B is NOT modified<br>• No partial DML committed (savepoint rollback) |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Server-side validation: taskId → WhatId → accountId cross-checked against customer360Id.Account__c |

---

#### SEC-2: IDOR Protection - Valid Same-Account Request

| Field | Value |
|-------|-------|
| **Stage** | SEC-2 |
| **Trigger** | Normal Save Request (positive control) |
| **Scenario** | Normal wizard save with matching `taskId` and `customer360Id`<br>• Both resolve to the same Account |
| **Expected Result** | • Save succeeds as normal<br>• Account and C360 fields updated correctly<br>• No regression from IDOR validation |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Positive control — existing happy-path tests cover this |

---

### Category: Full Regression

#### REG-1: Complete E2E Flow

| Field | Value |
|-------|-------|
| **Stage** | REG-1 |
| **Trigger** | Full End-to-End Regression |
| **Scenario** | Complete flow with new two-SLA trigger system:<br>**SLA 1 (Contract Received):**<br>1. Move Opportunity to "Contract Received"<br>2. Verify C360 + AE Task created (due: +1 working day)<br><br>**AE Handover:**<br>3. Open wizard via "Prepare Handover" button<br>4. Fill Pre-check section<br>5. Fill Notes section<br>6. Review and Submit<br>7. Verify AE Task = Completed, C360 = Completed<br><br>**SLA 2 (Closed Won):**<br>8. Move Opportunity to "Closed Won"<br>9. Verify ACM Task created (due: +3 working days)<br><br>**ACM Completion:**<br>10. Login as ACM<br>11. Complete IHC Task with feedback |
| **Expected Result** | All steps complete successfully as documented in individual test cases above |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | Full regression test with new two-trigger flow |

---

#### REG-2: Data Integrity Check

| Field | Value |
|-------|-------|
| **Stage** | REG-2 |
| **Trigger** | Data Integrity Verification |
| **Scenario** | After completing E2E:<br>• Query Customer_360__c record<br>• Verify all fields populated correctly<br>• Verify all timestamps present |
| **Expected Result** | • All fields have expected values<br>• All timestamp fields populated<br>• No NULL in required fields |
| **Observed Result** | |
| **Test Records** | |
| **Sandbox** | ⬜ |
| **Review** | ⬜ |
| **Production** | ⬜ |
| **Follow-Up** | |

---

## Test Summary

| Category | Total Tests | Passed (Sandbox) | Passed (Review) | Passed (Prod) |
|----------|-------------|------------------|-----------------|---------------|
| Flow Trigger - SLA 1 (Contract Received) | 3 | | | |
| Flow Trigger - SLA 2 (Closed Won) | 4 | | | |
| Wizard Launch | 6 | | | |
| Pre-check Section | 7 | | | |
| Notes Section | 5 | | | |
| Review Section | 4 | | | |
| ACM Task Flow | 6 | | | |
| Time Tracking | 4 | | | |
| Delta Save | 4 | | | |
| Permissions | 2 | | | |
| Edge Cases | 7 | | | |
| Security | 2 | | | |
| Regression | 2 | | | |
| **TOTAL** | **56** | | | |

---

## Sign-Off

| Environment | Tested By | Date | Approved By | Date |
|-------------|-----------|------|-------------|------|
| Sandbox | | | | |
| Review | | | | |
| Production | | | | |

---

# Part 2: Test Data Loading Instructions

The `test-data/` folder contains CSV files for creating test data in the sandbox using Salesforce Data Loader.

## Overview

| File | Object | Count | Dependencies |
|------|--------|-------|--------------|
| `01_accounts_parents.csv` | Account | 10 | None |
| `02_accounts_children.csv` | Account | 40 | Parent Accounts |
| `03_contacts.csv` | Contact | 200 | Child Accounts |
| `03b_contacts_parents.csv` | Contact | 50 | Parent Accounts |
| `04_opportunities_sales.csv` | Opportunity | 37 | Accounts 001-037 |
| `05_opportunities_closedwon.csv` | Opportunity | 3 | Accounts 038-040 |
| `06_opportunities_account_mgmt.csv` | Opportunity | 3 | Accounts 038-040 |

**Total Records:** 343 (50 Accounts + 250 Contacts + 43 Opportunities)

---

## Pre-requisites

1. **Salesforce Data Loader** installed and configured
2. **Sandbox credentials** with Account/Contact/Opportunity create permissions
3. Access to **Developer Console** to run SOQL queries

---

## Step 1: Get Record Type IDs

Run these SOQL queries in Developer Console to get the Record Type IDs:

### Account Record Types
```sql
SELECT Id, DeveloperName, Name 
FROM RecordType 
WHERE SObjectType = 'Account' AND DeveloperName = 'Sales'
```
Copy the **Id** value - this is `{{ACCOUNT_SALES_RT_ID}}`

### Opportunity Record Types
```sql
SELECT Id, DeveloperName, Name 
FROM RecordType 
WHERE SObjectType = 'Opportunity' 
AND DeveloperName IN ('Sales', 'Account_Management')
```
Copy the IDs:
- **Sales** Id → `{{OPP_SALES_RT_ID}}`
- **Account_Management** Id → `{{OPP_ACCTMGMT_RT_ID}}`

---

## Step 2: Prepare CSV Files

### 2.1 Replace Placeholders in Account Files

Open `01_accounts_parents.csv` and `02_accounts_children.csv`:
- Replace all `{{ACCOUNT_SALES_RT_ID}}` with the actual Account Sales Record Type ID

### 2.2 Replace Placeholders in Opportunity Files

Open `04_opportunities_sales.csv` and `05_opportunities_closedwon.csv`:
- Replace all `{{OPP_SALES_RT_ID}}` with the actual Opportunity Sales Record Type ID

Open `06_opportunities_account_mgmt.csv`:
- Replace all `{{OPP_ACCTMGMT_RT_ID}}` with the actual Opportunity Account_Management Record Type ID

---

## Step 3: Load Data in Order

### 3.1 Load Parent Accounts

1. Open Data Loader → Insert
2. Select Object: **Account**
3. Select CSV: `01_accounts_parents.csv`
4. Map fields:
   - `Name` → `Name`
   - `RecordTypeId` → `RecordTypeId`
   - `Service_Country__c` → `Service_Country__c`
   - `NumberOfEmployees` → `NumberOfEmployees`
   - `BillingCountry` → `BillingCountry`
   - `BillingCity` → `BillingCity`
   - `Umbrella_Company__c` → `Umbrella_Company__c`
5. Click **Finish** and save the success file

### 3.2 Export Parent Account IDs

Run this query to get the new Account IDs:
```sql
SELECT Id, Name 
FROM Account 
WHERE Name LIKE 'HO_Test_Parent_%'
ORDER BY Name
```

### 3.3 Prepare Child Accounts CSV

1. Open `02_accounts_children.csv` in Excel/Sheets
2. Create a VLOOKUP to populate `ParentId` using `Parent_Name_Reference`:
   - Import the parent account IDs from step 3.2
   - Use VLOOKUP: `=VLOOKUP(I2, ParentData!$A$2:$B$11, 2, FALSE)` (adjust range as needed)
3. Copy-paste the VLOOKUP results as values in the `ParentId` column
4. Delete the `Parent_Name_Reference` column before loading
5. Save the file

### 3.4 Load Child Accounts

1. Data Loader → Insert → Account
2. Select updated `02_accounts_children.csv`
3. Map all fields including `ParentId`
4. Save the success file

### 3.5 Export All Test Account IDs

```sql
SELECT Id, Name 
FROM Account 
WHERE Name LIKE 'HO_Test_Account_%' OR Name LIKE 'HO_Test_Parent_%'
ORDER BY Name
```

### 3.6 Prepare Contact CSVs

1. Open `03_contacts.csv` and `03b_contacts_parents.csv`
2. Use VLOOKUP to populate `AccountId` using `Account_Name_Reference`
3. Delete the `Account_Name_Reference` column before loading
4. Save the files

### 3.7 Load Contacts

1. Data Loader → Insert → Contact
2. Load `03b_contacts_parents.csv` first (parent account contacts)
3. Then load `03_contacts.csv` (child account contacts)

### 3.8 Prepare Opportunity CSVs

1. Open `04_opportunities_sales.csv`, `05_opportunities_closedwon.csv`, `06_opportunities_account_mgmt.csv`
2. Use VLOOKUP to populate `AccountId` using `Account_Name_Reference`
3. Delete the `Account_Name_Reference` column before loading
4. Save the files

### 3.9 Load Opportunities

**Important Order:**

1. Load `05_opportunities_closedwon.csv` FIRST
   - These are the "Closed Won" Sales opportunities that will trigger the Flow
   - The Flow will create Customer_360__c records and AE Tasks

2. Load `04_opportunities_sales.csv`
   - These are "Contract Received" stage - will NOT trigger Flow yet
   - You can manually move them to "Closed Won" to test Flow triggers

3. Load `06_opportunities_account_mgmt.csv` LAST
   - These are "Account_Management" record type at "Contract Received"
   - **Negative Test Case:** Moving these to "Closed Won" should NOT trigger Flow

---

## Step 4: Verify Test Data

### Count Verification
```sql
-- Accounts
SELECT COUNT() FROM Account WHERE Name LIKE 'HO_Test_%'
-- Expected: 50

-- Contacts
SELECT COUNT() FROM Contact WHERE Account.Name LIKE 'HO_Test_%'
-- Expected: 250

-- Opportunities
SELECT COUNT() FROM Opportunity WHERE Name LIKE 'HO_Test_%'
-- Expected: 43

-- Customer_360__c (after Closed Won opps are loaded)
SELECT COUNT() FROM Customer_360__c WHERE Account__r.Name LIKE 'HO_Test_%'
-- Expected: 3 (from the 3 Closed Won opportunities)
```

### Hierarchy Verification
```sql
SELECT Name, Parent.Name 
FROM Account 
WHERE Name LIKE 'HO_Test_Account_%' 
AND ParentId != null
ORDER BY Name
-- Should return 40 records with parent names
```

---

## Test Scenarios with Test Data

### Scenario A: Normal Flow Trigger (Accounts 001-037)
1. Select any "Contract Received" opportunity (HO_Test_Opp_001 to HO_Test_Opp_037)
2. Set `Allow_Closed_Won__c = true`
3. Change StageName to "Closed Won"
4. Save
5. **Expected:** Flow creates Customer_360__c record + AE Task

### Scenario B: Pre-existing Closed Won + AM Upsell (Accounts 038-040)
1. These accounts already have Closed Won Sales opportunities
2. They also have "Account_Management" opportunities at "Contract Received"
3. Close the AM opportunity as Won:
   - Set `Allow_Closed_Won__c = true`
   - Change StageName to "Closed Won"
4. **Expected:** Flow should NOT create another Customer_360__c record

### Scenario C: Contact Lookup Testing
1. Open any test Account (e.g., HO_Test_Account_001)
2. Verify 5 contacts exist
3. Verify CEO contact can be selected as Strategic Contact
4. Verify HR Manager can be selected as Operational Contact

---

## Update Account Contact Lookups

After loading contacts, you may want to link Strategic and Operational contacts to accounts. Here's a sample update file structure:

```csv
Id,Strategical_Key_Contact__c,Key_Contact__c
<account_id>,<ceo_contact_id>,<hr_manager_contact_id>
```

Query to get CEO contacts:
```sql
SELECT AccountId, Id, Name 
FROM Contact 
WHERE Title = 'CEO' 
AND Account.Name LIKE 'HO_Test_%'
```

Query to get HR Manager contacts:
```sql
SELECT AccountId, Id, Name 
FROM Contact 
WHERE Title = 'HR Manager' 
AND Account.Name LIKE 'HO_Test_%'
```

---

## Cleanup

To remove all test data after testing:

```sql
-- Delete in reverse order
DELETE [SELECT Id FROM Opportunity WHERE Name LIKE 'HO_Test_%'];
DELETE [SELECT Id FROM Contact WHERE Account.Name LIKE 'HO_Test_%'];
DELETE [SELECT Id FROM Customer_360__c WHERE Account__r.Name LIKE 'HO_Test_%'];
DELETE [SELECT Id FROM Account WHERE Name LIKE 'HO_Test_%'];
```

**Note:** Run these as Anonymous Apex in Developer Console, not SOQL.

---

## Troubleshooting

### Validation Rule Errors

**"Please populate service country on account"**
- Ensure `Service_Country__c = 'DE'` is in all account records (already set)

**"Cannot close opportunity as Won"**
- Ensure `Allow_Closed_Won__c = true` before changing stage to "Closed Won"

**"Account creation restricted"**
- Your profile may not have permission. Contact admin or use System Administrator profile.

### Parent Account Lookup Fails
- Ensure parent accounts are loaded and committed before loading children
- Verify Parent IDs are correct 18-character Salesforce IDs

### Flow Not Triggering
- Verify Flow `Opportunity_Closed_Won_Create_Handover` is activated
- Check Flow entry criteria matches your opportunity record type
- Review Debug Logs for Flow execution

---

# Part 3: Deployment History

## Phase 3 Deployment

Phase 3 introduced schema changes, LWC updates, and Apex service modifications for the Handover Wizard.

### Deployment Sequence

**Step 1: Deploy New Components & Fields (additive changes)**

```bash
sfdx force:source:deploy -p force-app -u handover-sandbox -w 10
```

Or using the manifest:
```bash
sfdx force:source:deploy -x manifest/package-phase3.xml -u handover-sandbox -w 10
```

**Step 2: Delete Deprecated Fields (destructive changes)**

After verifying Step 1 works, delete the old fields:

```bash
sfdx force:mdapi:deploy -d manifest -u handover-sandbox -w 10 --ignorewarnings
```

Note: For destructive deployment, the manifest folder needs:
- `package.xml` (use package-empty.xml renamed to package.xml)
- `destructiveChanges.xml` (use destructiveChanges-phase3.xml renamed)

Alternatively, manual destructive deployment:
```bash
mkdir -p destructive-deploy
cp manifest/package-empty.xml destructive-deploy/package.xml
cp manifest/destructiveChanges-phase3.xml destructive-deploy/destructiveChanges.xml
sfdx force:mdapi:deploy -d destructive-deploy -u handover-sandbox -w 10 --ignorewarnings
```

### Phase 3 Schema Changes (Customer_360__c)

| Change Type | Field |
|-------------|-------|
| Modified | `Type__c` (added "Pilot Handover" option) |
| New | `Documentation_Status__c` (picklist) |
| New | `Timestamp_Documentation_Completed__c` (DateTime) |
| Deleted | `Documentation_Completed__c` |
| Deleted | `Documentation_Completion_Date__c` |
| Deleted | `Hierarchy_Status__c` |

### Phase 3 Apex Changes

| File | Changes |
|------|---------|
| `HandoverService.cls` | Removed hierarchy task creation, added `initializeHandover()`, `completeHandover()`, `getContactDetails()` methods |

### Phase 3 LWC Changes

| Component | Changes |
|-----------|---------|
| `handoverWizardContainer` | Updated data model (role→title), removed hierarchyStatus, added parentAccountId |
| `handoverSectionPreChecks` | Removed hierarchy section, added Ultimate Parent (read-only) + Parent Account (lookup), Contact "Refresh" button, Title field |
| `handoverSectionReviewSubmit` | Updated to show Ultimate Parent, Parent Account, Contact Title |

---

## Opportunity "Prepare Handover" Button Deployment

Added a "Prepare Handover" button on the Opportunity object that reuses the existing Task-based wizard.

### Deployed Components

```bash
sfdx force:source:deploy -p \
  force-app/main/default/classes/HandoverService.cls,\
  force-app/main/default/classes/HandoverService.cls-meta.xml,\
  force-app/main/default/classes/HandoverServiceTest.cls,\
  force-app/main/default/classes/HandoverServiceTest.cls-meta.xml,\
  force-app/main/default/aura/PrepareHandoverAction,\
  force-app/main/default/lwc/handoverWizardContainer,\
  force-app/main/default/pages/HandoverWizardPage.page,\
  force-app/main/default/pages/HandoverWizardPage.page-meta.xml,\
  force-app/main/default/quickActions/Opportunity.Prepare_Handover.quickAction-meta.xml \
  --targetusername handover-sandbox -w 10
```

### Changes

| Component | Type | Change |
|-----------|------|--------|
| `HandoverService.cls` | ApexClass | Added `resolveHandoverTask(opportunityId)` method |
| `HandoverServiceTest.cls` | ApexClass | Added 3 tests for `resolveHandoverTask` |
| `PrepareHandoverAction` (Aura) | AuraBundle | Made object-aware via `force:hasSObjectName`; routes Task vs Opportunity launches |
| `handoverWizardContainer` (LWC) | LWC | Added `sourceObjectApiName`, `sourceRecordId` for return navigation |
| `HandoverWizardPage.page` | VF Page | Passes `c__sourceObjectApiName`, `c__sourceRecordId` URL params to LWC |
| `Opportunity.Prepare_Handover` | QuickAction | **New** — Lightning Component quick action on Opportunity |
| `package.xml` | Manifest | Added `Opportunity.Prepare_Handover` to QuickAction members |

### Post-Deployment Steps

1. Add "Prepare Handover" button to the Opportunity page layout via Dynamic Actions
2. Configure visibility rules (e.g., Stage = 'Contract Received' or later)

---

## Code Quality & Security Fixes (Round 1)

### Deployed Components

```bash
sfdx force:source:deploy -p \
  force-app/main/default/classes/HandoverService.cls,\
  force-app/main/default/classes/HandoverService.cls-meta.xml,\
  force-app/main/default/lwc/handoverWizardContainer,\
  force-app/main/default/permissionsets/Handover_Wizard_Access.permissionset-meta.xml \
  --targetusername handover-sandbox -w 10
```

### Changes

| # | Finding | Fix |
|---|---------|-----|
| 1 | `without sharing` on HandoverService | Added detailed security justification comment |
| 2 | `HandoverDTO.cls` orphaned dead code | Removed from permission set; class moved to `unrelated/` |
| 3 | `Schema.getGlobalDescribe()` anti-pattern | Replaced with `Schema.describeSObjects()` |
| 4 | Task due date documentation conflicts | Updated stakeholder decisions & release checklist (both use working days) |
| 5 | `WhatId` prefix hardcoding (`startsWith('006')`) | Replaced with `Id.getSObjectType()` in all 4 occurrences |
| 6 | Duplicate SOQL in `completeACMTask` | Merged two Opportunity queries into one |
| 7 | Unnecessary `@AuraEnabled` on `HandoverSaveRequest` | Removed all annotations from inner wrapper class |
| 8 | `console.log` in production LWC | Removed from `handoverWizardContainer.js` |
| 9 | Mixed language in error messages | Translated all English toast/error messages to German |
| 10 | `_hasChanges` flag mixed into request payload | Refactored `buildSaveRequest` to return `{ request, hasChanges }` |

---

## Critical Bug Fixes & Security Hardening (Round 2)

### Deployed Components

```bash
# Deploy 1: Bug fixes + security
sfdx force:source:deploy -p \
  force-app/main/default/classes/HandoverService.cls,\
  force-app/main/default/classes/HandoverService.cls-meta.xml,\
  force-app/main/default/classes/HandoverServiceTest.cls,\
  force-app/main/default/classes/HandoverServiceTest.cls-meta.xml,\
  force-app/main/default/lwc/acmTaskCompletion,\
  force-app/main/default/lwc/handoverWizardContainer,\
  force-app/main/default/lwc/handoverSectionPreChecks \
  --targetusername handover-sandbox -w 10

# Deploy 2: IDOR cross-validation tightening
sfdx force:source:deploy -p \
  force-app/main/default/classes/HandoverService.cls,\
  force-app/main/default/classes/HandoverService.cls-meta.xml,\
  force-app/main/default/classes/HandoverServiceTest.cls,\
  force-app/main/default/classes/HandoverServiceTest.cls-meta.xml \
  --targetusername handover-sandbox -w 10
```

### Critical Bugs Fixed

| # | Bug | Fix |
|---|-----|-----|
| 1 | **ACM completion blocked** — `validateForm()` still required `ihcScheduledTimestamp` (removed field) | Removed scheduled field from HTML template, JS validation, handler, and help text. Form now requires only 2 fields: completed timestamp + quality |
| 2 | **Unit tests would fail** — `testInitializeHandover_AccountLinkedTask` and `_CreatesCustomer360` called `initializeHandover` without pre-creating C360 | Pre-insert C360 in first two tests; renamed third test to `_NoCustomer360ThrowsError` to test the error path |
| 3 | **IDOR vulnerability** — `saveHandoverData` accepted `accountId` from client without validation | Two-phase fix: (a) resolve `accountId` from `customer360Id` server-side, (b) cross-validate `customer360Id.Account__c` against `taskId`→WhatId→Account. Mismatches are rejected before any DML |

### Medium Issues Fixed

| # | Issue | Fix |
|---|-------|-----|
| 4 | `HandoverDTO.cls` orphaned | Already in `unrelated/` — confirmed |
| 5 | Resume validity check only checked 4 of 7 Notes fields | Now checks all 7: `customerGoals`, `risks`, `relationshipRating`, `relationshipReason`, `keyLogistics`, `dos`, `donts` |
| 6 | Lookup fields could not be explicitly cleared (null silently ignored) | Removed `!= null` guard from `parentAccountId`, `strategicContactId`, `operationalContactId`; `dataMap.containsKey()` alone controls update |
| 7 | `console.error` calls remaining in production LWC | Removed all 8 calls across `handoverWizardContainer`, `handoverSectionPreChecks`, and `acmTaskCompletion` |

---

## UX Polish: "Weiter" Save Toast

### Deployed Component

```bash
sfdx force:source:deploy -p force-app/main/default/lwc/handoverWizardContainer \
  --targetusername handover-sandbox -w 10
```

### Change

When "Weiter" is clicked and user-entered data was actually saved (i.e., `hasChanges` is true), a success toast "Daten gespeichert" is now shown before navigating to the next step. Timestamp-only saves (no user field changes) remain silent.

---

### Production Deployment Notes

1. Always deploy to sandbox first and test thoroughly
2. Run destructive changes only after confirming new components work
3. Consider deploying during low-traffic periods
4. Have a rollback plan ready
5. After deploying Opportunity Quick Action, add the button to Opportunity page layouts via Dynamic Actions

---

*Document Version: 2.0*
*Last Updated: 20 February 2026*
