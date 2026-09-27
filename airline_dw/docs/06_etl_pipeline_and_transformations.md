# 06 กระบวนการ ETL Pipeline และการแปลงข้อมูล

## 1. ภาพรวม (Overview)

โครงการนี้ใช้กระบวนการในรูปแบบ ELT เพื่อจัดการข้อมูลการดำเนินงานของสายการบิน โดยนำข้อมูลจากไฟล์ CSV เข้าสู่ฐานข้อมูล DuckDB และใช้ dbt ในการทำความสะอาด แปลงชนิดข้อมูล และจัดเตรียมข้อมูลให้อยู่ในรูปแบบที่เหมาะสมสำหรับการสร้าง Data Warehouse และการวิเคราะห์ข้อมูล

กระบวนการทำงานของข้อมูลมีลำดับดังนี้:

CSV Source Files  
→ DuckDB Raw Schema  
→ dbt Staging Models  
→ Dimension Tables  
→ Fact Tables  
→ Data Warehouse  
→ Dashboard

## 2. การดึงและนำเข้าข้อมูล (Extract)

ข้อมูลต้นทางประกอบด้วยไฟล์ CSV จำนวน 8 ไฟล์ ได้แก่:

- `aircrafts_data.csv`
- `airports_data.csv`
- `boarding_passes.csv`
- `bookings.csv`
- `flights.csv`
- `seats.csv`
- `ticket_flights.csv`
- `tickets.csv`

Dataset ที่ใช้เป็น Enriched Dataset ซึ่งยังคงจำนวน Records เท่ากับข้อมูลต้นฉบับ แต่เพิ่มคอลัมน์ที่ได้จากการ derive หรือ join ข้อมูลเดิม เพื่อรองรับการวิเคราะห์ เช่น Manufacturer, Region, Duration, Delay, Local Time, Daypart, Weekend, Seat Capacity, Load Percentage และ Booking Lead Days

โปรเจกต์ใช้ Python script `scripts/load_raw.py` สำหรับโหลดไฟล์ CSV ทั้ง 8 ไฟล์เข้าสู่ `raw` schema ภายในฐานข้อมูล `dev.duckdb`

ข้อมูลต้นทางถูกโหลดเป็นชนิด `VARCHAR` โดยใช้:

`read_csv_auto(..., all_varchar=true)`

เพื่อรักษาค่าของข้อมูลต้นทางไว้ก่อน แล้วจึงแปลงชนิดข้อมูลใน Staging Layer ด้วย dbt

## 3. ชั้นข้อมูลดิบ (Raw Data Layer)

Raw Layer ประกอบด้วย 8 ตาราง ได้แก่:

- `raw.aircrafts_data`
- `raw.airports_data`
- `raw.boarding_passes`
- `raw.bookings`
- `raw.flights`
- `raw.seats`
- `raw.ticket_flights`
- `raw.tickets`

ข้อมูลในชั้นนี้ทำหน้าที่เป็นข้อมูลต้นทางสำหรับ Staging Models โดยยังไม่มีการนำ Business Logic ของ Data Warehouse มาใช้

## 4. การแปลงข้อมูลใน Staging Layer

Staging Layer ประกอบด้วย 8 Models โดยใช้สำหรับทำความสะอาดข้อมูล แปลงชนิดข้อมูล และปรับรูปแบบข้อมูลให้เป็นมาตรฐานก่อนนำไปสร้าง Dimension และ Fact Tables

### 4.1 `stg_bookings`

การแปลงข้อมูลประกอบด้วย:

- แปลง `book_date` เป็น `TIMESTAMP`
- แปลง `total_amount` เป็น `DECIMAL`
- เพิ่มข้อมูลสำหรับการวิเคราะห์วันที่ ได้แก่ `book_date_key`, `book_day_name`, `book_is_weekend` และ `book_day_type`

### 4.2 `stg_tickets`

การแปลงข้อมูลประกอบด้วย:

- จัดรูปแบบ `ticket_no`, `book_ref` และ `passenger_id`
- แปลง `book_date` เป็น `TIMESTAMP`
- รองรับ `book_date_key` และ `book_day_type`
- รักษาความสัมพันธ์ระหว่าง Ticket และ Booking ผ่าน `book_ref`

### 4.3 `stg_ticket_flights`

การแปลงข้อมูลประกอบด้วย:

- แปลง `flight_id` เป็น `INTEGER`
- แปลง `amount` เป็น `DECIMAL`
- ทำความสะอาดข้อมูล `fare_conditions`
- รองรับข้อมูล Booking และ Flight Date
- รองรับ `booking_lead_days`
- เพิ่มข้อมูลสนามบินและภูมิภาคต้นทาง–ปลายทาง
- เพิ่มข้อมูลรุ่นและผู้ผลิตเครื่องบิน
- รองรับ `scheduled_duration_minutes`

### 4.4 `stg_aircrafts`

การแปลงข้อมูลประกอบด้วย:

- ปรับ `aircraft_code` ให้เป็นตัวอักษรพิมพ์ใหญ่
- ทำความสะอาดชื่อรุ่นเครื่องบิน
- แปลง `range` เป็น `INTEGER`
- รองรับข้อมูล `manufacturer`

### 4.5 `stg_airports`

การแปลงข้อมูลประกอบด้วย:

