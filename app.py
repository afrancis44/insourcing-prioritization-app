import io
from datetime import date

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Insourcing Prioritization App",
    page_icon="🏭",
    layout="wide",
)


DEFAULT_WEIGHTS = {
    "Financial Impact / COGS Reduction": 20,
    "Strategic Capability Growth": 20,
    "Lead Time & Supply Control": 15,
    "Quality Control / Process Ownership": 15,
    "Operational Feasibility": 15,
    "Capacity Fit / Spindle Utilization": 10,
    "Future Product Leverage": 5,
}

RISK_MODIFIERS = {
    "Low": 0,
    "Moderate": -3,
    "High": -7,
    "Very High": -12,
}

DECISION_STATUSES = [
    "Not Started",
    "Under Review",
    "Approved",
    "Conditionally Approved",
    "Deferred",
    "Rejected",
]

PORTFOLIO_BUCKETS = [
    "Quick Win",
    "Spindle Time Filler",
    "Strategic Capability Builder",
    "Supplier Control Candidate",
    "Future Platform Enabler",
    "Defer",
]

ROADMAP_HORIZONS = [
    "0-12 Months",
    "12-24 Months",
    "24-36 Months",
    "Defer",
]

REQUIRED_ENABLERS = [
    "Existing Machine Capacity",
    "Swiss Lathe",
    "Laser Welding System",
    "5-Axis Machine",
    "Automated Part Handling",
    "Inspection / Metrology",
    "Fixture / Tooling",
    "Process Validation",
    "Supplier Transition Plan",
]

FUNCTIONAL_AREAS = [
    "Manufacturing Engineering",
    "Operations",
    "Quality",
    "Supply Chain",
    "Finance",
    "Engineering / R&D",
    "Leadership",
]


def load_sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Part Number": "PN-1001",
                "Description": "Existing CNC machined bracket",
                "Product Family": "Current Product A",
                "Current Supplier": "Supplier A",
                "Annual Usage": 3500,
                "Current Purchase Price": 48.00,
                "Estimated Internal Unit Cost": 31.00,
                "Target Process": "3-Axis Mill",
                "Required Machine": "Existing CNC Mill",
                "Supplier Lead Time Weeks": 6,
                "Quality History": "Stable",
                "Financial Score": 4,
                "Capability Growth Score": 2,
                "Lead Time Control Score": 3,
                "Quality Control Score": 3,
                "Feasibility Score": 5,
                "Capacity Fit Score": 5,
                "Future Product Score": 2,
                "Risk Level": "Low",
                "Decision Status": "Approved",
                "Portfolio Bucket": "Quick Win",
                "Roadmap Horizon": "0-12 Months",
                "Required Enabler": "Existing Machine Capacity",
                "Owner": "Manufacturing Engineering",
                "Next Action": "Complete fixture review and pilot lot plan",
                "Target Start": "2026-07-01",
                "Target Completion": "2026-10-31",
                "Swiss": False,
                "Laser Welding": False,
                "5-Axis": False,
                "Automated Handling": False,
                "Inspection / Metrology": True,
                "Fixturing": True,
                "Validation": False,
                "DFM Knowledge": True,
            },
            {
                "Part Number": "PN-2104",
                "Description": "Precision turned shaft",
                "Product Family": "Future Product B",
                "Current Supplier": "Supplier B",
                "Annual Usage": 9000,
                "Current Purchase Price": 22.50,
                "Estimated Internal Unit Cost": 15.25,
                "Target Process": "Swiss Lathe",
                "Required Machine": "Swiss Lathe",
                "Supplier Lead Time Weeks": 10,
                "Quality History": "Moderate Issues",
                "Financial Score": 3,
                "Capability Growth Score": 5,
                "Lead Time Control Score": 4,
                "Quality Control Score": 4,
                "Feasibility Score": 2,
                "Capacity Fit Score": 3,
                "Future Product Score": 5,
                "Risk Level": "High",
                "Decision Status": "Conditionally Approved",
                "Portfolio Bucket": "Strategic Capability Builder",
                "Roadmap Horizon": "12-24 Months",
                "Required Enabler": "Swiss Lathe",
                "Owner": "Operations",
                "Next Action": "Build Swiss lathe capital justification",
                "Target Start": "2027-01-01",
                "Target Completion": "2027-09-30",
                "Swiss": True,
                "Laser Welding": False,
                "5-Axis": False,
                "Automated Handling": False,
                "Inspection / Metrology": True,
                "Fixturing": True,
                "Validation": True,
                "DFM Knowledge": True,
            },
            {
                "Part Number": "PN-3308",
                "Description": "Laser welded subassembly",
                "Product Family": "Current Product C",
                "Current Supplier": "Supplier C",
                "Annual Usage": 2200,
                "Current Purchase Price": 145.00,
                "Estimated Internal Unit Cost": 97.00,
                "Target Process": "Laser Welding",
                "Required Machine": "Laser Welding System",
                "Supplier Lead Time Weeks": 14,
                "Quality History": "Recurring Issues",
                "Financial Score": 4,
                "Capability Growth Score": 5,
                "Lead Time Control Score": 5,
                "Quality Control Score": 5,
                "Feasibility Score": 2,
                "Capacity Fit Score": 2,
                "Future Product Score": 5,
                "Risk Level": "High",
                "Decision Status": "Under Review",
                "Portfolio Bucket": "Future Platform Enabler",
                "Roadmap Horizon": "24-36 Months",
                "Required Enabler": "Laser Welding System",
                "Owner": "Quality",
                "Next Action": "Define validation and process development plan",
                "Target Start": "2027-06-01",
                "Target Completion": "2028-03-31",
                "Swiss": False,
                "Laser Welding": True,
                "5-Axis": False,
                "Automated Handling": False,
                "Inspection / Metrology": True,
                "Fixturing": True,
                "Validation": True,
                "DFM Knowledge": True,
            },
        ]
    )


