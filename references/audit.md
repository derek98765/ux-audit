# Audit mode — UX/UI audit to a JSON report

Read after `ux-audit/SKILL.md`. Produces the findings JSON only; the HTML report is a separate mode (`references/report.md`) loaded only when the user asks for it.

Audit work as peer review, not as a simulated user. For problems: name them precisely, explain why they fail, label them with severity and classification, and give proposed solutions. For positives: note what works well, why it succeeds, and label it with a classification — no severity or solution needed.

## Setup

**Parse from invocation**: project name (required) + scope — a page, flow, or feature area (ask if missing).

**Load background references**: the `references/` folder inside this skill's directory contains one subfolder per project. Using the project name from the invocation, open `references/<project-name>/` and read every file inside it — these files (e.g. `project-overview.md`, `user-archetype.md`) contain domain background information. Do not read reference folders for other projects. If `references/<project-name>/` doesn't exist or is empty, ask the user for the background inline (product description, target users, key flows, design principles).

**Identify what to audit**: the scope points to real code in this project — find and read the relevant pages, components, and flows in the codebase, which is the primary source of truth. If the scope is ambiguous, ask which files or routes it maps to. The scope may also be an external URL (a deployed site with no local code) — in that case the rendered page is the primary source of truth, so capturing screens (below) is required, not optional.

**Capture screens**: the audit must reason over what the user actually sees, not just the code. Screens should cover both **1440px laptop** and **390px mobile** viewports. There are two ways to get them:

- **User-provided screenshots**: the user may attach screenshots directly in the conversation. Read every image provided before auditing.
- **Browser via Claude**: if the user asks you to open a URL, use the Claude browser tool to navigate to it and capture the page at both viewport widths.

Read all provided screens before auditing. If no screens are provided and no URL is given, ask the user to supply them.

## Audit

Evaluate for both problems and strengths. The checklists under each classification are a reference, not an exhaustive boundary — flag any issue you find that harms the user experience, even if it isn't listed. For problems, only flag what's actually broken, harmful, or violates usability best practices — not subjective style opinions. This includes visual issues with objective consequences: insufficient color contrast, text too small to read, touch targets too small to tap reliably. Do not flag things like color palette choices, illustration style, or visual polish that have no functional impact. For positives, note what works well and should be preserved. Calibrate every severity call against the personas and goals from the reference files.

**Severity scale (applies to all classifications)**:
- **p0**: blocks the user from completing their core goal entirely — broken flow, data loss, unrecoverable state, silent failure
- **p1**: significantly degrades the experience and will likely cause abandonment or major confusion — missing feedback, misleading actions, layout broken at a key breakpoint
- **p2**: creates friction or inconsistency but a workaround exists — extra steps, awkward copy, token misuse, minor layout issues at non-primary breakpoints
- **p3**: polish-level — no functional impact, user can complete their goal without noticing

---

### UX — Flow, Structure & Behavior

**What to review**: trace through every user-facing flow in scope. Follow the primary path a target persona would take, then the alternate and error paths. Read the routing logic, state transitions, and conditional rendering to understand what actually happens — not just what the happy path shows.