- ปรับ `airport_code` ให้เป็นตัวอักษรพิมพ์ใหญ่
- ทำความสะอาดชื่อสนามบิน เมือง และข้อมูลข้อความ
- รองรับ `country`
- รองรับ `analysis_region` สำหรับการวิเคราะห์ข้อมูลตามภูมิภาค

### 4.6 `stg_flights`

การแปลงข้อมูลประกอบด้วย:

- แปลง `flight_id` เป็น `INTEGER`
- แปลง Scheduled และ Actual Timestamp ให้เป็นชนิดข้อมูลวันและเวลาที่เหมาะสม
- ปรับรหัสสนามบินและรหัสเครื่องบินให้เป็นมาตรฐาน
- รองรับข้อมูลภูมิภาคต้นทางและปลายทาง
- รองรับ Aircraft Model และ Manufacturer
- แปลง Scheduled Duration และ Actual Duration
- รองรับ Departure Delay และ Arrival Delay
- รองรับตัวแปรระบุเที่ยวบินหรือความล่าช้ามากกว่า 2 ชั่วโมง
- รองรับเวลาท้องถิ่นของเที่ยวบิน
- รองรับ `departure_local_hour` และ `departure_daypart`
- รองรับการวิเคราะห์วันธรรมดาและวันหยุดสุดสัปดาห์
- รองรับ `seat_capacity`
- รองรับ `ticket_flight_count` และ `boarded_count`
- รองรับ `ticketed_load_pct` และ `boarded_load_pct`

ข้อมูล Actual Departure, Actual Arrival, Duration หรือ Delay บางรายการสามารถเป็น NULL ได้ตามสถานะของเที่ยวบิน จึงใช้ `TRY_CAST` เพื่อรองรับข้อมูลดังกล่าว

### 4.7 `stg_seats`

การแปลงข้อมูลประกอบด้วย:

- ปรับ `aircraft_code` และ `seat_no` ให้เป็นมาตรฐาน
- ทำความสะอาด `fare_conditions`
- รองรับ `aircraft_model`
- รองรับ `manufacturer`
- แปลง `total_seat_capacity` เป็น `INTEGER`

### 4.8 `stg_boarding_passes`

การแปลงข้อมูลประกอบด้วย:

- แปลง `flight_id` และ `boarding_no` เป็น `INTEGER`
- ปรับ `seat_no` ให้เป็นมาตรฐาน
- รองรับสนามบินต้นทางและปลายทาง
- รองรับภูมิภาคต้นทางและปลายทาง
- รองรับ Aircraft Code, Aircraft Model และ Manufacturer
- แปลง `seat_capacity` เป็น `INTEGER`

## 5. การตรวจสอบคุณภาพข้อมูล (Data Quality Validation)

โปรเจกต์ใช้ dbt tests สำหรับตรวจสอบคุณภาพของข้อมูลใน Staging Layer ได้แก่:

- `not_null` สำหรับตรวจสอบคอลัมน์สำคัญที่ไม่ควรเป็น NULL
- `unique` สำหรับตรวจสอบ Business Key ที่ต้องไม่ซ้ำ
- `relationships` สำหรับตรวจสอบ Referential Integrity ระหว่าง Models
- `accepted_values` สำหรับตรวจสอบค่าของ Flight Status และ Fare Conditions

ตัวอย่างความสัมพันธ์ที่ตรวจสอบ ได้แก่:

- Tickets → Bookings ผ่าน `book_ref`
- Ticket Flights → Tickets ผ่าน `ticket_no`
- Ticket Flights → Flights ผ่าน `flight_id`
- Flights → Airports ผ่าน Departure และ Arrival Airport
- Flights → Aircrafts ผ่าน `aircraft_code`
- Seats → Aircrafts ผ่าน `aircraft_code`
- Boarding Passes → Flights ผ่าน `flight_id`

หลังจากปรับ Staging Models และ Tests ให้รองรับ Enriched Dataset แล้ว ผลการทดสอบ Staging Layer คือ:

`PASS=90 WARN=0 ERROR=0 TOTAL=90`

แสดงว่า Tests ทั้ง 90 รายการผ่านทั้งหมด

## 6. กระบวนการโหลดข้อมูล (Load Process)

หลังจากข้อมูลผ่านการทำความสะอาดและตรวจสอบคุณภาพใน Staging Layer แล้ว จะถูกนำไปใช้ในการสร้าง Dimension Tables และ Fact Tables

ลำดับการทำงานคือ:

Raw  
→ Staging  
→ Dimensions  
→ Facts  
→ Analytics / Dashboard

การแยกข้อมูลเป็น Staging, Dimensions และ Facts ช่วยให้โครงสร้าง Data Warehouse สามารถรองรับการวิเคราะห์ตาม Business Questions ได้อย่างเป็นระบบ

## 7. คำสั่งสำหรับตรวจสอบ Pipeline

คำสั่งที่ใช้ในกระบวนการ ได้แก่:

```bash
python scripts/load_raw.py
dbt debug --profiles-dir .
dbt run --select path:models/staging --profiles-dir .
dbt test --select path:models/staging --profiles-dir .

## 8. แผนภาพกระบวนการ ELT Pipeline

```mermaid
flowchart LR
    A[CSV Source Files] --> B[Python load_raw.py]
    B --> C[DuckDB Raw Schema]
    C --> D[dbt Staging - 8 Models]
    D --> E[Dimension Tables]
    E --> F[Fact Tables]
    F --> G[Data Warehouse]
    G --> H[Interactive Dashboard]