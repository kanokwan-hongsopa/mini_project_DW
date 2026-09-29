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
| **2. 673020254-0 ธัณญ์ฌัณญา วงค์จันทร์** | Flight Staging, Cleaning, ETL |
| **3. 673020258-2 ปวริศา โง่นสูงเนิน** | Dimension Tables, OLTP ER |
| **4. 673020268-9 อนัญญา ทองปน** | Fact Tables, Analytical Queries Q1-Q8 |
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

<img width="2205" height="1661" alt="Galaxy Schema" src="https://github.com/user-attachments/assets/d980e549-26cd-4dfc-89ed-e4b6e11e1b0b" />

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

## 10. Applications

โปรเจกต์มีเครื่องมือสำหรับตรวจสอบและวิเคราะห์ Data Warehouse จำนวน **3 ส่วน**

### 10.1 Business Dashboard

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

### 10.2 Data Warehouse Explorer

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

### 10.3 DuckDB Query Tool

**ไฟล์:** `query_duckdb.py`

ใช้สำหรับ Query และตรวจสอบข้อมูลใน `dev.duckdb` ผ่าน Python / Terminal

สามารถตรวจสอบได้ เช่น

- รายชื่อ Tables
- Dimension / Fact Tables
- Row Count
- Column Count
- Schema / Data Types
- Sample Data

**รันด้วย**

```bash
python query_duckdb.py
```

### Dashboard Link

https://miniprojectdw-72b5jte8lfnerbx8jcrms7.streamlit.app/

---

## 11. Data Quality and Testing

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

## 12. How to Run the Project

### 12.1 Clone Repository

```bash
git clone https://github.com/kanokwan-hongsopa/mini_project_DW.git
cd mini_project_DW
```

### 12.2 Create Python Virtual Environment

```bash
python -m venv .venv
```

### 12.3 Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 12.4 Install Dependencies

```bash
pip install -r requirements.txt
```

### 12.5 Create dbt Profile

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

### 12.6 Load Raw Data

```bash
python scripts/load_raw.py
```

### 12.7 Run dbt Models

```bash
dbt run --profiles-dir .
```

### 12.8 Run dbt Tests

```bash
dbt test --profiles-dir .
```

### 12.9 Return to Project Root

```bash
cd ..
```

### 12.10 Run Business Dashboard

```bash
streamlit run dashboard_app.py
```

### 12.11 Run Data Warehouse Explorer

```bash
streamlit run app.py
```

### 12.12 Run DuckDB Query Tool

```bash
python query_duckdb.py
```

---

## 13. Repository Structure

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

## 14. Technologies Used

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

## 15. Conclusion

โปรเจกต์ **Airline Data Warehouse** ถูกพัฒนาขึ้นเพื่อแปลงข้อมูลสายการบินจาก Operational Data Source ให้เป็น Data Warehouse สำหรับการวิเคราะห์ข้อมูลเชิงธุรกิจ

ระบบถูกออกแบบในรูปแบบ **Galaxy Schema** ซึ่งประกอบด้วย **5 Dimension Tables** และ **3 Fact Tables** ได้แก่

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_utilization`

และสามารถรองรับ **Business Questions จำนวน 15 ข้อ** ครอบคลุมทั้งด้าน Revenue, Demand, Capacity Utilization, Booking Behavior, Fleet Usage และ Flight Operations

ข้อมูลถูกประมวลผลผ่าน **Python, DuckDB และ dbt** ก่อนนำไปวิเคราะห์ผ่าน Analytical Queries และแสดงผลด้วย Business Dashboard ที่พัฒนาด้วย **Streamlit และ Plotly**

นอกจากนี้โปรเจกต์ยังมี **Data Warehouse Explorer** และ **DuckDB Query Tool** สำหรับตรวจสอบโครงสร้าง Schema, Metadata และข้อมูลภายใน Data Warehouse

Dashboard รองรับ **Interactive Filters, Cascading Filters, Route Drill-down และ CSV Download** เพื่อช่วยสนับสนุนการวิเคราะห์และการตัดสินใจเชิงธุรกิจ

### Data Warehouse Explorer URL

https://miniprojectdw-fz7tpjqfaqjeqtcnlawq7x.streamlit.app/

### Dashboard URL

[https://miniprojectdw-72b5jte8lfnerbx8jcrms7.streamlit.app/](https://miniprojectdw-3pntnkkaea4sgwctctrzi7.streamlit.app/)

---

<img width="1152" height="1728" alt="Dashboard Screenshot" src="https://github.com/user-attachments/assets/2c6392b6-9c09-4753-b8be-797f4e2dc985" />
