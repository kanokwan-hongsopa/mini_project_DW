import duckdb
from pathlib import Path

DB_PATH = "dev.duckdb"
DATA_DIR = Path("datasetss")

tables = {
    "aircrafts_data": "aircrafts_data.csv",
    "airports_data": "airports_data.csv",
    "boarding_passes": "boarding_passes.csv",
    "bookings": "bookings.csv",
    "flights": "flights.csv",
    "seats": "seats.csv",
    "ticket_flights": "ticket_flights.csv",
    "tickets": "tickets.csv",
}

con = duckdb.connect(DB_PATH)

con.execute("CREATE SCHEMA IF NOT EXISTS raw")

for table_name, file_name in tables.items():
    file_path = DATA_DIR / file_name

    print(f"Loading {file_name} -> raw.{table_name}")

    con.execute(
        f"""
        CREATE OR REPLACE TABLE raw.{table_name} AS
        SELECT *
        FROM read_csv_auto(
            '{file_path.as_posix()}',
            header = true,
            all_varchar = true
        )
        """
    )

print("\nRaw tables created successfully.")

for table_name in tables:
    count = con.execute(
        f"SELECT COUNT(*) FROM raw.{table_name}"
    ).fetchone()[0]

    print(f"{table_name}: {count:,} rows")

con.close()