"""
Test Data Loader — 90 Day Onboarding Framework
Loads test data from data/ CSVs into the 90day sandbox in dependency order.

Load order:
  1. Parent Accounts       (01_accounts_parents.csv)
  2. Child Accounts        (02_accounts_children.csv — needs parent IDs)
  3. Parent Contacts       (03b_contacts_parents.csv — needs parent account IDs)
  4. Child Contacts        (03_contacts.csv — needs child account IDs)
  5. Closed Won Opps       (05_opportunities_closedwon.csv — needs child account IDs)
  6. Sales Opps            (04_opportunities_sales.csv — needs child account IDs)
  7. Account Mgmt Opps     (06_opportunities_account_mgmt.csv — needs child account IDs)
"""

import subprocess
import json
import csv
import os
import tempfile

ORG = "90day"
DATA_DIR = os.path.expanduser(
    "~/Desktop/90 Day Onboarding Framework/data"
)
WORK_DIR = tempfile.mkdtemp(prefix="ho_data_load_")

print(f"Working directory for prepared CSVs: {WORK_DIR}\n")


# ── helpers ──────────────────────────────────────────────────────────────────

def run_query(soql):
    result = subprocess.run(
        ["sf", "data", "query", "--query", soql,
         "--target-org", ORG, "--json"],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    if data.get("status", 1) != 0:
        raise RuntimeError(f"Query failed: {data}")
    return data["result"]["records"]


def bulk_insert(sobject, csv_file, allow_failure=False):
    print(f"  Loading {sobject} from {os.path.basename(csv_file)} ...")
    result = subprocess.run(
        ["sf", "data", "import", "bulk",
         "--sobject", sobject,
         "--file", csv_file,
         "--target-org", ORG,
         "--wait", "10",
         "--line-ending", "LF",
         "--json"],
        capture_output=True, text=True,
        env={**os.environ, "NO_COLOR": "1", "CI": "true"}
    )
    try:
        data = json.loads(result.stdout)
        status = data.get("status", 1)
        if status == 0:
            res = data.get("result", {})
            print(f"  ✅ Success — {res.get('numberRecordsProcessed', '?')} processed, "
                  f"{res.get('numberRecordsFailed', '?')} failed")
        else:
            msg = data.get("message", result.stderr.strip())
            if allow_failure:
                print(f"  ⚠️  Skipped (allowed failure): {msg}")
            else:
                print(f"  ❌ Failed: {msg}")
                raise RuntimeError(f"Bulk insert failed for {sobject}")
    except json.JSONDecodeError:
        print("  Raw output:", result.stdout[:500])
        if result.returncode != 0 and not allow_failure:
            raise RuntimeError(f"Bulk insert failed for {sobject}")
    print()


def prepare_csv(input_file, output_file, id_map, id_col, ref_col, field_overrides=None):
    """
    Replaces {{ACCOUNT_ID}} / {{PARENT_ID}} placeholders in id_col
    using ref_col as the lookup key into id_map.
    Removes the ref_col from the output.
    field_overrides: optional dict of {field: value} to force on every row.
    """
    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = [c for c in reader.fieldnames if c != ref_col]

    # Add any override columns not already present in source CSV
    if field_overrides:
        for field in field_overrides:
            if field not in fieldnames:
                fieldnames.append(field)

    missing = []
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            ref_name = row.get(ref_col, "").strip()
            actual_id = id_map.get(ref_name)
            if actual_id:
                row[id_col] = actual_id
            else:
                missing.append(ref_name)
            row.pop(ref_col, None)
            if field_overrides:
                for field, value in field_overrides.items():
                    row[field] = value
            writer.writerow(row)

    if missing:
        unique_missing = sorted(set(missing))
        print(f"  WARNING: {len(unique_missing)} reference(s) not resolved:")
        for m in unique_missing[:10]:
            print(f"    - {m}")
        if len(unique_missing) > 10:
            print(f"    ... and {len(unique_missing) - 10} more")

    return output_file


def build_id_map(records, name_field="Name"):
    return {r[name_field]: r["Id"] for r in records}


def count_existing(soql):
    """Returns totalSize for a COUNT() SOQL query."""
    result = subprocess.run(
        ["sf", "data", "query", "--query", soql,
         "--target-org", ORG, "--json"],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data["result"]["totalSize"]


# ── Step 1: Parent Accounts ───────────────────────────────────────────────────

print("=" * 60)
print("STEP 1: Loading Parent Accounts")
print("=" * 60)
if count_existing("SELECT COUNT() FROM Account WHERE Name LIKE 'HO_Test_Parent_%'") == 0:
    bulk_insert("Account", os.path.join(DATA_DIR, "01_accounts_parents.csv"))
else:
    print("  ⏭  Already loaded — skipping.\n")

parent_records = run_query(
    "SELECT Id, Name FROM Account WHERE Name LIKE 'HO_Test_Parent_%' ORDER BY Name"
)
parent_map = build_id_map(parent_records)
print(f"  Queried {len(parent_map)} parent accounts.\n")


# ── Step 2: Child Accounts ────────────────────────────────────────────────────

print("=" * 60)
print("STEP 2: Loading Child Accounts")
print("=" * 60)
if count_existing("SELECT COUNT() FROM Account WHERE Name LIKE 'HO_Test_Account_%'") == 0:
    child_csv = os.path.join(WORK_DIR, "02_accounts_children_ready.csv")
    prepare_csv(
        os.path.join(DATA_DIR, "02_accounts_children.csv"),
        child_csv,
        id_map=parent_map,
        id_col="ParentId",
        ref_col="Parent_Name_Reference"
    )
    bulk_insert("Account", child_csv)
else:
    print("  ⏭  Already loaded — skipping.\n")

all_account_records = run_query(
    "SELECT Id, Name FROM Account "
    "WHERE Name LIKE 'HO_Test_Account_%' OR Name LIKE 'HO_Test_Parent_%' "
    "ORDER BY Name"
)
account_map = build_id_map(all_account_records)
print(f"  Queried {len(account_map)} accounts (parents + children).\n")


# ── Step 3: Parent Contacts ───────────────────────────────────────────────────

print("=" * 60)
print("STEP 3: Loading Parent Account Contacts")
print("=" * 60)
if count_existing("SELECT COUNT() FROM Contact WHERE Account.Name LIKE 'HO_Test_Parent_%'") == 0:
    contacts_parents_csv = os.path.join(WORK_DIR, "03b_contacts_parents_ready.csv")
    prepare_csv(
        os.path.join(DATA_DIR, "03b_contacts_parents.csv"),
        contacts_parents_csv,
        id_map=account_map,
        id_col="AccountId",
        ref_col="Account_Name_Reference"
    )
    bulk_insert("Contact", contacts_parents_csv)
else:
    print("  ⏭  Already loaded — skipping.\n")


# ── Step 4: Child Contacts ────────────────────────────────────────────────────

print("=" * 60)
print("STEP 4: Loading Child Account Contacts")
print("=" * 60)
if count_existing("SELECT COUNT() FROM Contact WHERE Account.Name LIKE 'HO_Test_Account_%'") == 0:
    contacts_csv = os.path.join(WORK_DIR, "03_contacts_ready.csv")
    prepare_csv(
        os.path.join(DATA_DIR, "03_contacts.csv"),
        contacts_csv,
        id_map=account_map,
        id_col="AccountId",
        ref_col="Account_Name_Reference"
    )
    bulk_insert("Contact", contacts_csv)
else:
    print("  ⏭  Already loaded — skipping.\n")


# ── Step 5: Closed Won Opportunities (load first — triggers flow) ─────────────

print("=" * 60)
print("STEP 5: Loading Closed Won Opportunities")
print("=" * 60)
if count_existing("SELECT COUNT() FROM Opportunity WHERE RecordTypeId = '0121v000000z2JFAAY' AND Account.Name LIKE 'HO_Test_Account_03%'") == 0:
    closedwon_csv = os.path.join(WORK_DIR, "05_closedwon_ready.csv")
    prepare_csv(
        os.path.join(DATA_DIR, "05_opportunities_closedwon.csv"),
        closedwon_csv,
        id_map=account_map,
        id_col="AccountId",
        ref_col="Account_Name_Reference",
        field_overrides={"StageName": "Currently in Contact"}  # org flow blocks closed stages on insert
    )
    bulk_insert("Opportunity", closedwon_csv)
else:
    print("  ⏭  Already loaded — skipping.\n")


# ── Step 6: Sales Opportunities (Contract Received) ───────────────────────────

print("=" * 60)
print("STEP 6: Loading Sales Opportunities (Contract Received)")
print("=" * 60)
if count_existing("SELECT COUNT() FROM Opportunity WHERE RecordTypeId = '0121v000000z2JFAAY' AND Account.Name LIKE 'HO_Test_Account_00%'") == 0:
    sales_csv = os.path.join(WORK_DIR, "04_sales_ready.csv")
    prepare_csv(
        os.path.join(DATA_DIR, "04_opportunities_sales.csv"),
        sales_csv,
        id_map=account_map,
        id_col="AccountId",
        ref_col="Account_Name_Reference",
        field_overrides={"StageName": "Currently in Contact"}
    )
    bulk_insert("Opportunity", sales_csv)
else:
    print("  ⏭  Already loaded — skipping.\n")


# ── Step 7: Account Management Opportunities ──────────────────────────────────

print("=" * 60)
print("STEP 7: Loading Account Management Opportunities")
print("=" * 60)
if count_existing("SELECT COUNT() FROM Opportunity WHERE RecordTypeId = '0120Y000000Ay9JQAS' AND Account.Name LIKE 'HO_Test_%'") == 0:
    acctmgmt_csv = os.path.join(WORK_DIR, "06_acctmgmt_ready.csv")
    prepare_csv(
        os.path.join(DATA_DIR, "06_opportunities_account_mgmt.csv"),
        acctmgmt_csv,
        id_map=account_map,
        id_col="AccountId",
        ref_col="Account_Name_Reference",
        field_overrides={
            "StageName": "Pitch & Negotiation",
            "Competitor_1_current_future__c": "Unknown",
            "Competitor_2_current_future__c": "Unknown",
            "Competitor_3_current_future__c": "Unknown",
        }
    )
    bulk_insert("Opportunity", acctmgmt_csv)
else:
    print("  ⏭  Already loaded — skipping.\n")


# ── Verification ──────────────────────────────────────────────────────────────

print("=" * 60)
print("VERIFICATION")
print("=" * 60)

checks = [
    ("Accounts (all HO_Test_*)", "SELECT COUNT() FROM Account WHERE Name LIKE 'HO_Test_%'", 50),
    ("Contacts", "SELECT COUNT() FROM Contact WHERE Account.Name LIKE 'HO_Test_%'", 250),
    ("Opportunities", "SELECT COUNT() FROM Opportunity WHERE Account.Name LIKE 'HO_Test_Account_%'", 43),
]

all_ok = True
for label, soql, expected in checks:
    records = run_query(soql)
    r = records[0] if records else {}
    count = r.get("expr0") or r.get("COUNT()") or r.get("count") or len(records)
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0
    status = "✅" if count == expected else "⚠️ "
    if count != expected:
        all_ok = False
    print(f"  {status}  {label}: {count} (expected {expected})")

print()
if all_ok:
    print("All counts match. Test data loaded successfully.")
else:
    print("Some counts differ — check the warnings above.")
