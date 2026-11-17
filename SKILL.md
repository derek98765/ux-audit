---
name: ux-audit
description: Professional UX/UI audit of a page, flow or feature area, producing a structured JSON report of findings (severity, classification, suggested solutions) with screenshots of the affected screens. Also turns an audit JSON into a self-contained, interactive HTML report with screenshots in the issue cards when asked. Use when the user wants a UX/UI audit or peer review of a screen or flow, or says "generate the audit report", "make an HTML report from the audit", or passes an ux-audit JSON file. The report is a separate step — don't produce it unless asked.
version: 3.1.0
user-invocable: true
argument-hint: "<project-name> [page or flow to audit]  |  report [path to audit JSON]"
---

# UX audit

In audit mode, capture screenshots and save them with the findings JSON.
In report mode, use that JSON and its screenshots to build the HTML report when
the user asks for it.

## Pick the mode, then read its file

| The user wants | Mode | Read |
|---|---|---|
| a UX/UI audit or review of a page, flow or feature (a project name plus a scope) | **audit** | `references/audit.md` |
| an HTML report from an audit ("generate the report", "make it an HTML report", or an audit JSON path) | **report** | `references/report.md` |

Read only the file for your mode. In particular, don't load `references/report.md`
or `references/report-template.html` (about 40 KB) during a plain audit. After an
audit, mention the report in one line and stop.

## Where things live

All inside this skill's directory:

- `references/<project-name>/` — background for one project (product overview,
  user archetypes). Audit mode reads only the folder for the project being
  audited. Other files directly under `references/` belong to the skill, not to a
  project.
- `outputs/` — the audit JSON, `ux-audit-[project]-[scope]-[YYYY-MM-DD-HHmm].json`.
- `outputs/<audit-basename>-screenshots/` — screen captures for that JSON. Keep
  this folder next to the JSON so report mode can resolve its paths later.
- `reports/` — the HTML report, `ux-audit-report-[project]-[scope]-[YYYY-MM-DD].html`.

`outputs/` and `reports/` hold project data and are not committed.

## Rules for both modes

- Report what the evidence shows. Never invent a finding, a persona or a
  requirement that isn't in the code, the screens or the audit JSON.
- If the project name, the scope or the JSON path is missing and can't be
  inferred, ask.
- Create `outputs/` or `reports/` if they don't exist.
