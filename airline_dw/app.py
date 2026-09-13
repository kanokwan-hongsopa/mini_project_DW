import streamlit as st
import duckdb
from pathlib import Path

st.set_page_config(
    page_title="Airline Data Warehouse Dashboard",
    layout="wide"
)

# Connect to DuckDB
DB_PATH = Path(__file__).resolve().parent / "dev.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

# =========================
# TITLE
# =========================

st.title("Airline Data Warehouse Dashboard")
st.write("Dashboard for analyzing airline operations and ticket sales")


# =========================
# KPI
# =========================

total_sales = con.execute("""
    SELECT SUM(amount)
    FROM fact_ticket_sales
""").fetchone()[0]

total_ticket_flights = con.execute("""
    SELECT SUM(ticket_flight_count)
    FROM fact_ticket_sales
""").fetchone()[0]

total_flights = con.execute("""
    SELECT SUM(flight_count)
    FROM fact_flight_operations
""").fetchone()[0]

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


# =========================
# Q9: TOP ROUTES BY SALES
# =========================

st.subheader("Top Routes by Ticket Sales")

route_sales = con.execute("""
    SELECT
        dep.airport_code AS departure_airport,
        arr.airport_code AS arrival_airport,
        dep.airport_code || ' → ' || arr.airport_code AS route,
        SUM(f.amount) AS total_ticket_sales
    FROM fact_ticket_sales f
    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr
        ON f.arrival_airport_key = arr.airport_key
    GROUP BY
        dep.airport_code,
        arr.airport_code
    ORDER BY total_ticket_sales DESC
    LIMIT 10
""").fetchdf()

st.bar_chart(
    route_sales,
    x="route",
    y="total_ticket_sales"
)

# =========================
# Q10: AIRCRAFT USAGE
# =========================

st.subheader("Aircraft Usage by Number of Flights")

aircraft_usage = con.execute("""
    SELECT
        a.model,
        SUM(f.flight_count) AS total_flights
    FROM fact_flight_operations f
    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key
    GROUP BY
        a.model
    ORDER BY
        total_flights DESC
""").fetchdf()

st.bar_chart(
    aircraft_usage,
    x="model",
    y="total_flights"
)


# =========================
# Q11: AIRCRAFT SEAT COUNT
# =========================

st.subheader("Seat Capacity by Aircraft Model")

aircraft_seats = con.execute("""
    SELECT
        a.model,
        SUM(f.seat_count) AS total_seats
    FROM fact_seat_inventory f
    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key
    GROUP BY
        a.model
    ORDER BY
        total_seats DESC
""").fetchdf()

st.bar_chart(
    aircraft_seats,
    x="model",
    y="total_seats"
)
# =========================
# Q10: AIRCRAFT USAGE
# =========================

st.subheader("Aircraft Usage by Number of Flights")

aircraft_usage = con.execute("""
    SELECT
        a.model,
        SUM(f.flight_count) AS total_flights
    FROM fact_flight_operations f
    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key
    GROUP BY a.model
    ORDER BY total_flights DESC
""").fetchdf()

st.bar_chart(
    aircraft_usage,
    x="model",
    y="total_flights"
)


# =========================
# Q11: AIRCRAFT SEAT COUNT
# =========================

st.subheader("Seat Capacity by Aircraft Model")

aircraft_seats = con.execute("""
    SELECT
        a.model,
        SUM(f.seat_count) AS total_seats
    FROM fact_seat_inventory f
    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key
    GROUP BY a.model
    ORDER BY total_seats DESC
""").fetchdf()

st.bar_chart(
    aircraft_seats,
    x="model",
    y="total_seats"
)
# =========================
# Q12: FARE CLASS SEAT SHARE
# =========================

st.subheader("Fare Class Seat Share by Aircraft Model")

fare_share = con.execute("""
    WITH seat_summary AS (
        SELECT
            a.model,
            fc.fare_class,
            SUM(f.seat_count) AS seat_count
        FROM fact_seat_inventory f
        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key
        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key
        GROUP BY
            a.model,
            fc.fare_class
    )

    SELECT
        model,
        fare_class,
        seat_count
    FROM seat_summary
    ORDER BY
        model,
        seat_count DESC
""").fetchdf()

st.bar_chart(
    fare_share,
    x="model",
    y="seat_count",
    color="fare_class"
)


# =========================
# Q13: FLIGHT STATUS
# =========================

st.subheader("Flights by Status")

flight_status = con.execute("""
    SELECT
        s.status_name,
        SUM(f.flight_count) AS total_flights
    FROM fact_flight_operations f
    JOIN dim_flight_status s
        ON f.status_key = s.status_key
    GROUP BY
        s.status_name
    ORDER BY
        total_flights DESC
""").fetchdf()

st.bar_chart(
    flight_status,
    x="status_name",
    y="total_flights"
)
con.close()