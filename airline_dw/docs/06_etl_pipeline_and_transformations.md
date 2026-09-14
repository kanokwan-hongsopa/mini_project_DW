# 06 กระบวนการ ETL Pipeline และการแปลงข้อมูล

## 1. ภาพรวม (Overview)

โครงการนี้ใช้กระบวนการในรูปแบบ ELT เพื่อจัดการข้อมูลการดำเนินงานของสายการบิน โดยนำข้อมูลจากไฟล์ CSV เข้าสู่ฐานข้อมูล DuckDB และใช้ dbt ในการแปลงและจัดเตรียมข้อมูลดิบให้อยู่ในรูปแบบที่เหมาะสมสำหรับการสร้าง Data Warehouse และการวิเคราะห์ข้อมูล

กระบวนการทำงานของข้อมูล (Pipeline) มีลำดับดังนี้:

CSV Source Files  
→ DuckDB Raw Schema  
→ dbt Staging Models  
→ Dimension Tables  
→ Fact Tables  
→ Data Warehouse  
→ Dashboard


## 2. การดึงและนำเข้าข้อมูล (Extract)

ข้อมูลต้นทางประกอบด้วยไฟล์ CSV จากฐานข้อมูลเชิงปฏิบัติการ (Operational Data) จำนวน 8 ไฟล์ ได้แก่:

- `aircrafts_data.csv`
- `airports_data.csv`
- `boarding_passes.csv`
- `bookings.csv`
- `flights.csv`
- `seats.csv`
- `ticket_flights.csv`
- `tickets.csv`

โปรเจกต์ใช้ Python script `scripts/load_raw.py` สำหรับโหลดข้อมูลจากไฟล์ CSV ทั้งหมดเข้าสู่ `raw` schema ภายในฐานข้อมูล `dev.duckdb`

ในขั้นตอนเริ่มต้น คอลัมน์ทั้งหมดจากข้อมูลต้นทางจะถูกโหลดเป็นชนิดข้อมูล `VARCHAR` โดยใช้:

`read_csv_auto(..., all_varchar=true)`

วิธีนี้ช่วยรักษาค่าของข้อมูลต้นทางไว้ก่อนที่จะเข้าสู่ขั้นตอนการทำความสะอาดและแปลงชนิดข้อมูลด้วย dbt


## 3. ชั้นข้อมูลดิบ (Raw Data Layer)

`raw` schema ใช้สำหรับเก็บรักษาข้อมูลต้นทางก่อนที่จะมีการแปลงข้อมูลตามกฎหรือความต้องการทางธุรกิจ

ตัวอย่างตารางข้อมูลใน Raw Data Layer ได้แก่:

- `raw.flights`
- `raw.airports_data`
- `raw.aircrafts_data`
- `raw.seats`
- `raw.boarding_passes`

ข้อมูลในชั้นนี้จึงทำหน้าที่เป็นข้อมูลตั้งต้นสำหรับกระบวนการ Staging และการแปลงข้อมูลในขั้นตอนถัดไป


## 4. การแปลงข้อมูลใน Staging Layer (Staging Transformations)

Staging Layer ใช้สำหรับทำความสะอาด ปรับรูปแบบ และแปลงชนิดข้อมูลจาก Raw Data ให้มีความเหมาะสมก่อนนำไปสร้าง Dimension Tables และ Fact Tables


### 4.1 `stg_flights`

การแปลงข้อมูลประกอบด้วย:

- แปลง `flight_id` จาก `VARCHAR` เป็น `INTEGER`
- แปลงข้อมูลวันและเวลาตามกำหนดการ (scheduled timestamps) เป็น `TIMESTAMPTZ`
- แปลงข้อมูลวันและเวลาที่เกิดขึ้นจริง (actual timestamps) เป็น `TIMESTAMPTZ`
- แปลงค่า `\N` ให้เป็น SQL `NULL`
- ปรับรูปแบบรหัสสนามบินด้วย `TRIM` และ `UPPER`
- ปรับรูปแบบรหัสเครื่องบินด้วย `TRIM` และ `UPPER`
- ทำความสะอาดข้อมูลสถานะเที่ยวบินด้วย `TRIM`

สำหรับข้อมูล `actual_departure` และ `actual_arrival` ที่ไม่มีค่า จะยังคงเก็บไว้เป็น `NULL` เนื่องจากเที่ยวบินที่อยู่ในสถานะ Scheduled หรือ Cancelled อาจยังไม่มีเวลาที่ออกเดินทางหรือเดินทางมาถึงจริง


### 4.2 `stg_airports`

การแปลงข้อมูลประกอบด้วย:

- ปรับรหัสสนามบิน (`airport_code`) ให้เป็นตัวอักษรพิมพ์ใหญ่
- ลบช่องว่างที่ไม่จำเป็นออกจากข้อมูลประเภทข้อความ
- รักษาข้อมูลหลักของสนามบิน (Airport Master Data) ให้มีหนึ่งแถวต่อหนึ่งรหัสสนามบิน


### 4.3 `stg_aircrafts`

การแปลงข้อมูลประกอบด้วย:

