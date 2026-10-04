# Meesho Revenue Monitoring & Agentic Workflow

## Project Overview

This project is a complete revenue monitoring and decision-support pipeline built using
SQL, Python, narrative reporting, and a mock agent workflow.

The project starts with raw Meesho-style order and reseller data. The data is first
processed using SQL to calculate verified business metrics. These verified numbers are
then passed to Python for validation and Month-on-Month (MoM) growth detection.

The significant revenue changes are then converted into clear business narratives.
Finally, Part 4 connects all previous parts into a guarded mock monitoring agent that
prioritizes important changes and prepares messages for human approval.

The complete project workflow is:

Raw Data
→ Part 1 SQL Analysis
→ Part 2 Python Validation & Growth Detection
→ Part 3 Narrative & Data Masking
→ Part 4 Agentic Workflow

The main principle of this project is:

**Calculate first → Validate → Analyze → Explain → Draft → Human Approval**
## Project Structure

The project is organized into Data and four main parts.

```text
Meesho/
│
├── Data/
│   ├── dataset.py
│   ├── meesho_reseller.db
│   ├── orders.csv
│   └── resellers.csv
│
├── Part 1 SQL/
│   ├── queries.sql
│   ├── run_queries.py
│   └── output/
│       ├── june_aov.csv
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers.csv
│       └── zero_order_resellers.csv
│
├── part-2 engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
│
├── Part-3 Narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
│
├── Part-4 Agent/
│   ├── agent_spec.md
│   ├── mock_agent_runner.py
│   ├── test_agent.py
│   ├── april.csv
│   ├── may.csv
│   └── june.csv
│
└── README.md

`Ctrl + S`.

---

# STEP 3 — Data Section

இப்போது இதை next-ஆ paste பண்ணுங்க:

```markdown
## Data

The Data folder contains the source data and dataset generation script used by the
project.

The main files are:

- `dataset.py` — prepares the local dataset and database.
- `orders.csv` — contains order-level information.
- `resellers.csv` — contains reseller information.
- `meesho_reseller.db` — local database used by the SQL analysis.

The data contains information required for category revenue, order analysis, regional
revenue, reseller performance, and other business calculations.

No external API or online data source is required for the dataset.
## Regenerating the Dataset

The dataset can be regenerated locally using the Python dataset script.

From the project root directory, run:

```cmd
python "Data\dataset.py"

---

# STEP 5 — Part 1 Section

இப்போது Part 1 explanation:

```markdown
# Part 1 - SQL Business Analysis

Part 1 is responsible for calculating the verified business numbers from the source
data.

The SQL queries are stored in:

```text
Part 1 SQL/queries.sql
Part 1 SQL/run_queries.py

---

# STEP 6 — Part 1 → Part 2 Connection

இந்த section assignment-ன் **workflow mapping** requirement-க்கு முக்கியம்:

```markdown
## Part 1 → Part 2 Connection

Part 1 calculates the real business numbers using SQL before any automated decision is
made.

Part 2 then receives these verified numbers and applies validation and growth-detection
rules.

This follows the workflow pattern:

**Compute real numbers first → Validate and analyze them second.**

This separation prevents later stages from making decisions using unverified or invented
numbers.
