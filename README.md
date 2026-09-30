# Airline Data Warehouse Project

โปรเจกต์ Data Warehouse สำหรับวิเคราะห์ข้อมูลสายการบิน โดยใช้ข้อมูลจาก Airlines Dataset และพัฒนา Data Warehouse ด้วย **dbt + DuckDB** พร้อม Interactive Dashboard และเครื่องมือสำหรับตรวจสอบ Data Warehouse ด้วย **Streamlit และ Python**

---

## 1. Project Overview

โปรเจกต์นี้มีวัตถุประสงค์เพื่อสร้าง Data Warehouse สำหรับวิเคราะห์ข้อมูลด้านสายการบิน เช่น

- รายได้จากการขายตั๋ว
- จำนวน Ticket Flight
- สนามบินต้นทางและปลายทาง
- เส้นทางบิน
- Fare Class
- รูปแบบการจองล่วงหน้า
- Aircraft Manufacturer / Model
- Flight Operations
- Flight Delay
- Seat Capacity และ Seat Utilization

ระบบถูกออกแบบตั้งแต่

**Operational Data Source → Raw Tables → Staging → Dimension / Fact → Data Warehouse → Analytical Queries → Dashboard**

---

## 2. Team Members

| Member | Responsibility |
|---|---|
| **1. 673020246-9 ชลธิชา หอมพรมมา** | Source Configuration, Booking/Ticket Staging |
| **2. 673020268-9 อนัญญา ทองปน** | Flight Staging, Cleaning, ETL |
| **3. 673020258-2 ปวริศา โง่นสูงเนิน** | Dimension Tables, OLTP ER |
| **4. 673020254-0 ธัณญ์ฌัณญา วงค์จันทร์** | Fact Tables, Analytical Queries Q1-Q8 |
| **5. 673020487-7 กนกวรรณ หงษ์โสภา** | Analytical Queries Q9-Q15, Dashboard |

---

## 3. Dataset / Domain

### Domain

**Airline / Aviation Analytics**

### Dataset

**Airlines Dataset**

ข้อมูลต้นทางประกอบด้วย **8 ตาราง**

- `aircrafts_data`
- `airports_data`
- `boarding_passes`
- `bookings`
- `flights`
- `seats`
- `ticket_flights`
- `tickets`

ข้อมูลถูกนำมาใช้สร้าง Data Warehouse สำหรับวิเคราะห์

- **Ticket Sales**
- **Flight Operations**
- **Seat Utilization**

---

## 4. Business Questions

โปรเจกต์นี้กำหนด **Business Questions ทั้งหมด 15 ข้อ** ได้แก่

1. เส้นทางใดสร้างรายได้จากการขายตั๋วสูงที่สุด?
2. Fare Class ใดสร้างรายได้สูงที่สุด และมีสัดส่วนรายได้เท่าใด?
3. รายได้จากการขายตั๋วมีแนวโน้มเปลี่ยนแปลงอย่างไรในแต่ละเดือน?
4. ภูมิภาคต้นทาง–ปลายทางคู่ใดมีความต้องการเดินทางสูงที่สุด?
5. เส้นทางใดมีอัตราการใช้ที่นั่งของผู้โดยสารจริง (`boarded_load_pct`) สูงและต่ำที่สุด?
6. เที่ยวบินใดมีช่องว่างระหว่างจำนวนตั๋วที่ขายกับจำนวนผู้โดยสารที่ขึ้นเครื่องจริงมากที่สุด?
7. ช่วงเวลาใดของวันมีจำนวนเที่ยวบินและปริมาณผู้โดยสารสูงที่สุด?
8. วันธรรมดากับวันหยุดสุดสัปดาห์มีความต้องการเดินทางแตกต่างกันอย่างไร?
9. ผู้โดยสารมักจองตั๋วล่วงหน้ากี่วัน และรูปแบบการจองล่วงหน้าแตกต่างกันอย่างไรในแต่ละ Fare Class?
10. Aircraft Manufacturer และรุ่นเครื่องบินใดถูกใช้งานกับเที่ยวบินมากที่สุด?
11. เส้นทางใดมีความล่าช้าในการออกเดินทางและถึงปลายทางเฉลี่ยสูงที่สุด?
12. ในแต่ละภูมิภาคและช่วงเวลาของวัน ช่วงใดมีความล่าช้าในการออกเดินทางเฉลี่ยสูงที่สุด?
13. ในแต่ละเส้นทาง Fare Class ใดสร้างรายได้สูง แต่มีจำนวนตั๋วขายไม่สูงตามไปด้วย?
14. ในแต่ละภูมิภาค Aircraft Manufacturer/Model ใดมีอัตราการใช้ที่นั่งจริงสูงที่สุด?
15. เส้นทางและช่วงเวลาใดมีความต้องการเดินทางสูง และมีอัตราการใช้ที่นั่งสูงอย่างต่อเนื่องเมื่อเทียบกับข้อมูลชุดนี้?

