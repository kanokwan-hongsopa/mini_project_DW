import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Airline DW Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DATABASE PATH
# app.py อยู่ที่ root
# dev.duckdb อยู่ใน airline_dw/
# =========================================================

DB_PATH = Path(__file__).resolve().parent / "airline_dw" / "dev.duckdb"

if not DB_PATH.exists():
    st.error(f"ไม่พบฐานข้อมูล: {DB_PATH}")
    st.stop()

con = duckdb.connect(str(DB_PATH), read_only=True)

# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #ffffff;
        color: #111827;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: #f4f6f8;
        border-right: 1px solid #e5e7eb;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 15px;
        color: #64748b;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 750;
        margin-top: 10px;
        margin-bottom: 15px;
        color: #111827;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 12px;
        padding: 10px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# GET ALL TABLES
# =========================================================

all_tables = con.execute(
    """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'main'
    ORDER BY table_name
    """
).fetchdf()["table_name"].tolist()

# =========================================================
# MAIN DW TABLES
# =========================================================

DW_TABLES = [
    "dim_date",
    "dim_airport",
    "dim_aircraft",
    "dim_fare_class",
    "dim_flight_status",
    "fact_ticket_sales",
    "fact_flight_operations",
    "fact_seat_utilization",
]

available_dw_tables = [
    table
    for table in DW_TABLES
    if table in all_tables
]

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🗂️ Table Browser")

st.sidebar.caption(
    "Select a table to inspect"
)

selected_table = st.sidebar.selectbox(
    "Table",
    available_dw_tables
)

st.sidebar.divider()

# =========================================================
# QUICK STATS
# =========================================================

total_tables = len(all_tables)

dimension_count = len([
    table
    for table in available_dw_tables
    if table.startswith("dim_")
])

fact_count = len([
    table
    for table in available_dw_tables
    if table.startswith("fact_")
])

total_records = 0

for table_name in all_tables:
    count = con.execute(
        f'SELECT COUNT(*) FROM "{table_name}"'
    ).fetchone()[0]

    total_records += count

st.sidebar.markdown("### Quick Stats")

st.sidebar.write(
    f"**Total Tables:** {total_tables}"
)

st.sidebar.write(
    f"**Dimensions:** {dimension_count}"
)

st.sidebar.write(
    f"**Facts:** {fact_count}"
)

st.sidebar.write(
    f"**Total Records:** {total_records:,}"
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        📊 Airline DW Explorer
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Inspect and preview raw, staging, dimension and fact tables
        in dev.duckdb
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs(
    [
        "📋 Database Schema & Overview",
        "🔍 Data Viewer & Metadata",
    ]
)

# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-title">Database Tables Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Total Tables in main Schema",
        total_tables
    )

    c2.metric(
        "Total Records Across All Tables",
        f"{total_records:,}"
    )

    st.markdown(
        '<div class="section-title">Table List & Record Counts</div>',
        unsafe_allow_html=True
    )

    rows = []

    for table_name in all_tables:

        row_count = con.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]

        schema = con.execute(
            f"PRAGMA table_info('{table_name}')"
        ).fetchdf()

        if table_name.startswith("dim_"):
            table_type = "Dimension"

        elif table_name.startswith("fact_"):
            table_type = "Fact"

        elif table_name.startswith("stg_"):
            table_type = "Staging"

        else:
            table_type = "Other"

        rows.append(
            {
                "Table Name": table_name,
                "Table Type": table_type,
                "Row Count": row_count,
                "Column Count": len(schema),
            }
        )

    overview_df = pd.DataFrame(rows)

    st.dataframe(
        overview_df,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.markdown(
        f"""
        <div class="section-title">
            Data Viewer: {selected_table}
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # TABLE STATS
    # -----------------------------------------------------

    row_count = con.execute(
        f'SELECT COUNT(*) FROM "{selected_table}"'
    ).fetchone()[0]

    schema_df = con.execute(
        f"PRAGMA table_info('{selected_table}')"
    ).fetchdf()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        f"{row_count:,}"
    )

    c2.metric(
        "Columns",
        len(schema_df)
    )

    if selected_table.startswith("dim_"):
        table_type = "Dimension"

    elif selected_table.startswith("fact_"):
        table_type = "Fact"

    elif selected_table.startswith("stg_"):
        table_type = "Staging"

    else:
        table_type = "Other"

    c3.metric(
        "Table Type",
        table_type
    )

    # -----------------------------------------------------
    # METADATA
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Metadata / Data Types</div>',
        unsafe_allow_html=True
    )

    metadata_cols = [
        col
        for col in [
            "name",
            "type",
            "notnull",
            "pk",
        ]
        if col in schema_df.columns
    ]

    st.dataframe(
        schema_df[metadata_cols],
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # PREVIEW DATA
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Sample Data</div>',
        unsafe_allow_html=True
    )

    preview_rows = st.slider(
        "จำนวนแถวที่ต้องการ Preview",
        min_value=5,
        max_value=100,
        value=20,
        step=5
    )

    sample_df = con.execute(
        f"""
        SELECT *
        FROM "{selected_table}"
        LIMIT {preview_rows}
        """
    ).fetchdf()

    st.dataframe(
        sample_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # NULL CHECK
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Column Quality Check</div>',
        unsafe_allow_html=True
    )

    quality_rows = []

    for column_name in schema_df["name"].tolist():

        null_count = con.execute(
            f"""
            SELECT
                COUNT(*) - COUNT("{column_name}")
            FROM "{selected_table}"
            """
        ).fetchone()[0]

        data_type = schema_df.loc[
            schema_df["name"] == column_name,
            "type"
        ].iloc[0]

        quality_rows.append(
            {
                "Column": column_name,
                "Data Type": data_type,
                "Null Count": null_count,
            }
        )

    quality_df = pd.DataFrame(
        quality_rows
    )

    st.dataframe(
        quality_df,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Airline Data Warehouse • DuckDB • dbt • Streamlit"
)

con.close()