def initialize_state():
    if "weights" not in st.session_state:
        st.session_state.weights = DEFAULT_WEIGHTS.copy()
    if "candidates" not in st.session_state:
        st.session_state.candidates = load_sample_data()
    if "decision_log" not in st.session_state:
        st.session_state.decision_log = pd.DataFrame(
            [
                {
                    "Decision Date": "2026-06-12",
                    "Part Number": "PN-1001",
                    "Decision": "Approved",
                    "Rationale": "Good short-term savings, current-machine fit, and low transition risk.",
                    "Conditions": "Complete pilot lot before full production release.",
                    "Owner": "Manufacturing Engineering",
                    "Due Date": "2026-10-31",
                    "Review Status": "Open",
                },
                {
                    "Decision Date": "2026-06-12",
                    "Part Number": "PN-2104",
                    "Decision": "Conditionally Approved",
                    "Rationale": "Strong Swiss capability builder with future product relevance.",
                    "Conditions": "Requires capital approval and validation plan.",
                    "Owner": "Operations",
                    "Due Date": "2027-03-31",
                    "Review Status": "Open",
                },
            ]
        )


def calculate_scores(df: pd.DataFrame, weights: dict) -> pd.DataFrame:
    df = df.copy()

    score_map = {
        "Financial Score": "Financial Impact / COGS Reduction",
        "Capability Growth Score": "Strategic Capability Growth",
        "Lead Time Control Score": "Lead Time & Supply Control",
        "Quality Control Score": "Quality Control / Process Ownership",
        "Feasibility Score": "Operational Feasibility",
        "Capacity Fit Score": "Capacity Fit / Spindle Utilization",
        "Future Product Score": "Future Product Leverage",
    }

    for score_col in score_map:
        df[score_col] = pd.to_numeric(df[score_col], errors="coerce").fillna(0).clip(0, 5)

    df["Annual Purchased Spend"] = (
        pd.to_numeric(df["Annual Usage"], errors="coerce").fillna(0)
        * pd.to_numeric(df["Current Purchase Price"], errors="coerce").fillna(0)
    )
    df["Estimated Annual Internal Cost"] = (
        pd.to_numeric(df["Annual Usage"], errors="coerce").fillna(0)
        * pd.to_numeric(df["Estimated Internal Unit Cost"], errors="coerce").fillna(0)
    )
    df["Estimated Annual Savings"] = df["Annual Purchased Spend"] - df["Estimated Annual Internal Cost"]

    base_score = pd.Series(0.0, index=df.index)
    for score_col, weight_name in score_map.items():
        base_score += (df[score_col] / 5.0) * weights[weight_name]

    df["Base Score"] = base_score.round(1)
    df["Risk Modifier"] = df["Risk Level"].map(RISK_MODIFIERS).fillna(0)
    df["Final Score"] = (df["Base Score"] + df["Risk Modifier"]).round(1)

    return df


