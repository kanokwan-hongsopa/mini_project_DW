# 06 ETL Pipeline and Transformations

## 1. Overview

This project implements an ELT-style pipeline for airline operational data.

The overall data flow is:

CSV Source Files
→ Python Loader
→ DuckDB Raw Schema
→ dbt Staging Models
→ Dimension Tables
→ Fact Tables
→ Data Warehouse
→ Interactive Dashboard

The purpose of the pipeline is to clean, standardize, validate, and transform operational data before using it in the analytical data warehouse.

---

## 2. Extract Process

The source data consists of eight CSV files:

- aircrafts_data.csv
- airports_data.csv
- boarding_passes.csv
- bookings.csv
- flights.csv
- seats.csv
- ticket_flights.csv
- tickets.csv

The Python script:

`scripts/load_raw.py`

is used to load these files into DuckDB.

The data is loaded into the `raw` schema inside `dev.duckdb`.

The loader uses DuckDB's CSV reader and initially loads source columns as VARCHAR to preserve the original raw values before transformation.

Examples of raw tables include:

- raw.aircrafts_data
- raw.airports_data
- raw.boarding_passes
- raw.bookings
- raw.flights
- raw.seats
- raw.ticket_flights
- raw.tickets

---

## 3. Staging Layer

The staging layer is implemented using dbt.

The staging models are located in:

`models/staging/`

The staging layer prepares operational data before it is used to create Dimensions and Facts.

The models include:

- stg_bookings
- stg_tickets
- stg_ticket_flights
- stg_flights
- stg_airports
- stg_aircrafts
- stg_seats
- stg_boarding_passes

The staging models are materialized as views.

---

## 4. Data Cleaning and Transformations

### 4.1 stg_flights

The `stg_flights` model performs the following transformations:

- Converts `flight_id` from VARCHAR to INTEGER
- Converts scheduled departure and arrival values to TIMESTAMPTZ
- Converts actual departure and arrival values to TIMESTAMPTZ
- Converts `\N` values to SQL NULL
- Removes unnecessary whitespace
- Standardizes airport codes using UPPER
- Standardizes aircraft codes using UPPER
- Preserves valid missing actual departure and arrival values

Missing actual timestamps are not removed because scheduled or cancelled flights may not yet have actual departure or arrival times.

---

### 4.2 stg_airports

The `stg_airports` model performs the following transformations:

- Standardizes `airport_code` using UPPER and TRIM
- Removes unnecessary whitespace from airport names
- Cleans city values
- Cleans coordinate values
- Cleans timezone values

Airport data is treated as master data and is prepared for the `dim_airport` dimension.

---

### 4.3 stg_aircrafts

The `stg_aircrafts` model performs the following transformations:

- Standardizes `aircraft_code`
- Removes unnecessary whitespace from aircraft model names
- Converts aircraft `range` from VARCHAR to INTEGER

The cleaned data is prepared for the `dim_aircraft` dimension.

---

### 4.4 stg_seats

The `stg_seats` model performs the following transformations:

- Standardizes aircraft codes
- Standardizes seat numbers
- Cleans fare condition values
- Validates seat records using the combination of `aircraft_code` and `seat_no`

The data supports fare class analysis and seat inventory analysis.

---

### 4.5 stg_boarding_passes

The `stg_boarding_passes` model performs the following transformations:

- Cleans ticket numbers
- Converts `flight_id` to INTEGER
- Converts `boarding_no` to INTEGER
- Standardizes seat numbers

The combination of `ticket_no` and `flight_id` is used to validate duplicate boarding pass records.

---

## 5. NULL Handling

NULL handling is performed based on the business meaning of the data.

For example, the raw `flights` data may contain:

`\N`

in `actual_departure` and `actual_arrival`.

These values are converted to SQL NULL.

The records are not deleted because missing actual timestamps may be valid for:

- Scheduled flights
- Cancelled flights
- Flights that have not yet departed
- Flights that have not yet arrived

This preserves valid operational information.

---

## 6. Duplicate Validation

Duplicate records are checked using appropriate business keys.

The duplicate validation rules include:

- Flights: `flight_id`
- Airports: `airport_code`
- Aircrafts: `aircraft_code`
- Seats: `aircraft_code + seat_no`
- Boarding passes: `ticket_no + flight_id`

The validation did not identify duplicate records for these keys, so no valid rows were removed.

---

## 7. Data Quality Tests

dbt tests are used to validate data quality.

The project includes tests such as:

- `not_null`
- `unique`
- `relationships`
- `accepted_values`

Examples include:

- `flight_id` must not be NULL and must be unique
- `airport_code` must not be NULL and must be unique
- `aircraft_code` must not be NULL and must be unique
- departure and arrival airport codes must exist in `stg_airports`
- aircraft codes in flights must exist in `stg_aircrafts`
- flight IDs in boarding passes must exist in `stg_flights`
- fare conditions must contain accepted values
- flight status must contain accepted values

These tests help ensure data integrity before loading analytical models.

---

## 8. Load Process

After the staging models are cleaned and validated, the data is used to build the dimensional data warehouse.

The load order is:

Raw Data
→ Staging
→ Dimensions
→ Facts
→ Analytics
→ Dashboard

Dimension tables are created before Fact tables.

This helps preserve referential integrity because Fact tables depend on Dimension keys.

Examples of downstream models include:

- dim_airport
- dim_aircraft
- dim_date
- dim_fare_class
- dim_flight_status
- fact_ticket_sales
- fact_flight_operations
- fact_seat_inventory

---

## 9. Pipeline Diagram

```mermaid
flowchart LR
    A[CSV Operational Data]
    --> B[Python load_raw.py]

    B --> C[DuckDB Raw Schema]

    C --> D[dbt Staging Models]

    D --> E[Dimension Tables]

    E --> F[Fact Tables]

    F --> G[Data Warehouse]

    G --> H[Interactive Dashboard]

10. Validation Commands

The following commands are used to validate the pipeline:

python scripts/load_raw.py
dbt debug
dbt run
dbt test

The environment is configured using a Python virtual environment:

python -m venv .venv
source .venv/bin/activate

Dependencies are stored in:

requirements.txt

The pipeline is considered valid when:

the raw data loads successfully
dbt connection checks pass
staging models build successfully
dbt data quality tests pass
downstream Dimension and Fact models can reference the staging models successfully
11. Summary

The ETL/ELT process ensures that operational airline data is transformed into a clean and validated structure before entering the Data Warehouse.

The process includes:

Extracting data from CSV files
Loading data into DuckDB
Cleaning and standardizing values
Converting data types
Handling NULL values
Checking duplicate records
Running dbt data quality tests
Loading Dimensions before Facts
Preparing the data for analytical queries and dashboard visualization