# Airline Data Warehouse Project

โปรเจกต์ Data Warehouse สำหรับวิเคราะห์ข้อมูลสายการบิน โดยใช้ข้อมูลจาก Airlines Dataset และพัฒนา Data Warehouse ด้วย dbt + DuckDB พร้อม Interactive Dashboard ด้วย Streamlit

---

## 1. Project Overview

โปรเจกต์นี้มีวัตถุประสงค์เพื่อสร้าง Data Warehouse สำหรับวิเคราะห์ข้อมูลด้านสายการบิน เช่น

- ยอดขายตั๋ว
- จำนวน Ticket Flight
- สนามบินต้นทางและปลายทาง
- เส้นทางบิน
- Fare Class
- Aircraft
- Flight Status
- Flight Delay

ระบบถูกออกแบบตั้งแต่ Operational Database → Staging → Dimension / Fact → Data Warehouse → Dashboard

---

## 2. Team Members

| Member | Responsibility |
|------|------|
| 1. 673020246-9 ชลธิชา หอมพรมมา| Source Configuration, Booking/Ticket Staging, OLTP ER |
| 2. 673020254-0 ธัณญ์ฌัณญา วงค์จันทร์ | Flight Staging, Cleaning, ETL |
| 3. 673020258-2 ปวริศา โง่นสูงเนิน | Dimension Tables |
| 4. 673020268-9 อนัญญา ทองปน| Fact Tables, Analytical Queries Q1-Q8 |
| 5. 673020487-7 กนกวรรณ หงษ์โสภา | Analytical Queries Q9-Q15, Dashboard |

---

## 3. Dataset / Domain

### Domain

Airline / Aviation Analytics

### Dataset

Airlines Dataset

ข้อมูลต้นทางประกอบด้วย 8 ตาราง

- aircrafts_data
- airports_data
- boarding_passes
- bookings
- flights
- seats
- ticket_flights
- tickets

ข้อมูลถูกนำมาใช้สร้าง Data Warehouse สำหรับวิเคราะห์ Ticket Sales, Flight Operations และ Seat Inventory

---

## 4. Business Questions

โปรเจกต์นี้กำหนด Business Questions ทั้งหมด 15 ข้อ ได้แก่

1. ยอดขายตั๋วรวมเป็นเท่าใด?
2. จำนวน Ticket Flight ทั้งหมดเท่าใด?
3. Fare Class ใดสร้างยอดขายสูงที่สุด?
4. Fare Class ใดมีจำนวนตั๋วมากที่สุด?
5. ยอดขายตั๋วเปลี่ยนแปลงอย่างไรตามช่วงเวลา?
6. สนามบินต้นทางใดมีจำนวน Ticket Flight มากที่สุด?
7. สนามบินปลายทางใดมีจำนวน Ticket Flight มากที่สุด?
8. เส้นทางต้นทาง–ปลายทางใดมีจำนวน Ticket Flight มากที่สุด?
9. เส้นทางใดสร้างยอดขายตั๋วสูงที่สุด?
10. Aircraft model ใดถูกใช้กับเที่ยวบินมากที่สุด?
11. Aircraft model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด?
12. Aircraft model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร?
13. Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด?
14. สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด?
15. ในแต่ละช่วงเวลา เส้นทางต้นทาง–ปลายทางและ Fare Class ใดสร้างยอดขายตั๋วสูงที่สุด?

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
Streamlit Dashboard
```
---

## 6. Data Model

โปรเจกต์นี้ใช้รูปแบบ **Galaxy Schema (Fact Constellation)**

### Dimension Tables

- `dim_date`
- `dim_airport`
- `dim_aircraft`
- `dim_fare_class`
- `dim_flight_status`

### Fact Tables

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_inventory`

![Galaxy Schema](airline_dw/docs/galaxy_schema.png)
<img width="2205" height="1661" alt="Untitled Diagram drawio (25)" src="https://github.com/user-attachments/assets/d980e549-26cd-4dfc-89ed-e4b6e11e1b0b" />

---

---

## 7. ETL / ELT Pipeline

กระบวนการสร้าง Airline Data Warehouse ใช้แนวทาง ETL/ELT โดยนำข้อมูลต้นทางจากไฟล์ CSV เข้าสู่ DuckDB และใช้ dbt สำหรับ Transform ข้อมูลไปเป็น Staging, Dimension และ Fact Models