def to_excel_bytes(candidates: pd.DataFrame, decisions: pd.DataFrame, weights: dict) -> bytes:
    output = io.BytesIO()
    weights_df = pd.DataFrame(
        [{"Category": key, "Weight": value} for key, value in weights.items()]
    )
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        candidates.to_excel(writer, sheet_name="Candidates", index=False)
        decisions.to_excel(writer, sheet_name="Decision Log", index=False)
        weights_df.to_excel(writer, sheet_name="Weights", index=False)
    return output.getvalue()


def capability_summary(df: pd.DataFrame) -> pd.DataFrame:
    capability_cols = [
        "Swiss",
        "Laser Welding",
        "5-Axis",
        "Automated Handling",
        "Inspection / Metrology",
        "Fixturing",
        "Validation",
        "DFM Knowledge",
    ]
    rows = []
    for col in capability_cols:
        if col in df.columns:
            rows.append({"Capability": col, "Candidate Count": int(df[col].fillna(False).astype(bool).sum())})
    return pd.DataFrame(rows)


def header():
    st.title("Insourcing Prioritization Prototype")
    st.caption(
        "A working Streamlit prototype for evaluating, scoring, approving, and tracking part/product insourcing decisions."
    )


initialize_state()
header()

scored_df = calculate_scores(st.session_state.candidates, st.session_state.weights)

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Page",
        [
            "Dashboard",
            "Candidate Intake",
            "Scoring Matrix",
            "Decision Log",
            "Roadmap",
            "Capability Map",
            "Settings & Export",
        ],
    )

    st.divider()
    st.subheader("Filters")
    selected_status = st.multiselect(
        "Decision Status",
        DECISION_STATUSES,
        default=[],
    )
    selected_bucket = st.multiselect(
        "Portfolio Bucket",
        PORTFOLIO_BUCKETS,
        default=[],
    )
    selected_horizon = st.multiselect(
        "Roadmap Horizon",
        ROADMAP_HORIZONS,
        default=[],
    )

filtered_df = scored_df.copy()
if selected_status:
    filtered_df = filtered_df[filtered_df["Decision Status"].isin(selected_status)]
if selected_bucket:
    filtered_df = filtered_df[filtered_df["Portfolio Bucket"].isin(selected_bucket)]
if selected_horizon:
    filtered_df = filtered_df[filtered_df["Roadmap Horizon"].isin(selected_horizon)]