---

## 5. Data Warehouse Architecture

โครงสร้างการทำงานของระบบ

```text
Raw Airline Dataset
        ↓
Raw Tables
        ↓
Staging Models
        ↓
Dimension & Fact Models
        ↓
DuckDB Data Warehouse
        ↓
Analytical Queries
        ↓
Streamlit Applications
```

---

## 6. Data Model

โปรเจกต์นี้ใช้รูปแบบ **Galaxy Schema (Fact Constellation)** เนื่องจากมี Fact Table หลายตารางและมีการใช้ Dimension บางส่วนร่วมกัน

### Dimension Tables

- `dim_date`
- `dim_airport`
- `dim_aircraft`
- `dim_fare_class`
- `dim_flight_status`

### Fact Tables

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_utilization`

<img width="2948" height="2330" alt="Untitled Diagram drawio (1)" src="https://github.com/user-attachments/assets/bcd92561-66f8-4251-9143-1f993e1b24a5" />

---

## 7. ETL / ELT Pipeline

กระบวนการสร้าง Airline Data Warehouse ใช้แนวทาง **ETL/ELT** โดยนำข้อมูลต้นทางจากไฟล์ CSV เข้าสู่ DuckDB และใช้ dbt สำหรับ Transform ข้อมูลไปเป็น Staging, Dimension และ Fact Models

### Pipeline Overview

**CSV Source → Raw Tables → Staging Models → Dimension Tables → Fact Tables → Analytics → Dashboard**

### 7.1 Extract

ข้อมูลต้นทางประกอบด้วยไฟล์ CSV จำนวน **8 ตาราง** ได้แก่

- `aircrafts_data.csv`
- `airports_data.csv`
- `boarding_passes.csv`
- `bookings.csv`
- `flights.csv`
- `seats.csv`
- `ticket_flights.csv`
- `tickets.csv`

ข้อมูลถูกโหลดเข้าสู่ DuckDB ด้วย Python Script

`airline_dw/scripts/load_raw.py`

### 7.2 Transform

dbt ถูกใช้สำหรับทำความสะอาดและแปลงข้อมูล เช่น

- แปลง Data Type ให้เหมาะสม
- จัดการค่า NULL
- แปลงค่า `\N` เป็น NULL
- Standardize รูปแบบข้อมูล
- สร้าง Surrogate Key
- ตรวจสอบ Duplicate
- เชื่อมข้อมูลจากหลาย Source Table
- เพิ่มข้อมูล Region
- สร้าง Booking Lead Days
- สร้าง Daypart
- จำแนก Weekday / Weekend
- คำนวณ Departure Delay / Arrival Delay
- สร้าง Measure สำหรับ Seat Utilization
- สร้าง Dimension และ Fact Table ตาม Multidimensional Model

### 7.3 Load

ข้อมูลถูกโหลดตามลำดับ

1. Raw Tables
2. Staging Models
3. Dimension Tables
4. Fact Tables

โดยสร้าง **Dimension ก่อน Fact** เพื่อให้ Foreign Key สามารถเชื่อมโยงกับ Dimension ได้อย่างถูกต้อง

---

## 8. Data Warehouse Schema

Data Warehouse ประกอบด้วย **Dimension Table จำนวน 5 ตาราง** และ **Fact Table จำนวน 3 ตาราง**

### Dimension Tables

| Table | Description |
|---|---|
| `dim_date` | ข้อมูลวัน เดือน ปี และข้อมูล Weekday / Weekend |
| `dim_airport` | ข้อมูลสนามบิน เมือง ประเทศ และ Analysis Region |
| `dim_aircraft` | ข้อมูล Aircraft Code, Model, Manufacturer และ Range |
| `dim_fare_class` | ข้อมูลชั้นโดยสาร |
| `dim_flight_status` | ข้อมูลสถานะเที่ยวบิน |

### Fact Tables

| Table | Grain | Main Measures |
|---|---|---|
| `fact_ticket_sales` | 1 Ticket × 1 Flight Segment | `amount`, `ticket_flight_count`, `booking_lead_days` |
| `fact_flight_operations` | 1 Flight | `flight_count`, `boarded_count`, `departure_delay_minutes`, `arrival_delay_minutes` |
| `fact_seat_utilization` | 1 Flight | `seat_capacity`, `ticket_flight_count`, `boarded_count`, `booked_not_boarded_count`, `boarded_load_pct` |

---

## 9. Analytical Queries

โปรเจกต์มี **Analytical Queries จำนวน 15 ข้อ** โดย Query จาก Dimension และ Fact Tables ใน Data Warehouse

### Revenue & Demand Analysis

1. เส้นทางใดสร้างรายได้จากการขายตั๋วสูงที่สุด?
2. Fare Class ใดสร้างรายได้สูงที่สุด และมีสัดส่วนรายได้เท่าใด?
3. รายได้จากการขายตั๋วมีแนวโน้มเปลี่ยนแปลงอย่างไรในแต่ละเดือน?
4. ภูมิภาคต้นทาง–ปลายทางคู่ใดมีความต้องการเดินทางสูงที่สุด?

### Capacity Utilization Analysis

5. เส้นทางใดมีอัตราการใช้ที่นั่งของผู้โดยสารจริงสูงและต่ำที่สุด?
6. เที่ยวบินใดมีช่องว่างระหว่างจำนวนตั๋วที่ขายกับจำนวนผู้โดยสารที่ขึ้นเครื่องจริงมากที่สุด?

### Travel Pattern Analysis

7. ช่วงเวลาใดของวันมีจำนวนเที่ยวบินและปริมาณผู้โดยสารสูงที่สุด?
8. วันธรรมดากับวันหยุดสุดสัปดาห์มีความต้องการเดินทางแตกต่างกันอย่างไร?
9. ผู้โดยสารมักจองตั๋วล่วงหน้ากี่วัน และแตกต่างกันอย่างไรในแต่ละ Fare Class?

### Fleet & Operations Analysis

10. Aircraft Manufacturer และรุ่นเครื่องบินใดถูกใช้งานกับเที่ยวบินมากที่สุด?
11. เส้นทางใดมีความล่าช้าในการออกเดินทางและถึงปลายทางเฉลี่ยสูงที่สุด?

### Multidimensional / Challenge Analysis

12. ในแต่ละภูมิภาคและช่วงเวลาของวัน ช่วงใดมีความล่าช้าในการออกเดินทางเฉลี่ยสูงที่สุด?
13. ในแต่ละเส้นทาง Fare Class ใดสร้างรายได้สูง แต่มีจำนวนตั๋วขายไม่สูงตามไปด้วย?
14. ในแต่ละภูมิภาค Aircraft Manufacturer/Model ใดมีอัตราการใช้ที่นั่งจริงสูงที่สุด?
15. เส้นทางและช่วงเวลาใดมีทั้ง Demand และอัตราการใช้ที่นั่งสูงอย่างต่อเนื่องเมื่อเทียบกับข้อมูลชุดนี้?

Analytical Queries ใช้คำสั่ง เช่น

- `JOIN`
- `GROUP BY`
- `SUM()`
- `AVG()`
- `COUNT()`
- `MEDIAN()`
- Window Functions
- Common Table Expressions (CTE)

ไฟล์ Query อยู่ในโฟลเดอร์

`airline_dw/analyses/`

---

## 10. Query Usage Guide

ส่วนนี้อธิบายวิธีใช้งาน Query ของโปรเจกต์ Airline Data Warehouse ทั้งในรูปแบบ SQL Analysis Files และผ่าน Python Query Tool

### 10.1 Query Files Location

Analytical Queries ทั้งหมดอยู่ในโฟลเดอร์

`airline_dw/analyses/`

ประกอบด้วยไฟล์ Query ตั้งแต่ Q1–Q15 ได้แก่

- `query_01_route_revenue.sql`
- `query_02_fare_class_revenue_share.sql`
- `query_03_monthly_revenue_trend.sql`
- `query_04_region_pair_demand.sql`
- `query_05_route_boarded_load.sql`
- `query_06_booked_not_boarded_gap.sql`
- `query_07_daypart_traffic.sql`
- `query_08_weekday_weekend_demand.sql`
- `query_09_booking_lead_by_fare_class.sql`
- `query_10_aircraft_usage.sql`
- `query_11_route_delay.sql`
- `query_12_region_daypart_delay.sql`
- `query_13_route_fare_efficiency.sql`
- `query_14_region_aircraft_load.sql`
- `query_15_route_daypart_high_demand_load.sql`

### 10.2 เตรียม Environment ก่อนใช้งาน Query

เปิด Terminal แล้วเข้าโฟลเดอร์โปรเจกต์

```bash
cd mini_project_DW
```

Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

จากนั้นเข้าโฟลเดอร์ `airline_dw`

```bash
cd airline_dw
```

### 10.3 ตรวจสอบ Data Warehouse ก่อนรัน Query

ตรวจสอบการเชื่อมต่อของ dbt

```bash
dbt debug --profiles-dir .
```

สร้างหรืออัปเดต Data Warehouse Models

```bash
dbt run --profiles-dir .
```

ตรวจสอบคุณภาพข้อมูล

```bash
dbt test --profiles-dir .
```

เมื่อคำสั่งเหล่านี้ทำงานสำเร็จ จะสามารถ Query ข้อมูลจาก Dimension และ Fact Tables ใน Data Warehouse ได้

### 10.4 การใช้งาน Analytical SQL Queries

ไฟล์ SQL ในโฟลเดอร์

`airline_dw/analyses/`

ถูกออกแบบให้ตอบ Business Questions Q1–Q15 โดยแต่ละไฟล์ใช้ข้อมูลจาก Dimension และ Fact Tables ที่เกี่ยวข้อง

ตัวอย่างเช่น

- `query_01_route_revenue.sql` ใช้วิเคราะห์รายได้ตามเส้นทาง
- `query_05_route_boarded_load.sql` ใช้วิเคราะห์อัตราการใช้ที่นั่งตามเส้นทาง
- `query_09_booking_lead_by_fare_class.sql` ใช้วิเคราะห์ระยะเวลาการจองล่วงหน้าตาม Fare Class
- `query_12_region_daypart_delay.sql` ใช้วิเคราะห์ Delay ตาม Region × Daypart
- `query_14_region_aircraft_load.sql` ใช้วิเคราะห์ Seat Utilization ตาม Region × Aircraft

สามารถเปิดไฟล์ `.sql` แต่ละไฟล์เพื่อดู Logic และ SQL Query ที่ใช้ตอบ Business Question ได้โดยตรง

### 10.5 Compile Analytical Queries ด้วย dbt

สามารถใช้ `dbt compile` เพื่อตรวจสอบและ Compile SQL Analysis Files ได้ด้วยคำสั่ง

```bash
dbt compile --profiles-dir .
```

หลังจาก Compile สำเร็จ SQL ที่ผ่านการประมวลผลแล้วจะอยู่ในโฟลเดอร์

```text
target/compiled/
```

การ Compile ช่วยตรวจสอบว่า `ref()` และ Logic ที่อ้างอิง dbt Models ถูกแปลงเป็น SQL ที่สามารถนำไปใช้งานกับ Data Warehouse ได้

### 10.6 การ Query ผ่าน Python

โปรเจกต์มีไฟล์

`query_duckdb.py`

อยู่ที่ Root ของ Repository

ใช้สำหรับ Query และตรวจสอบข้อมูลใน DuckDB ผ่าน Terminal โดยไม่จำเป็นต้องเปิด Dashboard

ก่อนรันให้กลับไปที่ Root ของโปรเจกต์

```bash
cd ..
```

จากนั้นรัน

```bash
python query_duckdb.py
```

โปรแกรมสามารถใช้ตรวจสอบข้อมูล เช่น

- รายชื่อ Tables ใน Data Warehouse
- จำนวน Dimension Tables
- จำนวน Fact Tables
- จำนวน Records
- จำนวน Columns
- Schema
- Data Types
- Sample Data

### 10.7 ตัวอย่างการใช้งาน `query_duckdb.py`

เมื่อรัน

```bash
python query_duckdb.py
```

โปรแกรมจะแสดงเมนูสำหรับเลือกดูข้อมูล

```text
1. Database Overview
2. Explore Table
3. List All Tables
```

#### ตัวเลือก 1: Database Overview

ใช้สำหรับดูภาพรวมของ Data Warehouse เช่น

- จำนวน Tables
- จำนวน Dimension Tables
- จำนวน Fact Tables
- จำนวน Records
- จำนวน Columns

#### ตัวเลือก 2: Explore Table

ใช้สำหรับเลือก Table ที่ต้องการตรวจสอบ เช่น

```text
dim_date
dim_airport
dim_aircraft
dim_fare_class
dim_flight_status
fact_ticket_sales
fact_flight_operations
fact_seat_utilization
```

หลังจากเลือก Table สามารถดูข้อมูล เช่น

- Row Count
- Schema
- Data Types
- Sample Rows
- ข้อมูลภายใน Table

#### ตัวเลือก 3: List All Tables

ใช้สำหรับแสดงรายชื่อ Tables ทั้งหมดที่มีอยู่ใน Data Warehouse

### 10.8 ตัวอย่าง SQL Query

ตัวอย่างการ Query รายได้ตาม Fare Class

```sql
SELECT
    fare_class_key,
    SUM(amount) AS total_revenue
