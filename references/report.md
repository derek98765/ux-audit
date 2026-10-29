# Report mode — interactive HTML report from an audit JSON

Read after `ux-audit/SKILL.md`, only when the user asks for a report (or passes an audit JSON path). Don't load this for a plain audit.

Generate a polished, interactive HTML report from a ux-audit JSON file (the output of audit mode). The report is self-contained (two external font `<link>` tags are the only allowed external deps) and saved alongside the source JSON.

The canonical visual reference is `references/report-template.html` in this skill's directory (read the whole file before generating). **Every report must match that template exactly** — same CSS custom properties, class names, HTML structure, and JS pattern.

## Input

Accept the JSON file in two ways:
1. **Path provided**: the user or a preceding ux-audit run specifies the file path directly — use it.
2. **No path provided**: look in the `outputs/` folder of this skill's directory for the most recently modified `ux-audit-*.json` file and use that. Files follow the naming convention `ux-audit-[project]-[scope]-[YYYY-MM-DD-HHmm].json` (the `HHmm` suffix is the local 24-hour time the audit was run).

Read and parse the JSON before generating anything. The expected shape is:

```json
{
  "audit": { "project", "scope", "date", "summary" },
  "findings": [{ "id", "title", "description", "location", "severity", "classification", "solution", "effort", "personas_affected" }],
  "positives": [{ "id", "title", "classification", "description" }],
  "personas": [{ "name", "role", "goal_status", "body", "blockers" }],
  "requirements": [{ "requirement", "status", "notes" }]
}
```

`personas` and `requirements` are **optional**. See conditional rendering rules below.

### Field details

- `severity`: `"p0"` | `"p1"` | `"p2"` | `"p3"`
- `classification`: `"ux"` | `"ui"` | `"product"` | `"content"` | `"dev"` (maps to cat-badge class — see Category badges below)
- `effort`: `"low"` | `"low-med"` | `"med"` | `"high"`
- `personas[].goal_status`: `"Blocked"` | `"Partial"` | `"Unblocked"`
- `requirements[].status`: `"Met"` | `"Partial"` | `"Not Met"`

## Output

Save `ux-audit-report-[project]-[scope]-[YYYY-MM-DD].html` to the `reports/` folder inside this skill's directory. Create the folder if it doesn't exist.

After saving, tell the user the file path and that they can open it in a browser.

## Template structure

All reports use the two-column shell layout from `references/report-template.html`. Do not deviate.

### External dependencies (only two allowed)

Load these in `<head>` — no other external resources:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,500&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

All CSS goes in an inline `<style>` block in `<head>`. All JS is a single inline `<script>` block before `</body>`. No CDN scripts.

### Design tokens (copy verbatim from references/report-template.html)

Use the exact `:root` variables from `references/report-template.html`:
- **Ink scale**: `--ink-900` → `--ink-25`, plus `--paper` and `--rule`
- **Severity colors**: `--sev-p0-bg/fg/mid`, `--sev-p1-bg/fg/mid`, `--sev-p2-bg/fg/mid`, `--sev-p3-bg/fg/mid`
- **Status colors**: `--green-fg/bg`, `--amber-fg`, `--red-fg`
- **Category badge colors**: `--cat-ux-bg/fg`, `--cat-prod-bg/fg`, `--cat-brand-bg/fg`, `--cat-cont-bg/fg`
- **Font variables**: `--font-display: 'Source Serif 4'`, `--font-ui: 'Barlow'`
- **Space scale**: `--space-1` through `--space-16`

### Layout

```
.shell  →  grid: 220px sidebar  |  1fr main
           max-width: 1260px, centered
```

- **Sidebar** (`.sidebar`): sticky, 100vh, scrollable, border-right, contains logo/org label, divider, nav buttons, and meta at the bottom
- **Main** (`.main`): padded content area, starts with `.masthead` then tab panels

### Sidebar

The sidebar contains:
1. **Logo block** (`.sidebar-logo`): org label (e.g. "UX Research Division") and report type + year
2. **Divider** (`.sidebar-divider`)
3. **Nav** (`.sidebar-nav`): section label "Sections" + one `.nav-btn` per visible tab, each with optional `.nav-count` badge showing item count
4. **Meta** (`.sidebar-meta`): at bottom — Product (from `audit.project`), Date (from `audit.date`), Phase/scope (from `audit.scope`)

**Navigation buttons show only tabs that have data.** Specifically:
- Always show: Overview, Issues, Positives
- Show "Persona Impact" only if `personas` array is present and non-empty
- Omit the nav button entirely if the corresponding tab has no data
- **There is no separate Recommendations tab.** Each finding's solution lives inside its own issue card as a "Recommended Solution" callout (see Tab 03).

The active tab's button gets the `.active` class. Each `nav-btn` calls `showTab('id')` where id is one of: `overview`, `personas`, `issues`, `positives`.

