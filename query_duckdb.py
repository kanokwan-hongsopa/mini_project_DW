import duckdb
from pathlib import Path
import pandas as pd

# =========================================================
# DATABASE PATH
# query_duckdb.py อยู่ที่ root ของ mini_project_DW
# dev.duckdb อยู่ใน airline_dw/
# =========================================================

DB_PATH = Path(__file__).resolve().parent / "airline_dw" / "dev.duckdb"

if not DB_PATH.exists():
    print(f"ไม่พบฐานข้อมูล: {DB_PATH}")
    raise SystemExit

con = duckdb.connect(str(DB_PATH), read_only=True)

# =========================================================
# TABLE GROUPS
# =========================================================

DIMENSION_TABLES = [
    "dim_date",
    "dim_airport",
    "dim_aircraft",
    "dim_fare_class",
    "dim_flight_status",
]

FACT_TABLES = [
    "fact_ticket_sales",
    "fact_flight_operations",
    "fact_seat_utilization",
]

DW_TABLES = DIMENSION_TABLES + FACT_TABLES


# =========================================================
# HELPERS
# =========================================================

def line():
    print("=" * 90)


def table_exists(table_name):
    result = con.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = ?
        """,
        [table_name],
    ).fetchone()[0]

    return result > 0


# =========================================================
# SHOW DW OVERVIEW
# =========================================================

def show_dw_overview():
    line()
    print("AIRLINE DATA WAREHOUSE OVERVIEW")
    line()

    rows = []

    for table_name in DW_TABLES:

        if not table_exists(table_name):
            rows.append(
                {
                    "table_name": table_name,
                    "table_type": (
                        "Dimension"
                        if table_name.startswith("dim_")
                        else "Fact"
                    ),
                    "record_count": "NOT FOUND",
                    "column_count": "NOT FOUND",
                }
            )
            continue

        count = con.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]

        schema = con.execute(
            f"PRAGMA table_info('{table_name}')"
        ).fetchdf()

        rows.append(
            {
                "table_name": table_name,
                "table_type": (
                    "Dimension"
                    if table_name.startswith("dim_")
                    else "Fact"
                ),
                "record_count": count,
                "column_count": len(schema),
            }
        )

    df = pd.DataFrame(rows)

    print()
    print(df.to_string(index=False))

    existing_df = df[
        df["record_count"] != "NOT FOUND"
    ]

    print()
    line()
    print("SUMMARY")
    line()

    print(f"Total expected DW tables : {len(DW_TABLES)}")
    print(f"Dimensions               : {len(DIMENSION_TABLES)}")
    print(f"Facts                    : {len(FACT_TABLES)}")

    if not existing_df.empty:
        total_records = sum(
            int(x)
            for x in existing_df["record_count"]
        )

        print(f"Total records             : {total_records:,}")


# =========================================================
# SHOW ALL DATABASE TABLES
# =========================================================

def show_all_tables():
    line()
    print("ALL TABLES IN dev.duckdb")
    line()

    df = con.execute(
        """
        SELECT
            table_schema,
            table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN (
            'information_schema',
            'pg_catalog'
        )
        ORDER BY
            table_schema,
            table_name
        """
    ).fetchdf()

    if df.empty:
        print("ไม่พบตารางในฐานข้อมูล")
        return

    print()
    print(df.to_string(index=False))


# =========================================================
# SHOW ROW COUNT
# =========================================================

def show_row_count(table_name):
    line()
    print(f"ROW COUNT: {table_name}")
    line()

    count = con.execute(
        f'SELECT COUNT(*) FROM "{table_name}"'
    ).fetchone()[0]

    print()
    print(f"{table_name}: {count:,} rows")


# =========================================================
# SHOW SCHEMA
# =========================================================

def show_schema(table_name):
    line()
    print(f"SCHEMA / METADATA: {table_name}")
    line()

    schema = con.execute(
        f"PRAGMA table_info('{table_name}')"
    ).fetchdf()

    if schema.empty:
        print("ไม่พบ schema")
        return

    columns_to_show = [
        "name",
        "type",
        "notnull",
        "pk",
    ]

    print()
    print(
        schema[
            columns_to_show
        ].to_string(index=False)
    )


# =========================================================
# SHOW SAMPLE DATA
# =========================================================

def show_sample(table_name, limit=10):
    line()
    print(f"SAMPLE DATA: {table_name}")
    line()

    df = con.execute(
        f"""
        SELECT *
        FROM "{table_name}"
        LIMIT {limit}
        """
    ).fetchdf()

    if df.empty:
        print("ไม่มีข้อมูล")
        return

    print()
    print(df.to_string(index=False))


# =========================================================
# SHOW COMPLETE TABLE DETAIL
# =========================================================

def show_table_detail(table_name):
    show_row_count(table_name)
    print()
    show_schema(table_name)
    print()
    show_sample(table_name)


# =========================================================
# TABLE SELECTOR
# =========================================================

def select_table():
    line()
    print("SELECT DATA WAREHOUSE TABLE")
    line()

    available_tables = [
        table
        for table in DW_TABLES
        if table_exists(table)
    ]

    if not available_tables:
        print("ไม่พบ Data Warehouse Tables")
        return None

    print()

    for index, table_name in enumerate(
        available_tables,
        start=1,
    ):
        table_type = (
            "Dimension"
            if table_name.startswith("dim_")
            else "Fact"
        )

        print(
            f"{index}. "
            f"{table_name} "
            f"({table_type})"
        )

    print("0. กลับเมนูหลัก")

    choice = input(
        "\nเลือกหมายเลขตาราง: "
    ).strip()

    if choice == "0":
        return None

    try:
        choice_index = int(choice) - 1

        if (
            choice_index < 0
            or choice_index >= len(available_tables)
        ):
            raise ValueError

        return available_tables[
            choice_index
        ]

    except ValueError:
        print("กรุณาเลือกหมายเลขที่ถูกต้อง")
        return None


# =========================================================
# TABLE INSPECTION MENU
# =========================================================

def inspect_table():
    table_name = select_table()

    if table_name is None:
        return

    while True:
        print()
        line()
        print(f"TABLE: {table_name}")
        line()

        print("1. ดูจำนวน Rows")
        print("2. ดู Schema / Data Types")
        print("3. ดู Sample Data")
        print("4. ดูทั้งหมด")
        print("0. กลับเมนูหลัก")

        choice = input(
            "\nเลือกเมนู: "
        ).strip()

        if choice == "1":
            show_row_count(table_name)

        elif choice == "2":
            show_schema(table_name)

        elif choice == "3":
            show_sample(table_name)

        elif choice == "4":
            show_table_detail(table_name)

        elif choice == "0":
            break

        else:
            print("กรุณาเลือกเมนูที่ถูกต้อง")
            continue

        input(
            "\nกด Enter เพื่อดำเนินการต่อ..."
        )


# =========================================================
# MAIN MENU
# =========================================================

def main():
    while True:
        print()
        line()
        print("AIRLINE DATA WAREHOUSE - QUERY DUCKDB")
        line()

        print(f"Database: {DB_PATH}")

        print()
        print("1. ดูภาพรวม Data Warehouse")
        print("2. เลือก Table เพื่อตรวจสอบ")
        print("3. ดู Table ทั้งหมดใน dev.duckdb")
        print("0. Exit")

        choice = input(
            "\nเลือกเมนู: "
        ).strip()

        if choice == "1":
            show_dw_overview()

        elif choice == "2":
            inspect_table()

        elif choice == "3":
            show_all_tables()

        elif choice == "0":
            print()
            print("ปิด Query DuckDB")
            break

        else:
            print("กรุณาเลือกเมนูที่ถูกต้อง")
            continue

        if choice != "2":
            input(
                "\nกด Enter เพื่อดำเนินการต่อ..."
            )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    try:
        main()
    finally:
        con.close()