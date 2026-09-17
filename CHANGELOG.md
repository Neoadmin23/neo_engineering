# Changelog

All notable changes to the NeoEngineering app. Versioning follows
[SemVer](https://semver.org): MAJOR.MINOR.PATCH — breaking / feature / fix.

## [1.9.1] — 2026-09-12
### Fixed / Changed — resilient demo loading
- A failure mid-load could roll back most of the dataset, leaving only
  early records (leads/opportunities) — matching the reported symptom.
  The loader now runs **each project in its own savepoint and commits on
  success**: one failing project can no longer erase the others, and
  masters persist regardless.
- The Load Demo Data dialog now reports **per-project results** — ✔/✘ per
  project with the exact error text for any failure (also written to the
  Error Log with the project name), so the root cause is visible without
  terminal access.
- Delete Demo Data additionally removes orphan Project Briefs left by
  partial loads.

## [1.9.0] — 2026-09-11
### Changed — richer demo masters
- Demo now creates a proper bilingual **Engineering Services item group**
  with three service items: Design Services, Supervision Services (sales)
  and Execution Works (purchase, used by the PO/Invoice leg) — replacing
  the single generic demo item.
- Demo Quotations are now a realistic two-line proposal: design fee (40%)
  + supervision fee (60%) of the contract value, with bilingual line
  descriptions.
- Leads now carry the `company` field (your transacting company) in
  addition to the organization name — previously blank.
- Cleanup removes all three items and the item group (link-checked, never
  forced).

### Upgrade note
- If demo data from an earlier version is loaded, run Delete Demo Data
  before loading again so quotations rebuild on the new items.

## [1.8.2] — 2026-09-10
### Changed
- Delete Demo Data now also removes the demo masters — Customers,
  Suppliers, Project Types, demo UOMs and the demo Item — but only when
  no other transactions link to them. Frappe's link validation is used as
  the check (no force-delete), so any master referenced by real records
  is kept and reported in the output instead.

## [1.8.1] — 2026-09-10
### Fixed
- Demo load failed with "Value missing for Opportunity: Company /
  Opportunity Date": both Opportunity creators (project chain and
  pipeline extras) now set `company` and `transaction_date`.

## [1.8.0] — 2026-09-10
### Added — complete CRM cycle in the demo
- Every demo project now starts from the front of the funnel:
  **Lead** (engineering fields filled: type, location, budget, services) →
  **Project Brief** (linked to the lead) → **Opportunity** (Converted,
  linked to the brief, service type set) → **submitted Quotation**
  (proposal Rev 1 against the demo services item, marked Ordered) →
  Project. Lead flips to Converted and the brief carries both back-links,
  so the customer can click through the whole chain in either direction.
- **Live pipeline extras**: one open Lead ("Riyadh Schools Extension") and
  one Opportunity at Quotation stage with a draft proposal — the funnel
  shows motion, not just history.
- Quotation creation is defensive (skips with logged guidance if selling
  defaults are missing); demo Item now created with the masters.
- Cleanup extended: delete_demo_data removes demo Quotations,
  Opportunities and Leads (including the pipeline extras).

## [1.7.1] — 2026-09-09
### Fixed
- Demo loading failed with "Workflow State transition not allowed from
  Draft to Approved": demo records are seeded directly in their
  illustrative states, and `frappe.flags.in_import` does not bypass
  workflow transition validation on all builds. Seeding (and demo
  deletion, whose cancels are validated the same way) now run inside a
  `_workflow_bypass()` context that stubs the validator at every Frappe
  binding site and restores it afterwards — even on error. Live user
  actions are unaffected: the bypass exists only for the duration of the
  demo calls.

## [1.7.0] — 2026-09-09
### Added — demo without the terminal
- **Load Demo Data from the UI**: the Engineering Dashboard now shows a
  setup banner when the site has no projects (System Manager only) with
  "Load Demo Data" and "Create Customer Test User" buttons; the same actions
  (plus "Delete Demo Data") live in the dashboard menu. Confirmation dialogs
  and progress freeze included; the bench command still works.
- **Customer test user**: one click creates/refreshes
  customer.demo@neoengineering.test with the engineering + standard-module
  roles needed for the walkthrough, generates a password, and shows the
  credentials once with a reminder to disable the user after evaluation.
- 15 new Arabic entries for all demo-UI strings.