if page == "Dashboard":
    st.subheader("Executive Dashboard")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Candidates", len(filtered_df))
    kpi2.metric("Avg Final Score", f"{filtered_df['Final Score'].mean():.1f}" if len(filtered_df) else "0")
    kpi3.metric("Estimated Annual Savings", f"${filtered_df['Estimated Annual Savings'].sum():,.0f}")
    kpi4.metric("Approved / Conditional", int(filtered_df["Decision Status"].isin(["Approved", "Conditionally Approved"]).sum()))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.markdown("### Top Candidates")
        top_cols = [
            "Part Number",
            "Description",
            "Portfolio Bucket",
            "Roadmap Horizon",
            "Final Score",
            "Estimated Annual Savings",
            "Decision Status",
        ]
        st.dataframe(
            filtered_df.sort_values("Final Score", ascending=False)[top_cols],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.markdown("### Portfolio Mix")
        bucket_data = filtered_df.groupby("Portfolio Bucket", dropna=False).size().reset_index(name="Count")
        if len(bucket_data):
            chart = (
                alt.Chart(bucket_data)
                .mark_bar()
                .encode(
                    x=alt.X("Count:Q"),
                    y=alt.Y("Portfolio Bucket:N", sort="-x"),
                    tooltip=["Portfolio Bucket", "Count"],
                )
            )
            st.altair_chart(chart, use_container_width=True)

    left2, right2 = st.columns(2)

    with left2:
        st.markdown("### Roadmap Horizon")
        horizon_data = filtered_df.groupby("Roadmap Horizon", dropna=False).size().reset_index(name="Count")
        if len(horizon_data):
            chart = (
                alt.Chart(horizon_data)
                .mark_bar()
                .encode(
                    x=alt.X("Roadmap Horizon:N"),
                    y=alt.Y("Count:Q"),
                    tooltip=["Roadmap Horizon", "Count"],
                )
            )
            st.altair_chart(chart, use_container_width=True)

    with right2:
        st.markdown("### Capability Demand")
        cap_data = capability_summary(filtered_df)
        if len(cap_data):
            chart = (
                alt.Chart(cap_data)
                .mark_bar()
                .encode(
                    x=alt.X("Candidate Count:Q"),
                    y=alt.Y("Capability:N", sort="-x"),
                    tooltip=["Capability", "Candidate Count"],
                )
            )
            st.altair_chart(chart, use_container_width=True)


elif page == "Candidate Intake":
    st.subheader("Candidate Intake")

    with st.form("candidate_form", clear_on_submit=True):
        st.markdown("### Add Candidate Part / Product")
        c1, c2, c3 = st.columns(3)

        with c1:
            part_number = st.text_input("Part Number")
            description = st.text_input("Description")
            product_family = st.text_input("Product Family")
            current_supplier = st.text_input("Current Supplier")

        with c2:
            annual_usage = st.number_input("Annual Usage", min_value=0, step=1)
            purchase_price = st.number_input("Current Purchase Price", min_value=0.0, step=0.01)
            internal_cost = st.number_input("Estimated Internal Unit Cost", min_value=0.0, step=0.01)
            supplier_lead_time = st.number_input("Supplier Lead Time Weeks", min_value=0, step=1)

        with c3:
            target_process = st.text_input("Target Process")
            required_machine = st.selectbox("Required Machine / Enabler", REQUIRED_ENABLERS)
            quality_history = st.selectbox("Quality History", ["Stable", "Moderate Issues", "Recurring Issues", "Unknown"])
            owner = st.selectbox("Owner", FUNCTIONAL_AREAS)

        st.markdown("### Initial Scoring")
        s1, s2, s3, s4 = st.columns(4)
        financial_score = s1.slider("Financial Score", 1, 5, 3)
        capability_score = s1.slider("Capability Growth Score", 1, 5, 3)
        lead_time_score = s2.slider("Lead Time Control Score", 1, 5, 3)
        quality_score = s2.slider("Quality Control Score", 1, 5, 3)
        feasibility_score = s3.slider("Feasibility Score", 1, 5, 3)
        capacity_score = s3.slider("Capacity Fit Score", 1, 5, 3)
        future_product_score = s4.slider("Future Product Score", 1, 5, 3)
        risk_level = s4.selectbox("Risk Level", list(RISK_MODIFIERS.keys()))

        st.markdown("### Classification")
        class1, class2, class3 = st.columns(3)
        decision_status = class1.selectbox("Decision Status", DECISION_STATUSES, index=1)
        portfolio_bucket = class2.selectbox("Portfolio Bucket", PORTFOLIO_BUCKETS)
        roadmap_horizon = class3.selectbox("Roadmap Horizon", ROADMAP_HORIZONS)

        st.markdown("### Capability Tags")
        tags = st.columns(4)
        swiss = tags[0].checkbox("Swiss")
        laser = tags[0].checkbox("Laser Welding")
        five_axis = tags[1].checkbox("5-Axis")
        automation = tags[1].checkbox("Automated Handling")
        inspection = tags[2].checkbox("Inspection / Metrology")
        fixturing = tags[2].checkbox("Fixturing")
        validation = tags[3].checkbox("Validation")
        dfm = tags[3].checkbox("DFM Knowledge")

        next_action = st.text_area("Next Action")
        target_start = st.date_input("Target Start", value=date.today())
        target_completion = st.date_input("Target Completion", value=date.today())

        submitted = st.form_submit_button("Add Candidate")

        if submitted:
            if not part_number:
                st.error("Part Number is required.")
            else:
                new_row = {
                    "Part Number": part_number,
                    "Description": description,
                    "Product Family": product_family,
                    "Current Supplier": current_supplier,
                    "Annual Usage": annual_usage,
                    "Current Purchase Price": purchase_price,
                    "Estimated Internal Unit Cost": internal_cost,
                    "Target Process": target_process,
                    "Required Machine": required_machine,
                    "Supplier Lead Time Weeks": supplier_lead_time,
                    "Quality History": quality_history,
                    "Financial Score": financial_score,
                    "Capability Growth Score": capability_score,
                    "Lead Time Control Score": lead_time_score,
                    "Quality Control Score": quality_score,
                    "Feasibility Score": feasibility_score,
                    "Capacity Fit Score": capacity_score,
                    "Future Product Score": future_product_score,
                    "Risk Level": risk_level,
                    "Decision Status": decision_status,
                    "Portfolio Bucket": portfolio_bucket,
                    "Roadmap Horizon": roadmap_horizon,
                    "Required Enabler": required_machine,
                    "Owner": owner,
                    "Next Action": next_action,
                    "Target Start": str(target_start),
                    "Target Completion": str(target_completion),
                    "Swiss": swiss,
                    "Laser Welding": laser,
                    "5-Axis": five_axis,
                    "Automated Handling": automation,
                    "Inspection / Metrology": inspection,
                    "Fixturing": fixturing,
                    "Validation": validation,
                    "DFM Knowledge": dfm,
                }
                st.session_state.candidates = pd.concat(
                    [st.session_state.candidates, pd.DataFrame([new_row])],
                    ignore_index=True,
                )
                st.success(f"Added candidate {part_number}.")

    st.markdown("### Current Candidate List")
    st.dataframe(calculate_scores(st.session_state.candidates, st.session_state.weights), use_container_width=True, hide_index=True)


elif page == "Scoring Matrix":
    st.subheader("Scoring Matrix")

    st.info(
        "Scores are 1-5. The app calculates a weighted base score, applies the risk modifier, and generates a final score."
    )

    editable_cols = [
        "Part Number",
        "Description",
        "Financial Score",
        "Capability Growth Score",
        "Lead Time Control Score",
        "Quality Control Score",
        "Feasibility Score",
        "Capacity Fit Score",
        "Future Product Score",
        "Risk Level",
        "Decision Status",
        "Portfolio Bucket",
        "Roadmap Horizon",
        "Required Enabler",
        "Owner",
        "Next Action",
    ]

    edited = st.data_editor(
        st.session_state.candidates[editable_cols],
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Financial Score": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
            "Capability Growth Score": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
            "Lead Time Control Score": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
            "Quality Control Score": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
            "Feasibility Score": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
            "Capacity Fit Score": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
            "Future Product Score": st.column_config.NumberColumn(min_value=1, max_value=5, step=1),
            "Risk Level": st.column_config.SelectboxColumn(options=list(RISK_MODIFIERS.keys())),
            "Decision Status": st.column_config.SelectboxColumn(options=DECISION_STATUSES),
            "Portfolio Bucket": st.column_config.SelectboxColumn(options=PORTFOLIO_BUCKETS),
            "Roadmap Horizon": st.column_config.SelectboxColumn(options=ROADMAP_HORIZONS),
            "Required Enabler": st.column_config.SelectboxColumn(options=REQUIRED_ENABLERS),
            "Owner": st.column_config.SelectboxColumn(options=FUNCTIONAL_AREAS),
        },
    )

    if st.button("Save Scoring Changes"):
        for col in edited.columns:
            st.session_state.candidates[col] = edited[col]
        st.success("Scoring changes saved.")

    st.markdown("### Calculated Scores")
    calc_cols = [
        "Part Number",
        "Description",
        "Base Score",
        "Risk Level",
        "Risk Modifier",
        "Final Score",
        "Estimated Annual Savings",
        "Decision Status",
        "Portfolio Bucket",
        "Roadmap Horizon",
    ]
    st.dataframe(
        calculate_scores(st.session_state.candidates, st.session_state.weights)
        .sort_values("Final Score", ascending=False)[calc_cols],
        use_container_width=True,
        hide_index=True,
    )