- ปรับรหัสเครื่องบิน (`aircraft_code`) ให้เป็นตัวอักษรพิมพ์ใหญ่
- ลบช่องว่างที่ไม่จำเป็นออกจากชื่อรุ่นเครื่องบิน
- แปลงข้อมูลระยะบิน (`range`) จาก `VARCHAR` เป็น `INTEGER`


### 4.4 `stg_seats`

การแปลงข้อมูลประกอบด้วย:

- ปรับรูปแบบรหัสเครื่องบินให้เป็นมาตรฐาน
- ปรับรูปแบบหมายเลขที่นั่ง (`seat_no`) ให้เป็นมาตรฐาน
- ทำความสะอาดข้อมูลประเภทชั้นโดยสาร (`fare_conditions`)
- ตรวจสอบข้อมูลโดยใช้ Composite Business Key ได้แก่ `aircraft_code + seat_no`


### 4.5 `stg_boarding_passes`

การแปลงข้อมูลประกอบด้วย:

- แปลง `flight_id` เป็น `INTEGER`
- แปลง `boarding_no` เป็น `INTEGER`
- ปรับรูปแบบหมายเลขที่นั่งให้เป็นมาตรฐาน
- ตรวจสอบข้อมูลซ้ำโดยใช้ `ticket_no + flight_id` เป็น Business Key


## 5. การตรวจสอบคุณภาพข้อมูล (Data Quality Validation)

โปรเจกต์ใช้ dbt tests สำหรับตรวจสอบคุณภาพและความถูกต้องของข้อมูลใน Staging Layer โดยครอบคลุม:

- การตรวจสอบค่า `NOT NULL`
- การตรวจสอบความไม่ซ้ำกัน (Uniqueness) ของ Business Keys
- การตรวจสอบความสัมพันธ์ระหว่าง Staging Models
- การตรวจสอบค่าที่ยอมรับได้ของสถานะเที่ยวบิน (Accepted Flight Status Values)
- การตรวจสอบค่าที่ยอมรับได้ของชั้นโดยสาร (Accepted Fare Class Values)

มีการตรวจสอบข้อมูลซ้ำโดยใช้ Business Key ของแต่ละชุดข้อมูล ได้แก่:

- Flights: `flight_id`
- Airports: `airport_code`
- Aircrafts: `aircraft_code`
- Seats: `aircraft_code + seat_no`
- Boarding Passes: `ticket_no + flight_id`

จากการตรวจสอบ ไม่พบข้อมูลซ้ำตาม Business Keys ที่กำหนดไว้


## 6. กระบวนการโหลดข้อมูล (Load Process)

หลังจากข้อมูลผ่านกระบวนการแปลงและตรวจสอบคุณภาพใน Staging Layer แล้ว ข้อมูลที่ผ่านการทำความสะอาดจะถูกนำไปใช้ในการสร้าง Dimension Tables ก่อน

จากนั้นจึงสร้าง Fact Tables โดยใช้ Keys ที่เชื่อมโยงกับ Dimension Tables

ลำดับการโหลดข้อมูลมีดังนี้:

Raw  
→ Staging  
→ Dimensions  
→ Facts  
→ Analytics / Dashboard

การสร้าง Dimension Tables ก่อน Fact Tables ช่วยให้สามารถรักษาความสัมพันธ์และ Referential Integrity ระหว่าง Fact Tables และ Dimension Tables ได้อย่างถูกต้อง


## 7. คำสั่งสำหรับตรวจสอบ Pipeline (Validation Commands)

ใช้คำสั่งต่อไปนี้ในการโหลดข้อมูล ตรวจสอบการเชื่อมต่อ สร้าง Models และทดสอบคุณภาพข้อมูล:

```bash
python scripts/load_raw.py
dbt debug
dbt run
dbt test
```

โดย:

- `python scripts/load_raw.py` ใช้สำหรับโหลดข้อมูลจากไฟล์ CSV เข้าสู่ DuckDB Raw Schema
- `dbt debug` ใช้ตรวจสอบการตั้งค่าและการเชื่อมต่อของ dbt
- `dbt run` ใช้สร้างและประมวลผล dbt Models
- `dbt test` ใช้ตรวจสอบคุณภาพและความถูกต้องของข้อมูลตาม Tests ที่กำหนดไว้


## 8. แผนภาพกระบวนการ ETL/ELT Pipeline

```mermaid
flowchart LR
    A[ข้อมูลต้นทาง CSV]
    --> B[Python load_raw.py]

    B --> C[DuckDB Raw Schema]

    C --> D[dbt Staging]

    D --> E[Dimension Tables]

    E --> F[Fact Tables]

    F --> G[Data Warehouse]

    G --> H[Interactive Dashboard]
```

แผนภาพแสดงลำดับการไหลของข้อมูลตั้งแต่ข้อมูลต้นทางในรูปแบบ CSV ผ่านกระบวนการโหลดข้อมูลด้วย Python เข้าสู่ DuckDB จากนั้นใช้ dbt ในการทำ Staging และแปลงข้อมูล ก่อนนำไปสร้าง Dimension Tables และ Fact Tables ภายใน Data Warehouse และนำข้อมูลที่ได้ไปใช้สำหรับการวิเคราะห์และแสดงผลผ่าน Interactive Dashboard