FROM fact_ticket_sales
GROUP BY fare_class_key
ORDER BY total_revenue DESC;
```

ตัวอย่างการ Query จำนวนเที่ยวบินตามสถานะ

```sql
SELECT
    status_key,
    COUNT(*) AS total_flights
FROM fact_flight_operations
GROUP BY status_key
ORDER BY total_flights DESC;
```

ตัวอย่างการ Query อัตราการใช้ที่นั่ง

```sql
SELECT
    departure_airport_key,
    arrival_airport_key,
    SUM(boarded_count) AS boarded_count,
    SUM(seat_capacity) AS seat_capacity,
    ROUND(
        100.0 * SUM(boarded_count) / NULLIF(SUM(seat_capacity), 0),
        2
    ) AS boarded_load_pct
FROM fact_seat_utilization
GROUP BY
    departure_airport_key,
    arrival_airport_key
ORDER BY boarded_load_pct DESC;
```

### 10.9 Mapping Query กับ Business Questions

| Query File | Business Question |
|---|---|
| `query_01_route_revenue.sql` | เส้นทางที่สร้างรายได้สูงที่สุด |
| `query_02_fare_class_revenue_share.sql` | รายได้และสัดส่วนรายได้ตาม Fare Class |
| `query_03_monthly_revenue_trend.sql` | แนวโน้มรายได้รายเดือน |
| `query_04_region_pair_demand.sql` | Demand ตามคู่ภูมิภาคต้นทาง–ปลายทาง |
| `query_05_route_boarded_load.sql` | อัตราการใช้ที่นั่งตามเส้นทาง |
| `query_06_booked_not_boarded_gap.sql` | ช่องว่างระหว่าง Ticket กับ Boarded |
| `query_07_daypart_traffic.sql` | Traffic ตามช่วงเวลาของวัน |
| `query_08_weekday_weekend_demand.sql` | Weekday vs Weekend Demand |
| `query_09_booking_lead_by_fare_class.sql` | Booking Lead Time ตาม Fare Class |
| `query_10_aircraft_usage.sql` | Aircraft Usage |
| `query_11_route_delay.sql` | Delay ตามเส้นทาง |
| `query_12_region_daypart_delay.sql` | Delay ตาม Region × Daypart |
| `query_13_route_fare_efficiency.sql` | Route × Fare Class Revenue Efficiency |
| `query_14_region_aircraft_load.sql` | Region × Aircraft Seat Utilization |
| `query_15_route_daypart_high_demand_load.sql` | Route × Daypart High Demand and Load |

### 10.10 สรุปการใช้งาน Query

Query ของโปรเจกต์สามารถใช้งานได้ 2 รูปแบบหลัก

1. **SQL Analytical Queries**
   - อยู่ใน `airline_dw/analyses/`
   - ใช้ตอบ Business Questions Q1–Q15
   - สามารถ Compile ผ่าน dbt ได้

2. **Python DuckDB Query Tool**
   - ใช้ไฟล์ `query_duckdb.py`
   - ใช้ตรวจสอบ Database, Schema, Records และ Sample Data
   - เหมาะสำหรับตรวจสอบ Data Warehouse ผ่าน Terminal

ทั้งสองวิธีใช้ข้อมูลจาก Dimension และ Fact Tables ที่สร้างด้วย dbt

---

## 11. Applications

โปรเจกต์มีเครื่องมือสำหรับตรวจสอบและวิเคราะห์ Data Warehouse จำนวน **3 ส่วน**

### 11.1 Business Dashboard

**ไฟล์:** `dashboard_app.py`

ใช้สำหรับวิเคราะห์ **Business Questions Q1–Q15** และนำเสนอข้อมูลในรูปแบบ Interactive Dashboard

Dashboard พัฒนาด้วย

- Streamlit
- Plotly
- pandas
- DuckDB

#### Dashboard Features

- KPI Summary
- Revenue & Demand Analysis
- Capacity Utilization Analysis
- Travel Pattern Analysis
- Fleet & Operations Analysis
- Multidimensional Analysis
- Date Range Filter
- Departure Airport Filter
- Arrival Airport Filter
- Fare Class Filter
- Aircraft Model Filter
- Cascading Filters
- Route Drill-down
- CSV Download

**รันด้วย**

```bash
streamlit run dashboard_app.py
```

### 11.2 Data Warehouse Explorer

**ไฟล์:** `app.py`

ใช้สำหรับตรวจสอบโครงสร้างและข้อมูลภายใน Data Warehouse

#### Features

- Table Browser
- Database Schema Overview
- Dimension / Fact Tables
- Row Count
- Column Count
- Metadata / Data Types
- Sample Data
- Column Quality Check

**รันด้วย**

```bash
streamlit run app.py
```

### 11.3 DuckDB Query Tool

**ไฟล์:** `query_duckdb.py`

ใช้สำหรับ Query และตรวจสอบข้อมูลใน `dev.duckdb` ผ่าน Python / Terminal

**รันด้วย**

```bash
python query_duckdb.py
```

### Dashboard Link

[https://miniprojectdw-72b5jte8lfnerbx8jcrms7.streamlit.app/](https://miniprojectdw-3pntnkkaea4sgwctctrzi7.streamlit.app/)

---

## 12. Data Quality and Testing

โปรเจกต์ใช้ **dbt tests** เพื่อตรวจสอบคุณภาพข้อมูล

ตัวอย่างการตรวจสอบ ได้แก่

- `not_null`
- `unique`
- `relationships`
- `accepted_values`

สามารถสร้าง Data Warehouse Models ด้วย

```bash
dbt run --profiles-dir .
```

และตรวจสอบคุณภาพข้อมูลด้วย

```bash
dbt test --profiles-dir .
```

นอกจากนี้ยังพบ Data Quality Issue บางส่วน เช่น ค่า `booking_lead_days` ติดลบ ซึ่งควรพิจารณาอย่างระมัดระวังในการตีความผลการวิเคราะห์

---

## 13. How to Run the Project

### 13.1 Clone Repository

```bash
git clone https://github.com/kanokwan-hongsopa/mini_project_DW.git
cd mini_project_DW
```

### 13.2 Create Python Virtual Environment

```bash
python -m venv .venv
```

### 13.3 Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 13.4 Install Dependencies

```bash
pip install -r requirements.txt
```

### 13.5 Create dbt Profile

เข้าไปที่โฟลเดอร์

```bash
cd airline_dw
```

สร้างไฟล์ `profiles.yml` ภายในโฟลเดอร์ `airline_dw`

```yaml
airline_dw:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: dev.duckdb
      threads: 4