elif page == "Decision Log":
    st.subheader("Decision Log")

    with st.form("decision_form", clear_on_submit=True):
        st.markdown("### Log Decision")
        d1, d2, d3 = st.columns(3)

        with d1:
            decision_date = st.date_input("Decision Date", value=date.today())
            part_number = st.selectbox("Part Number", scored_df["Part Number"].tolist())
            decision = st.selectbox("Decision", ["Approved", "Conditionally Approved", "Deferred", "Rejected"])

        with d2:
            owner = st.selectbox("Owner", FUNCTIONAL_AREAS)
            due_date = st.date_input("Due Date", value=date.today())
            review_status = st.selectbox("Review Status", ["Open", "In Progress", "Closed"])

        with d3:
            rationale = st.text_area("Rationale")
            conditions = st.text_area("Conditions / Follow-Ups")

        submitted = st.form_submit_button("Add Decision Record")
        if submitted:
            new_decision = {
                "Decision Date": str(decision_date),
                "Part Number": part_number,
                "Decision": decision,
                "Rationale": rationale,
                "Conditions": conditions,
                "Owner": owner,
                "Due Date": str(due_date),
                "Review Status": review_status,
            }
            st.session_state.decision_log = pd.concat(
                [st.session_state.decision_log, pd.DataFrame([new_decision])],
                ignore_index=True,
            )
            st.success("Decision record added.")

    st.markdown("### Decision Records")
    st.dataframe(st.session_state.decision_log, use_container_width=True, hide_index=True)


