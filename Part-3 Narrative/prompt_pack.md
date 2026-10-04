# Reusable Prompt Pack

## Trigger

Run this prompt when a category's `is_flagged` result is exactly `"flagged"`.

## Input list

The prompt requires the following placeholder variables:

- `{category}` — category name
- `{previous_revenue}` — revenue in the previous month
- `{current_revenue}` — revenue in the current month
- `{mom_pct}` — calculated Month-on-Month growth percentage
- `{month}` — current month
- `{prev_month}` — previous month
- `{region}` — region relevant to the stakeholder update, if supplied
- `{alias}` — coded reseller alias, if a reseller is relevant

## Prompt

Write a concise stakeholder update for a regional manager using the
Context → Insight → Implication structure.

Context:
State what `{category}` is being measured and explicitly name the period
`{month}` versus `{prev_month}`. Use only the supplied values.

Insight:
State the supplied Month-on-Month result `{mom_pct}%` as a fact.
Compare `{previous_revenue}` with `{current_revenue}` when useful.
Do not calculate or introduce any additional number that is not supplied.

Implication:
Give one specific and actionable next step for the regional manager.
If you propose a possible cause that is not directly proven by the supplied
data, label it explicitly as a hypothesis.

Rules:
1. Never invent a number, percentage, date, reseller, cause, or business fact.
2. Every number in the narrative must come directly from the supplied
   placeholders.
3. Use the exact category and month names supplied.
4. If a reseller is mentioned, use only `{alias}` and never the raw reseller name.
5. Separate verified facts from hypotheses.
6. Keep the recommendation specific and actionable.

## Checklist

Before using the generated narrative, verify:

- [ ] Every number in the draft exactly matches a supplied placeholder value.
- [ ] The category name and both month names match the supplied inputs.
- [ ] Every data-supported statement is presented as a fact.
- [ ] Every possible cause not proven by the data is explicitly labeled as a hypothesis.
- [ ] The recommendation is specific and actionable rather than vague.
- [ ] Any reseller is referenced only by its coded alias and never by its raw name.
- [ ] No unsupported business claim has been added.