```

ตรวจสอบการเชื่อมต่อด้วย

```bash
dbt debug --profiles-dir .
```

### 13.6 Load Raw Data

```bash
python scripts/load_raw.py
```

### 13.7 Run dbt Models

```bash
dbt run --profiles-dir .
```

### 13.8 Run dbt Tests

```bash
dbt test --profiles-dir .
```

### 13.9 Return to Project Root

```bash
cd ..
```

### 13.10 Run Business Dashboard

```bash
streamlit run dashboard_app.py
```

### 13.11 Run Data Warehouse Explorer

```bash
streamlit run app.py
```

### 13.12 Run DuckDB Query Tool

```bash
python query_duckdb.py
```

---

## 14. Repository Structure

โครงสร้างหลักของ Repository

```text
mini_project_DW/
│
├── README.md
├── requirements.txt
├── app.py
├── dashboard_app.py
├── query_duckdb.py
│
└── airline_dw/
    │
    ├── dbt_project.yml
    ├── dev.duckdb
    │
    ├── datasets/
    │   ├── aircrafts_data.csv
    │   ├── airports_data.csv
    │   ├── boarding_passes.csv
    │   ├── bookings.csv
    │   ├── flights.csv
    │   ├── seats.csv
    │   ├── ticket_flights.csv
    │   └── tickets.csv
    │
    ├── analyses/
    │   ├── query_01_route_revenue.sql
    │   ├── query_02_fare_class_revenue_share.sql
    │   ├── query_03_monthly_revenue_trend.sql
    │   ├── ...
    │   └── query_15_route_daypart_high_demand_load.sql
    │
    ├── models/
    │   ├── staging/
    │   └── datawarehouse/
    │
    ├── scripts/
    │   └── load_raw.py
    │
    └── docs/
        ├── 01_OLTP_ER_Diagram.md
        ├── 02_data_dictionary.md
        ├── 03_business_questions.md
        ├── 04_multidimensional_model.md
        ├── 05_business_insights.md
        ├── 06_etl_pipeline_and_transformations.md
        └── 07_dashboard_documentation.md