*Task flow & navigation*
- Can the user complete their primary goal without confusion or dead ends?
- Are steps sequenced in the order the user naturally needs them — no premature asks, no missing prerequisites?
- Is the number of steps proportionate to the task complexity — no unnecessary friction added by the product?
- Does the flow match the user's mental model of how this task works in the real world, or does it force them to learn a new model?
- Are navigation labels self-explanatory without needing to click to find out — does the label match the destination?
- Can the user always tell where they are, where they came from, and how to go back or undo?
- Are exit points (cancel, back, close) always available — users should never feel trapped in a flow?
- Does the interface follow established conventions for this type of product so users can apply prior knowledge (Jakob's law)?

*Information architecture & cognitive load*
- Does the IA group related things together and separate unrelated things clearly — does the structure reflect how users think, not how the system is built?
- Is complexity revealed progressively — advanced options, edge cases, and secondary actions surfaced only when needed?
- Are the number of choices on any one screen minimised — too many options increases decision time and abandonment (Hick's law)?
- Is each screen focused on one primary task or decision, with supporting content clearly subordinate?
- Are sensible defaults provided so users can proceed without configuring everything from scratch?
- Is the most common or recommended path the path of least resistance — does the design guide users toward the right action without forcing it?
- Is content chunked into digestible pieces — long forms, settings, or information broken into logical sections rather than presented as a wall?

*Feedback & error handling*
- Does the user know what will happen before they take an action — are consequences stated upfront, not revealed after?
- After every action, does the system immediately confirm what happened (success, processing, failure) — no silent operations?
- Is feedback proportionate — minor actions get subtle confirmation, significant actions get clear acknowledgement?
- When something goes wrong, does the error explain what happened in plain language and offer a specific next step — not just a generic failure message?
- Are error messages placed at the point of failure, not at the top of the page?
- Are empty states meaningful — do they explain why it's empty, set expectations, and suggest what to do next?
- Are destructive or irreversible actions (delete, disconnect, submit payment) guarded with a confirmation step that clearly states the consequence?
- Can users undo or recover from mistakes wherever possible — the cost of accidental actions should be low?

---

### UI — Visual Communication, Affordance & Responsiveness

**What to review**: evaluate the visual layer only where it affects whether a user can understand and act. Check that the implementation uses the project's design system correctly and that the UI holds at both target breakpoints (1440px laptop, 390px mobile). Flag issues only when they cause a user to misread hierarchy, miss an action, take the wrong path, or encounter a broken layout.

**What to check**:

*Visual hierarchy & affordance*
- Is the primary action on each screen visually dominant? Would a user immediately know what to do?
- Do interactive elements (buttons, links, inputs) look interactive? Do non-interactive elements look static?
- Is visual hierarchy consistent with information hierarchy — does the most important thing look most important?
- Is contrast sufficient for body text, labels, and interactive elements to be readable?
- Are loading, disabled, and active states visually distinguishable?
- Are primary CTAs visible above the fold without scrolling? In long modals or sheets, is the CTA sticky so it remains accessible as the user scrolls through the content?

*Design system consistency*
- Are spacing, typography, and color values using design tokens — not hardcoded values?
- Are shadcn components used where they exist, rather than custom-built equivalents?
- Are component variants and props used correctly and consistently across equivalent elements?

*Responsiveness*
- Check at two breakpoints: **laptop (1440px)** and **mobile (390px)** — the screens captured in Setup.
- Do multi-column layouts reshape correctly from laptop to mobile (e.g. multi-column → single column), not collapse or overflow?
- Are touch targets at least 44×44px on mobile?
- Do padding, gaps, and font sizes reduce from laptop to mobile — not stay fixed at desktop sizes?
- Does content stay within the viewport — no horizontal overflow, no text or elements clipped?
- Do wide tables, sticky panels, or side rails reshape appropriately on mobile?

---

### Product — Strategy, Scope & Mechanism

**What to review**: issues in this category cannot be fixed directly in design or code — they require a product decision. Flag things where the underlying feature, mechanism, or business constraint is what's causing the UX problem. Examples: a feature that's missing entirely, how authentication works (supported login methods), pricing structure that creates friction, a core flow that works as built but is the wrong thing to build.

**What to check**:
- Are there core user goals that can't be achieved because the feature doesn't exist or is out of scope?
- Does the current mechanism (auth method, payment flow, data model, pricing tier) create unavoidable friction for the target persona?
- Is the product asking users to do something that should be handled by the system?
- Are there supported/unsupported capabilities (e.g. no SSO, no guest checkout) that block a persona's primary use case?
- Does the feature as designed serve the product's needs at a meaningful cost to the user experience?

---

### Content — Messaging & Communication

**What to review**: read every user-facing string in scope — headings, CTAs, labels, body copy, taglines, error messages, empty states, tooltips, confirmation dialogs, onboarding text. Evaluate whether the messaging is clear, value-driven, and consistent in voice.

**What to check**:

*Clarity & simplicity*
- Is the message as short as it can be without losing meaning?
- Is it written in plain language the target persona would naturally use — no jargon, no internal system terms?
- Does each sentence do one job? Are there compound messages that should be split?
- Do CTAs name the outcome, not the mechanics? ("Start free trial" not "Submit", "Save and continue" not "Next")

*Value & purpose*
- Do headlines and key messages articulate why this matters to the user — not just what it is?
- Does onboarding and marketing copy lead with user benefit, not feature description?
- Are empty states and zero-data screens framed as opportunities, not dead ends?

*Consistency & tone*
- Is tone consistent across the flow — no unexpected shifts between formal and casual, technical and plain?
- Do similar actions use the same language throughout (e.g. "delete" in one place and "remove" in another for the same action)?
- Does the voice feel like it belongs to one product, or does it feel assembled from different sources?

---

### Dev — Logic, State Coverage & Bugs

**What to review**: read the component and logic code to identify gaps between what the UI promises and what the implementation actually handles. This is not a code quality review — focus on correctness from the user's perspective: does the code produce the right behavior, cover the right states, and handle the edge cases a real user will hit?

**What to check**:

*State coverage*
- Are all meaningful UI states implemented: loading, empty, error, disabled, success, partial/stale?
- Do loading states appear immediately on action trigger, not after a delay?

*Logic & correctness*
- Does the logic handle edge cases: zero items, maximum limits, special characters, very long strings?
- Are calculations, filters, or sorting operations correct at boundary values?
- Are conditional renders based on the right conditions — could a user see UI intended for a different role, state, or context?
- Are mutations (create, update, delete) guarded against double-submission or accidental repeat triggers?

## Output

Save `ux-audit-[project]-[scope]-[YYYY-MM-DD-HHmm].json` to the `outputs/` folder inside this skill's directory. Create the folder if it doesn't exist. The `HHmm` suffix is the local 24-hour time the audit was run (e.g. `2026-06-23-1430`), so multiple audits of the same scope on the same day don't collide.

```json
{
  "audit": {
    "project": "",
    "scope": "",
    "date": "YYYY-MM-DD HH:mm",
    "summary": "One paragraph: overall UX health and the dominant theme."
  },
  "findings": [{
    "id": "F-001",
    "title": "",
    "description": "What the problem is and why it fails the user.",
    "location": "e.g. Onboarding step 2 — email input",
    "severity": "p0 | p1 | p2 | p3",
    "classification": "ux | ui | product | content | dev",
    "solution": "Specific, handoff-ready fix.",
    "effort": "low | medium | high",
    "personas_affected": [""]
  }],
  "positives": [{
    "id": "P-001",
    "title": "",
    "classification": "ux | ui | product | content | dev",
    "description": "What works and why it should be preserved."
  }]
}
```

**Severity**: p0 = blocks core goal · p1 = likely abandonment · p2 = friction with workaround · p3 = polish  
**Effort**: low = hours · medium = 1–2 days · high = 3+ days

After saving, print a one-paragraph summary with the issue count breakdown and top P0/P1 findings. Do not echo the full JSON. Then offer the HTML report in one line ("say 'generate the report' for an interactive HTML version") — don't generate it unless asked.
