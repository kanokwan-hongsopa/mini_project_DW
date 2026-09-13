# 06 ETL Pipeline and Transformations

## 1. Overview

The project uses an ELT-style pipeline to move airline
operational data from CSV files into DuckDB and transform
the raw data using dbt.

Pipeline:

CSV Source Files
→ DuckDB Raw Schema
→ dbt Staging Models
→ Dimension Tables
→ Fact Tables
→ Data Warehouse
→ Dashboard


## 2. Extract

The source data consists of eight operational CSV files:

- aircrafts_data.csv
- airports_data.csv
- boarding_passes.csv
- bookings.csv
- flights.csv
- seats.csv
- ticket_flights.csv
- tickets.csv

The Python script `scripts/load_raw.py` loads all CSV files
into the `raw` schema of `dev.duckdb`.

All source columns are initially loaded as VARCHAR using
`read_csv_auto(..., all_varchar=true)`.


## 3. Raw Data Layer

The raw schema preserves the source data before business
transformations.

Examples:

- raw.flights
- raw.airports_data
- raw.aircrafts_data
- raw.seats
- raw.boarding_passes


## 4. Staging Transformations

### 4.1 stg_flights

Transformations include:

- flight_id converted from VARCHAR to INTEGER
- scheduled timestamps converted to TIMESTAMPTZ
- actual timestamps converted to TIMESTAMPTZ
- `\N` values converted to SQL NULL
- airport codes standardized using TRIM and UPPER
- aircraft codes standardized using TRIM and UPPER
- flight status cleaned using TRIM

Missing actual departure and arrival values are retained
as NULL because scheduled or cancelled flights may not have
actual timestamps.


### 4.2 stg_airports

Transformations include:

- airport codes standardized to uppercase
- whitespace removed from text attributes
- airport master data retained at one row per airport code


### 4.3 stg_aircrafts

Transformations include:

- aircraft codes standardized to uppercase
- model names trimmed
- aircraft range converted from VARCHAR to INTEGER


### 4.4 stg_seats

Transformations include:

- aircraft codes standardized
- seat numbers standardized
- fare conditions cleaned
- validation performed using the composite business key
  aircraft_code + seat_no


### 4.5 stg_boarding_passes

Transformations include:

- flight_id converted to INTEGER
- boarding_no converted to INTEGER
- seat numbers standardized
- duplicate validation performed using
  ticket_no + flight_id


## 5. Data Quality Validation

dbt tests are used to validate:

- NOT NULL constraints
- uniqueness of business keys
- relationships between staging models
- accepted flight status values
- accepted fare class values

Duplicate validation found no duplicate records for:

- flights: flight_id
- airports: airport_code
- aircrafts: aircraft_code
- seats: aircraft_code + seat_no
- boarding passes: ticket_no + flight_id


## 6. Load Process

After staging transformations are completed and validated,
the cleaned data is used to build Dimension tables first.

The Fact tables are then created using the Dimension keys.

Load order:

Raw
→ Staging
→ Dimensions
→ Facts
→ Analytics / Dashboard

Loading Dimensions before Facts helps maintain referential
integrity between Fact and Dimension tables.


## 7. Validation Commands

```bash
python scripts/load_raw.py
dbt debug
dbt run
dbt test

````markdown
```mermaid
flowchart LR
    A[CSV Operational Data]
    --> B[Python load_raw.py]

    B --> C[DuckDB raw schema]

    C --> D[dbt Staging]

    D --> E[Dimension Tables]

    E --> F[Fact Tables]

    F --> G[Data Warehouse]

    G --> H[Interactive Dashboard]