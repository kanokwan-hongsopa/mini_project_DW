import duckdb

con = duckdb.connect("dev.duckdb")

con.execute("CREATE SCHEMA IF NOT EXISTS raw")

con.execute("""
CREATE OR REPLACE TABLE raw.bookings AS
SELECT *
FROM read_csv_auto('datasetss/bookings.csv', all_varchar=true)
""")

con.execute("""
CREATE OR REPLACE TABLE raw.tickets AS
SELECT *
FROM read_csv_auto('datasetss/tickets.csv', all_varchar=true)
""")

con.execute("""
CREATE OR REPLACE TABLE raw.ticket_flights AS
SELECT *
FROM read_csv_auto('datasetss/ticket_flights.csv', all_varchar=true)
""")

print("Raw tables created successfully")

print(con.execute("""
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'raw'
ORDER BY table_name
""").fetchdf())

con.close()