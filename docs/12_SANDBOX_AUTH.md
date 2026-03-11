# Sandbox authentication (90day)

**Purpose:** Reference for the project-specific sandbox. No secrets are stored in this file or in the repo.

---

## Stored in this project (safe to commit)

| Item | Value |
|------|--------|
| **Org alias** | `90day-sandbox` |
| **Username** | `arun.kumar@heyjobs.de.90day` |
| **Instance URL (API)** | `https://heyjobs--90day.sandbox.my.salesforce.com` |
| **Lightning URL** | `https://heyjobs--90day.sandbox.lightning.force.com/lightning/page/home` |
| **Login host (sandbox)** | `https://test.salesforce.com` |

Use the alias with the CLI: `-u 90day-sandbox` or `--target-org 90day-sandbox`.

---

## Not stored in the project (by design)

- **Passwords** and **access tokens** are never committed. The Salesforce CLI stores them locally under `.sf/` (and `.sfdx/`), which are listed in `.gitignore`.
- Anyone cloning the repo must run the login command below with their own credentials.

---

## How to authenticate (or re-authenticate)

From the project root:

```bash
sf org login web --instance-url https://test.salesforce.com --alias 90day-sandbox
```

A browser opens; sign in with the sandbox username and your password. The CLI will store the session locally.

To confirm:

```bash
sf org display --target-org 90day-sandbox
```

---

## If this file becomes sensitive

If your team decides that even usernames or instance URLs should not live in the repo (e.g. for compliance), you can:

1. Remove this file from version control and add `docs/SANDBOX_AUTH.md` to `.gitignore`, or  
2. Replace specific values with placeholders (e.g. `YOUR_SANDBOX_USERNAME`) and keep only the re-auth instructions.

For most teams, documenting alias and login URL is acceptable; the critical rule is **never commit passwords or tokens**.