### Masthead

Inside `.main`, before the tab panels:

```html
<div class="masthead">
  <div class="masthead-eyebrow">UX / UI Audit Report</div>
  <h1><em>[Product Name]</em> — [Scope description]</h1>
  <div class="masthead-meta-grid">
    <!-- 3-4 .masthead-meta-item blocks with .meta-label + .meta-value -->
    <!-- Include: Audit Mode, Product Phase, Goal, and optionally Personas Audited -->
  </div>
</div>
```

The `<h1>` uses italic serif: `<em>` wraps the product name (normal weight), dash separates it from the scope. The `<h1>` itself is `font-style: italic`.

### Tab panels

Each tab is a `div.tab-panel` with `id="tab-[name]"`. Only the active panel has `.active`. On page load, `tab-overview` is active.

```html
<div id="tab-overview"  class="tab-panel active"> … </div>
<div id="tab-personas"  class="tab-panel"> … </div>  <!-- omit if no personas -->
<div id="tab-issues"    class="tab-panel"> … </div>
<div id="tab-positives" class="tab-panel"> … </div>
```

Each panel's content is wrapped in one or more `.report-section` divs, each starting with a `.section-header` containing `.section-number` (two-digit, e.g. "01") and `.section-title` (uppercase label).

---

## Tab content specifications

### Tab 01 — Overview

**The `.score-strip` comes FIRST — above the Executive Summary section**, as a direct child of `#tab-overview` (not inside the `.report-section`). The Executive Summary section follows it.

```html
<div id="tab-overview" class="tab-panel active">

  <div class="score-strip">
    <!-- 1 or 2 .score-block divs — see below -->
  </div>

  <section class="report-section">
    <div class="section-header">
      <span class="section-number">01</span>
      <span class="section-title">Executive Summary</span>
    </div>
    <p class="exec-summary"> … audit.summary … </p>
  </section>
</div>
```

The `.score-strip` uses `grid-template-columns: 1fr 1fr` when both blocks are present, or `grid-template-columns: 1fr` when only the severity block is present (no requirements data).

**Score block A — Requirements bar** (only if `requirements` data exists):
```html
<div class="score-block">
  <div class="score-block-label">Requirements Coverage — N audited</div>
  <div class="req-bar-wrap">
    <div class="req-bar-seg req-bar-met"     style="width:XX%">N</div>
    <div class="req-bar-seg req-bar-partial" style="width:XX%">N</div>
    <div class="req-bar-seg req-bar-notmet"  style="width:XX%">N</div>
  </div>
  <div class="req-legend"> … </div>
</div>
```
Omit this block entirely if `requirements` is absent or empty.

**Score block B — Issue counts by severity** (always present):
```html
<div class="score-block">
  <div class="score-block-label">Issue Counts by Severity</div>
  <div class="sev-row">
    <div class="sev-cell sev-p0"><div class="sev-num">N</div><div class="sev-label">P0 Critical</div></div>
    <div class="sev-cell sev-p1"><div class="sev-num">N</div><div class="sev-label">P1 High</div></div>
    <div class="sev-cell sev-p2"><div class="sev-num">N</div><div class="sev-label">P2 Medium</div></div>
    <div class="sev-cell sev-p3"><div class="sev-num">N</div><div class="sev-label">P3 Low</div></div>
  </div>
</div>
```

**Section 02: Requirements Coverage** (only if `requirements` data exists):
A `.req-table` with columns: Requirement / Status / Assessment Notes. Status cells use `.status-met`, `.status-partial`, or `.status-notmet` classes. Omit this entire section if no requirements data.

---

### Tab 02 — Personas (omit entirely if no personas)

**Section 03: Persona Impact Analysis**

For each persona, render a `.persona-card`:
```html
<div class="persona-card">
  <div class="persona-card-header">
    <div>
      <div class="persona-name">Name</div>
      <div class="persona-role">Role description</div>
    </div>
    <span class="goal-badge goal-[yes|partial|no]">Unblocked|Partial|Blocked</span>
  </div>
  <p class="persona-body">body text</p>
  <ul class="blocker-list">
    <li>Blocker item</li>
  </ul>
</div>
```

`goal_status` → badge class mapping:
- `"Unblocked"` → `goal-yes`
- `"Partial"` → `goal-partial`
- `"Blocked"` → `goal-no`

---

### Tab 03 — Issues

**Section 04: Identified Issues**

Group findings by severity in descending order (P0 → P1 → P2 → P3). Only render a severity group if it has at least one finding.

```html
<div class="issue-section">
  <div class="issue-section-heading">P0 · Critical</div>
  <div class="issue-list">
    <div class="issue-card issue-p0"> … </div>
  </div>
</div>
```

