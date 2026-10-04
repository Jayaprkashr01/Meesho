# Part 4 — Agentic Workflow Specification

## 4.1 Agent Specification

### Goal

Keep Meesho category managers informed of categories whose month-on-month revenue moves beyond the 8% threshold, while requiring human approval before any message is considered sent.

### Tools

The monitoring agent uses the following functions:

- `validate_feed()` from Part 2
- `mom_growth()` from Part 2
- `is_flagged()` from Part 2
- Part 3 prompt-pack template logic for drafting stakeholder messages

The Part 2 growth functions are imported and reused without modification.

### Memory / State

The agent remembers or receives the previous month's revenue for every category. This allows the agent to calculate month-on-month growth when the next month's feed is processed.

### Planner

The agent follows these ordered subtasks:

1. Load the previous-month and current-month revenue feeds and validate the current feed.
2. If validation fails, stop immediately and report all validation errors.
3. If validation succeeds, calculate MoM growth for every category.
4. Run `is_flagged()` for every category.
5. Sort flagged categories by absolute MoM percentage in descending order.
6. Draft messages for at most the top 3 flagged categories.
7. Mark remaining flagged categories as `suppressed, review manually`.
7b. Record exact-boundary categories in `escalated_categories` without drafting messages.
8. Emit one structured JSON object for the run.

### Feedback Loop

Every drafted message is held for human approval.

The agent never automatically sends an email or external message.

The runner therefore reports:

`drafted_and_held_for_approval`

instead of actually sending the message.

---

## Guardrails

### Input Guardrail

`validate_feed()` must pass before any MoM calculation or drafting takes place.

If validation returns `False`, the run immediately becomes a Hard Stop.

### Action Guardrail

No message is ever automatically sent.

Messages are only drafted and held for human approval.

### Output Guardrail

Every number in a drafted message must trace directly to a Part 1 or Part 2 value.

The agent must not invent revenue, growth percentages, order counts, or other numerical values.

---

## Success Condition

A run is successful when:

- The feed is valid.
- MoM calculations complete successfully.
- Flagged categories are correctly identified.
- At most three messages are drafted.
- Remaining flagged categories are suppressed.
- Exact-boundary categories are escalated.
- Every numerical value in the draft is traceable to verified project data.

If no category crosses the threshold, the run can correctly produce zero drafts.

## Error Condition

If `validate_feed()` returns `False`, the agent performs a Hard Stop.

The validation errors are surfaced in the output.

No MoM calculation or message drafting is attempted.

---

# 4.2 Given-When-Then Agent Specifications

## Specification 1

**GIVEN** April to May Ethnic Wear revenue changes from `104520.77` to `185107.61`

**WHEN** the agent calculates MoM growth and evaluates the threshold

**THEN** MoM growth must be `77.1` and the category must be `"flagged"`.

---

## Specification 2

**GIVEN** May to June Beauty & Personal Care revenue changes from `35542.11` to `37559.07`

**WHEN** the agent evaluates the category

**THEN** MoM growth must be `5.67` and the result must be `"not_flagged"`.

---

## Specification 3

**GIVEN** previous revenue is `100000` and current revenue is `108000`

**WHEN** the agent evaluates the exact threshold boundary

**THEN** MoM growth must be exactly `8.0` and the result must be `"escalate_exact_boundary"`.

---

## Specification 4

**GIVEN** the corrupted feed contains one negative revenue, one missing category and one missing revenue

**WHEN** the agent validates the feed

**THEN** validation must fail with exactly these three errors:

1. `line 3: negative revenue (-4200.0) for category=Western Wear`
2. `line 4: missing category (month=July)`
3. `line 6: missing revenue (category=Home & Kitchen)`

No MoM calculation or drafting is allowed after this Hard Stop.

---

# 4.3 Structured JSON Output

Every run produces one JSON object with these top-level fields:

- `run_month`
- `validation_status`
- `validation_errors`
- `flagged_categories`
- `suppressed_categories`
- `escalated_categories`
- `action_taken`

Each flagged category contains:

- `category`
- `mom_pct`
- `previous_revenue`
- `current_revenue`
- `drafted`
- `message` when drafted

Possible action values:

- `drafted_and_held_for_approval`
- `hard_stop`

---

# 4.4 Mock Agent Runner

The mock runner exposes:

`run(month, previous_month_csv, current_month_csv)`

It performs the complete monitoring workflow without network calls, API keys, email or SMTP.

The runner imports the Part 2 growth engine functions without re-implementing them.

Messages are drafted only and held for human approval.