elif page == "Roadmap":
    st.subheader("Roadmap")

    roadmap_cols = [
        "Part Number",
        "Description",
        "Portfolio Bucket",
        "Roadmap Horizon",
        "Required Enabler",
        "Owner",
        "Target Start",
        "Target Completion",
        "Decision Status",
        "Final Score",
        "Next Action",
    ]
    roadmap_df = filtered_df[roadmap_cols].sort_values(["Roadmap Horizon", "Final Score"], ascending=[True, False])
    st.dataframe(roadmap_df, use_container_width=True, hide_index=True)

    st.markdown("### Roadmap by Horizon")
    roadmap_count = roadmap_df.groupby(["Roadmap Horizon", "Portfolio Bucket"]).size().reset_index(name="Count")
    if len(roadmap_count):
        chart = (
            alt.Chart(roadmap_count)
            .mark_bar()
            .encode(
                x=alt.X("Roadmap Horizon:N"),
                y=alt.Y("Count:Q"),
                color=alt.Color("Portfolio Bucket:N"),
                tooltip=["Roadmap Horizon", "Portfolio Bucket", "Count"],
            )
        )
        st.altair_chart(chart, use_container_width=True)


elif page == "Capability Map":
    st.subheader("Capability Map")

    cap_cols = [
        "Part Number",
        "Description",
        "Portfolio Bucket",
        "Roadmap Horizon",
        "Swiss",
        "Laser Welding",
        "5-Axis",
        "Automated Handling",
        "Inspection / Metrology",
        "Fixturing",
        "Validation",
        "DFM Knowledge",
    ]
    st.dataframe(filtered_df[cap_cols], use_container_width=True, hide_index=True)

    st.markdown("### Capability Summary")
    cap_data = capability_summary(filtered_df)
    st.dataframe(cap_data, use_container_width=True, hide_index=True)

    if len(cap_data):
        chart = (
            alt.Chart(cap_data)
            .mark_bar()
            .encode(
                x=alt.X("Candidate Count:Q"),
                y=alt.Y("Capability:N", sort="-x"),
                tooltip=["Capability", "Candidate Count"],
            )
        )
        st.altair_chart(chart, use_container_width=True)


elif page == "Settings & Export":
    st.subheader("Settings & Export")

    st.markdown("### Scoring Weights")
    st.caption("Weights should total 100 points. Adjust these to match leadership priorities.")

    new_weights = {}
    total_weight = 0
    for key, value in st.session_state.weights.items():
        new_value = st.number_input(key, min_value=0, max_value=100, value=int(value), step=1)
        new_weights[key] = new_value
        total_weight += new_value

    st.metric("Total Weight", total_weight)

    if total_weight != 100:
        st.warning("Weights should total 100 before using the model for governance decisions.")

    if st.button("Save Weights"):
        st.session_state.weights = new_weights
        st.success("Weights saved.")

    st.divider()
    st.markdown("### Data Import")

    uploaded = st.file_uploader("Upload candidate CSV", type=["csv"])
    if uploaded is not None:
        uploaded_df = pd.read_csv(uploaded)
        if st.button("Replace Candidate Data with Uploaded CSV"):
            st.session_state.candidates = uploaded_df
            st.success("Candidate data replaced.")

    st.divider()
    st.markdown("### Export")

    export_df = calculate_scores(st.session_state.candidates, st.session_state.weights)
    st.download_button(
        "Download Candidates as CSV",
        data=export_df.to_csv(index=False),
        file_name="insourcing_candidates_scored.csv",
        mime="text/csv",
    )

    st.download_button(
        "Download Workbook Export",
        data=to_excel_bytes(export_df, st.session_state.decision_log, st.session_state.weights),
        file_name="insourcing_prioritization_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.markdown("### Current Data Preview")
    st.dataframe(export_df, use_container_width=True, hide_index=True)