**Each issue card is an expandable accordion.** Clicking the `.issue-card-head` toggles the `.open` class on the parent `.issue-card`, which expands `.issue-body-wrap` (collapsed by default via `max-height: 0; overflow: hidden`). The chevron rotates 180° when open. **The recommendation lives inside the card** as a "Recommended Solution" callout — there is no separate Recommendations tab.

Each `.issue-card` structure:
```html
<div class="issue-card issue-p[0-3]">
  <div class="issue-card-head">
    <div class="issue-severity-stripe">
      <span class="sev-pill sev-pill-p[0-3]">P0</span>
    </div>
    <div class="issue-head-content">
      <div class="issue-title-row">
        <span class="issue-title">Title</span>
        <span class="cat-badge cat-[ux|product|branding|content]">UX</span>
      </div>
      <div class="issue-meta-row">
        <span class="issue-meta-item"><strong>Location:</strong> …</span>
        <span class="issue-meta-item"><strong>Affects:</strong> …</span>
      </div>
    </div>
    <div class="issue-chev"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></div>
  </div>
  <div class="issue-body-wrap"><div class="issue-body">
    <p class="issue-body-text">Description paragraph</p>
    <div class="resolution-box">
      <div class="fix-label">Recommended Solution</div>
      <p class="issue-body-text">Solution text (from finding.solution)</p>
    </div>
  </div></div>
</div>
```

Key structural points:
- `.issue-card-head` is a **3-column grid** (`36px 1fr 36px`): severity stripe, content, chevron.
- The body is double-wrapped: `.issue-body-wrap` (the collapsing container) wraps `.issue-body` (the padded content). Close both at the end: `</div></div>`.
- The solution is wrapped in a `.resolution-box` (light green callout) with a `.fix-label` reading **"Recommended Solution"**.

The `.issue-severity-stripe` background color comes from the parent card class (`.issue-p0` through `.issue-p3`), controlled by CSS. The `sev-pill` class controls the colored text pill.

**"Affects" field**: use `personas_affected` array joined with ", " or "All users" if empty.

---

### Tab 04 — Positives

**Section 05: Positive Findings**

```html
<div class="positive-list">
  <div class="positive-card">
    <div class="positive-title">Title</div>
    <p class="positive-body">Description</p>
  </div>
</div>
```

---

### Recommendations — no separate tab

Recommendations are **not** a standalone tab. Each finding's `solution` is rendered inside that finding's issue card, in a `.resolution-box` callout labeled "Recommended Solution" (see Tab 03). Do not generate a `tab-recommendations` panel, a `.rec-list`, or `.rec-row` markup. The `.effort-indicator` CSS remains in the template but is unused in the current layout.

---

## Category badge class mapping

| classification value | cat-badge class |
|---|---|
| `"ux"` or `"ui"` | `cat-ux` |
| `"product"` | `cat-product` |
| `"branding"` or `"brand"` | `cat-branding` |
| `"content"` or `"dev"` | `cat-content` |

Badge label text: capitalize the classification (e.g. `"ux"` → "UX", `"product"` → "Product").

---

## JavaScript

Two pieces of JS only — `showTab()` for tab switching and a delegated click handler that toggles issue-card accordions. Place both inline before `</body>`:

```html
<script>
  function showTab(id) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + id).classList.add('active');
    document.querySelector('[onclick="showTab(\'' + id + '\')"]').classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Expandable accordion for issue cards
  document.querySelectorAll('.issue-card-head').forEach(function (head) {
    head.addEventListener('click', function () {
      head.closest('.issue-card').classList.toggle('open');
    });
  });
</script>
```

No other JS. No `alert()`, `console.log()`, or debug output. No data embedded in JS arrays. All content is static HTML. Issue cards start collapsed; the print stylesheet force-expands them (`.issue-body-wrap { max-height: none !important }`) and hides the chevrons.

---

## Responsive & print

Copy the `@media (max-width: 860px)` and `@media print` blocks exactly from `references/report-template.html`.

At ≤860px: sidebar collapses to a horizontal flex nav bar; logo, meta, and divider are hidden; nav items wrap in a row.

For print: sidebar hidden, all panels shown (`display: block !important`); accordions force-expanded and chevrons hidden.

---

## Sidebar count badges

Each `.nav-btn` that has countable items should include a `.nav-count` span:
- **Issues**: total count of all findings
- **Positives**: total count of positives
- **Persona Impact**: count of persona cards (omit entirely if no personas)
- **Overview**: no count badge

---

## Code constraints

- All styles in one `<style>` block in `<head>`
- Only `<link>` tags for Google Fonts allowed as external deps
- No CDN scripts, no external JS
- No `alert()`, `console.log()`, or debug output
- Must render correctly in Chrome and Safari at `file://` protocol
- Print-safe: all panels display in print mode
