# Insourcing Prioritization Streamlit Prototype

This is a working Streamlit prototype for evaluating and tracking part/product insourcing decisions.

## Purpose

The app supports a cross-functional insourcing review process across:

- Manufacturing Engineering
- Operations
- Quality
- Supply Chain
- Finance
- Engineering / R&D
- Leadership

It is designed to prioritize parts based on:

- Financial impact / COGS reduction
- Strategic capability growth
- Lead time and supply control
- Quality control / process ownership
- Operational feasibility
- Capacity fit / spindle utilization
- Future product leverage
- Risk modifier

## Included Pages

- Dashboard
- Candidate Intake
- Scoring Matrix
- Decision Log
- Roadmap
- Capability Map
- Settings & Export

## How to Run Locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

## Notes

This prototype uses Streamlit session state, so data persists only during the active browser session.

For a production version, replace session state with a persistent database such as:

- SQLite
- PostgreSQL
- SharePoint List / Dataverse through API integration
- Snowflake / SQL Server
- Acumatica API integration for ERP data

## Suggested Next Development Steps

1. Add user authentication.
2. Add persistent database storage.
3. Add role-based edit permissions.
4. Add attachment support for drawings, quotes, validations, and ROI files.
5. Add approval workflow notifications.
6. Connect supplier spend, lead time, and quality data to ERP/QMS sources.