## [1.6.0] — 2026-09-08
### Added — full customer-demo dataset
- Demo generator now covers the **whole process** for a customer walkthrough:
  - Engineering Site Visits on every project.
  - Visible **revision loop** on each design: Rev A submitted → client
    "Revision Required" (with comments) → Rev B issued, A auto-superseded →
    resubmitted → approved. Two Design Submissions per project tell the story.
  - **Certificate history** on the executing project (3 monthly certificates:
    20% → 45% → 65%) so the dashboard's 6-month certified trend draws.
  - A live Site Inspection with an **open High observation** — lights the
    dashboard card and lets you demonstrate BR-010 blocking closure.
  - **Financial leg** on the executing project: demo service Item →
    submitted Purchase Order (Main Contract, linked to the tender) →
    submitted Purchase Invoice linked to the latest certificate, validated
    live by BR-012. Defensive: if the site's accounts aren't set up for
    direct PI creation, the engineering records still complete and guidance
    is logged instead of failing.
  - Cleanup extended: delete_demo_data now removes POs, PIs and the demo Item.

## [1.5.0] — 2026-09-08
### Added
- **Bilingual (Arabic)**: `translations/ar.csv` with 379 entries covering all
  26 DocType names, ~150 field labels, all workflow states and actions,
  select options (disciplines, severities, stages, service types), the
  process map, and the dashboard. Frappe renders Arabic RTL automatically
  (English stays LTR) when the user sets Language = العربية.
- **Engineering Dashboard** (`/app/engineering-dashboard`): 8 clickable
  number cards (active projects, submissions with client, pending reviews,
  licenses, tenders, open observations, certified this month, warranty),
  three charts (projects by stage, documents by status, 6-month certified
  trend) and a recent-projects table with Docs%/Site% — one API round-trip,
  role-guarded, fully translatable. Workspace shortcut added.
- **Demo data generator** (`setup/demo.py`): bilingual masters (project
  types, UOMs, 2 customers, 3 prequalified contractors) and four projects
  frozen at Design / Tendering / Execution / Closed, each with the full
  record chain built to satisfy BR-001…BR-016. Explicit commands only:
  `bench --site <site> execute neo_engineering.setup.demo.make_demo_data`
  and `...demo.delete_demo_data`. Never runs automatically.

## [1.4.0] — 2026-09-07
### Changed
- Process Map redesigned to match the office's classic flow chart: lane
  headers with department icons, filled lane-tinted step boxes with inline
  numbering, decision diamonds with Yes/No exits, revision note boxes
  ("Discuss Revisions / Alternatives", "Revise Design", "Send Back for
  Corrections") wired into the loops, chart title header, and a clickable
  "Key Outputs at Each Stage" strip (every output opens its record list).
  All transaction chips, BR tooltips, and the post-completion warranty path
  retained; strings wrapped for translation.

## [1.3.1] — 2026-09-06
### Added
- Process Map: hover (and keyboard-focus) tooltips on every BR-0xx reference,
  spelling out the full business rule in plain language.

## [1.3.0] — 2026-09-05
### Added
- Interactive **Engineering Process Map** desk page: five-department swimlane
  flow chart (Client/BD, Design, Technical, Tendering/Supervision, PM &
  Close-out) with 16 numbered steps, decision diamonds with Yes/No loops,
  parallel licensing path, and auto-drawn arrows. Every step carries direct
  links to open the transaction list or create a new record.
- Workspace now opens with a "Process Map (start here)" shortcut and hint.

## [1.2.0] — 2026-08-30
### Changed
- BOQ Items: "Item / Group" is now a Link to the standard Item master with
  auto-fetch of description, UOM (stock UOM) and rate (standard rate).
  The link is optional — free-text BOQ lines remain valid.
- Project Type on Project Brief and Lead now links to the standard
  Project Type master instead of free text.
- Removed "ERPNext" from all user-visible text (Settings descriptions,
  workspace legend, app description). Functional dependency declarations
  are unchanged.

## [1.1.0] — 2026-08-30
### Changed
- Workspace rebuilt as a numbered nine-stage process pathway with
  color-coded shortcuts, "⚠ Requires" dependency callouts (BR references)
  and "➜ Then" flow pointers per stage.
### Fixed
- Added `[tool.bench.frappe-dependencies]` to pyproject.toml
  (frappe / erpnext >=15,<16) — required by newer bench versions;
  installation previously failed its compatibility check.

## [1.0.1] — 2026-08-30
### Changed
- Rebranded app from Alwathaeq Engineering to NeoEngineering
  (package `neo_engineering`); removed all remaining company references.
  Custom fieldnames on standard DocTypes are unchanged.

## [1.0.0] — 2026-08-25
### Added
- Initial release per Technical Development Specification v1.0:
  13 submittable DocTypes + 13 child tables, Engineering Management
  Settings, ~60 custom fields on 11 standard DocTypes, 11 role-bound
  workflows, 14 roles, business rules BR-001…BR-016 enforced server-side,
  daily notification scheduler, Engineering Management workspace,
  idempotent install/migrate.