```

---

## 15. Technologies Used

- **Python**
- **dbt**
- **DuckDB**
- **SQL**
- **Streamlit**
- **Plotly**
- **pandas**
- **Git**
- **GitHub**

---

## 16. Conclusion

โปรเจกต์ **Airline Data Warehouse** ถูกพัฒนาขึ้นเพื่อแปลงข้อมูลสายการบินจาก Operational Data Source ให้เป็น Data Warehouse สำหรับการวิเคราะห์ข้อมูลเชิงธุรกิจ

ระบบถูกออกแบบในรูปแบบ **Galaxy Schema** ซึ่งประกอบด้วย **5 Dimension Tables** และ **3 Fact Tables** ได้แก่

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_utilization`

และสามารถรองรับ **Business Questions จำนวน 15 ข้อ** ครอบคลุมทั้งด้าน Revenue, Demand, Capacity Utilization, Booking Behavior, Fleet Usage และ Flight Operations

ข้อมูลถูกประมวลผลผ่าน **Python, DuckDB และ dbt** ก่อนนำไปวิเคราะห์ผ่าน Analytical Queries และแสดงผลด้วย Business Dashboard ที่พัฒนาด้วย **Streamlit และ Plotly**

นอกจากนี้โปรเจกต์ยังมี **Data Warehouse Explorer** และ **DuckDB Query Tool** สำหรับตรวจสอบโครงสร้าง Schema, Metadata และข้อมูลภายใน Data Warehouse

Dashboard รองรับ **Interactive Filters, Cascading Filters, Route Drill-down และ CSV Download** เพื่อช่วยสนับสนุนการวิเคราะห์และการตัดสินใจเชิงธุรกิจ

### Dashboard URL

[https://miniprojectdw-72b5jte8lfnerbx8jcrms7.streamlit.app/](https://miniprojectdw-3pntnkkaea4sgwctctrzi7.streamlit.app/)

### DW Explorer URL

https://miniprojectdw-fz7tpjqfaqjeqtcnlawq7x.streamlit.app/

---

<img width="1024" height="1536" alt="27612" src="https://github.com/user-attachments/assets/0bf0df64-6c27-48a3-a8af-93ff22d2ce6b" />