### Pipeline Overview

**CSV Source → Raw Tables → Staging Models → Dimension Tables → Fact Tables → Analytics → Dashboard**

### 7.1 Extract

ข้อมูลต้นทางประกอบด้วยไฟล์ CSV จำนวน 8 ตาราง ได้แก่

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
- สร้าง Dimension และ Fact Table ตาม Multidimensional Model

### 7.3 Load

ข้อมูลถูกโหลดตามลำดับ

1. Raw Tables
2. Staging Models
3. Dimension Tables
4. Fact Tables

โดยสร้าง Dimension ก่อน Fact เพื่อให้ Foreign Key สามารถเชื่อมโยงกับ Dimension ได้อย่างถูกต้อง

---

## 8. Data Warehouse Schema

Data Warehouse ประกอบด้วย Dimension Table จำนวน 5 ตาราง และ Fact Table จำนวน 3 ตาราง

### Dimension Tables

| Table | Description |
|---|---|
| `dim_date` | ข้อมูลวัน เดือน ไตรมาส และปี |
| `dim_airport` | ข้อมูลสนามบิน |
| `dim_aircraft` | ข้อมูลรุ่นเครื่องบิน |
| `dim_fare_class` | ข้อมูลชั้นโดยสาร |
| `dim_flight_status` | ข้อมูลสถานะเที่ยวบิน |

### Fact Tables

| Table | Grain | Main Measures |
|---|---|---|
| `fact_ticket_sales` | 1 Ticket × 1 Flight Segment | `amount`, `ticket_flight_count` |
| `fact_flight_operations` | 1 Flight | `flight_count`, `departure_delay_minutes`, `arrival_delay_minutes` |
| `fact_seat_inventory` | 1 Aircraft × 1 Fare Class | `seat_count` |

---

## 9. Analytical Queries

โปรเจกต์มี Business Questions จำนวน 15 ข้อ และมี Analytical Queries สำหรับวิเคราะห์ข้อมูลจาก Data Warehouse

### Sales Analysis

1. ยอดขายตั๋วรวมเป็นเท่าใด
2. จำนวน Ticket Flight ทั้งหมดเท่าใด
3. Fare Class ใดสร้างยอดขายสูงที่สุด
4. Fare Class ใดมีจำนวน Ticket Flight มากที่สุด
5. ยอดขายตั๋วเปลี่ยนแปลงอย่างไรตามช่วงเวลา

### Airport and Route Analysis

6. สนามบินต้นทางใดมีจำนวน Ticket Flight มากที่สุด
7. สนามบินปลายทางใดมีจำนวน Ticket Flight มากที่สุด
8. เส้นทางต้นทาง–ปลายทางใดมีจำนวน Ticket Flight มากที่สุด
9. เส้นทางใดสร้างยอดขายตั๋วสูงที่สุด

### Aircraft Analysis

10. Aircraft Model ใดถูกใช้กับเที่ยวบินมากที่สุด
11. Aircraft Model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด
12. Aircraft Model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร

### Flight Operations Analysis

13. Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด
14. สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด

### Multidimensional Analysis

15. ในแต่ละช่วงเวลา เส้นทางต้นทาง–ปลายทางและ Fare Class ใดสร้างยอดขายตั๋วสูงที่สุด

Analytical Queries ใช้คำสั่ง เช่น

- `JOIN`
- `GROUP BY`
- `SUM()`
- `AVG()`
- `COUNT()`
- Window Functions

ไฟล์ Query อยู่ในโฟลเดอร์

`airline_dw/analyses/`

---

## 10. Interactive Dashboard

โปรเจกต์มี Interactive Dashboard สำหรับแสดงผลและวิเคราะห์ข้อมูลจาก Data Warehouse

Dashboard พัฒนาด้วย

- Streamlit
- Plotly
- pandas
- DuckDB

Dashboard เชื่อมต่อกับ DuckDB Data Warehouse โดยตรง

### Dashboard Features

