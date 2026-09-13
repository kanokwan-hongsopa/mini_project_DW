import streamlit as st
import duckdb
from pathlib import Path

st.set_page_config(
    page_title="Airline Data Warehouse Dashboard",
    layout="wide"
)

DB_PATH = Path(__file__).resolve().parents[1] / "dev.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

st.title("Airline Data Warehouse Dashboard")
st.write("Dashboard for analyzing airline operations and ticket sales")

# KPI 1: Total Ticket Sales
total_sales = con.execute("""
    SELECT SUM(amount)
    FROM fact_ticket_sales
""").fetchone()[0]

# KPI 2: Total Ticket Flights
total_ticket_flights = con.execute("""
    SELECT SUM(ticket_flight_count)
    FROM fact_ticket_sales
""").fetchone()[0]

# KPI 3: Total Flights
total_flights = con.execute("""
    SELECT SUM(flight_count)
    FROM fact_flight_operations
""").fetchone()[0]

# KPI 4: Average Departure Delay
avg_delay = con.execute("""
    SELECT AVG(departure_delay_minutes)
    FROM fact_flight_operations
    WHERE departure_delay_minutes > 0
""").fetchone()[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Ticket Sales",
    f"{total_sales:,.2f}"
)

col2.metric(
    "Total Ticket Flights",
    f"{total_ticket_flights:,.0f}"
)

col3.metric(
    "Total Flights",
    f"{total_flights:,.0f}"
)

col4.metric(
    "Average Departure Delay",
    f"{avg_delay:,.2f} min"
)

con.close()