- KPI Summary
- Total Ticket Sales
- Total Ticket Flights
- Total Flights
- Average Departure Delay
- Sales by Fare Class
- Sales Trend
- Departure Airport Analysis
- Arrival Airport Analysis
- Route Analysis
- Aircraft Usage Analysis
- Seat Capacity Analysis
- Flight Status Analysis
- Delay Analysis
- Multidimensional Analysis
- Date Range Filter
- Cascading Filters
- Route Drill-down
- CSV Download

### Dashboard Filters

ผู้ใช้สามารถกรองข้อมูลด้วย

- Date Range
- Departure Airport
- Arrival Airport
- Fare Class
- Aircraft Model

ตัวกรองถูกออกแบบเป็น Cascading Filters โดยตัวเลือกจะเปลี่ยนตามข้อมูลที่มีอยู่จริง

### Dashboard Screenshot

ใส่ Screenshot Dashboard ที่นี่

```text
airline_dw/app.py
```

### Dashboard Link

ใส่ลิงก์ Dashboard ที่นี่เมื่อ Deploy แล้ว

`Dashboard URL: <ใส่ลิงก์ที่นี่>`

---

## 11. Data Quality and Testing

โปรเจกต์ใช้ dbt tests เพื่อตรวจสอบคุณภาพข้อมูล

ตัวอย่างการตรวจสอบ ได้แก่

- `not_null`
- `unique`
- `relationships`
- `accepted_values`

สามารถรันการตรวจสอบด้วยคำสั่ง

```bash
dbt test
```

และสร้าง Data Warehouse Models ด้วย

```bash
dbt run
```

---

## 12. How to Run the Project

### 12.1 Clone Repository

```bash
git clone <repository-url>
cd mini_project_DW
```

### 12.2 Create Python Virtual Environment

```bash
python -m venv .venv
```

Activate environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 12.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 12.4 Load Raw Data

```bash
cd airline_dw
python scripts/load_raw.py
```

### 12.5 Run dbt Models

```bash
dbt run
```

### 12.6 Run dbt Tests

```bash
dbt test
```

### 12.7 Run Dashboard

```bash
streamlit run app.py
```

---

## 13. Repository Structure

โครงสร้างหลักของ Repository

```text
mini_project_DW/
│
├── README.md
├── requirements.txt
│
└── airline_dw/
    │
    ├── app.py
    ├── dbt_project.yml
    │
    ├── analyses/
    │   ├── query_01...
    │   ├── ...
    │   └── query_15...
    │
    ├── models/
    │   ├── staging/
    │   └── datawarehouse/
    │
    ├── scripts/
    │   └── load_raw.py
    │
    └── docs/
        ├── OLTP ER Diagram
        ├── Multidimensional Model Documentation
        ├── Galaxy Schema
        └── Dashboard Documentation
```

---

## 14. Technologies Used

- Python
- dbt
- DuckDB
- SQL
- Streamlit
- Plotly
- pandas
- Git
- GitHub

---

## 15. Conclusion

โปรเจกต์ Airline Data Warehouse ถูกพัฒนาขึ้นเพื่อแปลงข้อมูลสายการบินจาก Operational Data Source ให้เป็น Data Warehouse สำหรับการวิเคราะห์ข้อมูล

ระบบถูกออกแบบในรูปแบบ Galaxy Schema ซึ่งประกอบด้วย 5 Dimension Tables และ 3 Fact Tables และสามารถรองรับ Business Questions จำนวน 15 ข้อ

ข้อมูลถูกประมวลผลผ่าน Python, DuckDB และ dbt ก่อนนำไปวิเคราะห์และแสดงผลผ่าน Interactive Dashboard ที่พัฒนาด้วย Streamlit และ Plotly

Dashboard รองรับการกรองข้อมูล การ Drill-down และการวิเคราะห์ข้อมูลหลายมิติ ทำให้สามารถนำข้อมูลใน Data Warehouse ไปใช้เพื่อสนับสนุนการวิเคราะห์เชิงธุรกิจได้

Dashboard URL:  https://miniprojectdw-72b5jte8lfnerbx8jcrms7.streamlit.app/

---

<img width="1152" height="1728" alt="ดีไซน์ที่ยังไม่ได้ตั้งชื่อ" src="https://github.com/user-attachments/assets/2c6392b6-9c09-4753-b8be-797f4e2dc985" />

