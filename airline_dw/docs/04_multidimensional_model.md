# 04_Multidimensional_Model

## 1. ภาพรวมการออกแบบ

Airline Data Warehouse ถูกออกแบบในรูปแบบ **Galaxy Schema (Fact Constellation)** เนื่องจากระบบมี Fact Table มากกว่าหนึ่งตาราง และมี Dimension บางตารางที่ถูกใช้งานร่วมกันระหว่างหลาย Fact Table

โครงสร้าง Data Warehouse ประกอบด้วย Dimension Table จำนวน 5 ตาราง และ Fact Table จำนวน 3 ตาราง

### Dimension Tables

1. `dim_date`
2. `dim_airport`
3. `dim_aircraft`
4. `dim_fare_class`
5. `dim_flight_status`

### Fact Tables

1. `fact_ticket_sales`
2. `fact_flight_operations`
3. `fact_seat_utilization`

การออกแบบใหม่นี้รองรับการวิเคราะห์ข้อมูลได้หลายมุมมองมากขึ้น เช่น

- รายได้จากการขายตั๋ว
- จำนวน Ticket Flight
- แนวโน้มรายได้ตามช่วงเวลา
- สนามบินต้นทางและปลายทาง
- เส้นทางการบิน
- ภูมิภาคต้นทางและปลายทาง
- วันธรรมดาและวันหยุดสุดสัปดาห์
- ช่วงเวลาของวัน
- ประเภทชั้นโดยสาร
- รุ่นเครื่องบิน
- บริษัทผู้ผลิตเครื่องบิน
- สถานะเที่ยวบิน
- ระยะเวลาของเที่ยวบิน
- ความล่าช้าของเที่ยวบิน
- จำนวนที่นั่งทั้งหมด
- จำนวนตั๋วที่ขาย
- จำนวนผู้โดยสารที่ขึ้นเครื่อง
- อัตราการใช้ที่นั่ง
- รูปแบบการจองตั๋วล่วงหน้า

---

# 2. Dimension Tables

## 2.1 DIM_DATE

**ชื่อ Model:** `dim_date`

**วัตถุประสงค์:**  
ใช้สำหรับการวิเคราะห์ข้อมูลตามช่วงเวลา เช่น วัน สัปดาห์ เดือน ไตรมาส และปี รวมถึงการเปรียบเทียบข้อมูลระหว่างวันธรรมดาและวันหยุดสุดสัปดาห์

**Grain:**  
1 แถวแทน 1 วันที่

| Attribute | รายละเอียด |
|---|---|
| date_key | Surrogate Key ของวันที่ในรูปแบบ YYYYMMDD |
| full_date | วันที่เต็ม |
| day | วันที่ของเดือน |
| day_name | ชื่อวัน |
| week | สัปดาห์ของปี |
| month | หมายเลขเดือน |
| month_name | ชื่อเดือน |
| quarter | ไตรมาส |
| year | ปี |
| is_weekend | ระบุว่าวันดังกล่าวเป็นวันหยุดสุดสัปดาห์หรือไม่ |
| day_type | ประเภทวัน ได้แก่ Weekday หรือ Weekend |

### Hierarchy

Hierarchy หลักของ `dim_date` คือ

**Year → Quarter → Month → Date**

Hierarchy นี้สามารถใช้สำหรับการ Roll-up และ Drill-down ตามช่วงเวลาได้

ตัวอย่างเช่น จากข้อมูลระดับปี สามารถเจาะลงไปเป็นไตรมาส เดือน และวันที่ได้ตามลำดับ

นอกจากนี้ `day_type` ยังช่วยให้สามารถเปรียบเทียบพฤติกรรมการเดินทางระหว่าง

- Weekday
- Weekend

ได้อีกด้วย

---

## 2.2 DIM_AIRPORT

**ชื่อ Model:** `dim_airport`

**วัตถุประสงค์:**  
ใช้สำหรับวิเคราะห์ข้อมูลตามสนามบินต้นทาง สนามบินปลายทาง เมือง ประเทศ ภูมิภาค และเส้นทางการบิน

**Grain:**  
1 แถวแทน 1 สนามบิน

| Attribute | รายละเอียด |
|---|---|
| airport_key | Surrogate Key ของสนามบิน |
| airport_code | รหัสสนามบิน |
| airport_name | ชื่อสนามบิน |
| city | เมืองที่สนามบินตั้งอยู่ |
| country | ประเทศที่สนามบินตั้งอยู่ |
| analysis_region | ภูมิภาคที่ใช้สำหรับการวิเคราะห์ |
| coordinates | พิกัดของสนามบิน |
| timezone | เขตเวลาของสนามบิน |

### Hierarchy

สามารถใช้ข้อมูลในระดับ

**Country → Analysis Region → City → Airport**

เพื่อทำการ Roll-up และ Drill-down จากภาพรวมระดับประเทศหรือภูมิภาคไปจนถึงสนามบินแต่ละแห่ง

`analysis_region` เป็นกลุ่มภูมิภาคที่ใช้สำหรับการวิเคราะห์จากข้อมูลที่จัดเตรียมไว้ใน Dataset และไม่ควรตีความโดยอัตโนมัติว่าเป็นเขตการปกครองอย่างเป็นทางการ

### Role-Playing Dimension

`dim_airport` ถูกใช้เป็น **Role-Playing Dimension** เนื่องจาก Dimension เดียวกันถูกใช้ใน Fact Table มากกว่าหนึ่งบทบาท ได้แก่

- Departure Airport
- Arrival Airport

โดยเชื่อมผ่าน Foreign Key

- `departure_airport_key` → `dim_airport.airport_key`
- `arrival_airport_key` → `dim_airport.airport_key`

ดังนั้นจึงไม่จำเป็นต้องสร้าง Physical Dimension แยกเป็น `dim_departure_airport` และ `dim_arrival_airport`

แนวทางนี้ช่วยลดความซ้ำซ้อนของข้อมูล และยังสามารถวิเคราะห์สนามบินในบทบาทต้นทางและปลายทางได้อย่างชัดเจน

---

## 2.3 DIM_AIRCRAFT

**ชื่อ Model:** `dim_aircraft`

**วัตถุประสงค์:**  
ใช้สำหรับวิเคราะห์ข้อมูลตามรุ่นเครื่องบิน บริษัทผู้ผลิต และคุณลักษณะของเครื่องบิน

**Grain:**  
1 แถวแทน 1 Aircraft Code

| Attribute | รายละเอียด |
|---|---|
| aircraft_key | Surrogate Key ของเครื่องบิน |
| aircraft_code | รหัสเครื่องบิน |
| model | รุ่นของเครื่องบิน |
| manufacturer | บริษัทผู้ผลิตเครื่องบิน |
| range | ระยะทางสูงสุดที่เครื่องบินสามารถบินได้ |

ตัวอย่างบริษัทผู้ผลิตในข้อมูล เช่น

- Boeing
- Airbus
- Sukhoi
- Cessna
- Bombardier

### Hierarchy

สามารถวิเคราะห์ข้อมูลในระดับ

**Manufacturer → Aircraft Model / Aircraft Code**

ตัวอย่างเช่น สามารถเริ่มจากการวิเคราะห์จำนวนเที่ยวบินของ Boeing และ Airbus แล้ว Drill-down ลงไปดูแต่ละ Model ได้

Dimension นี้สามารถถูกใช้งานร่วมกับ Fact ที่เกี่ยวข้องกับ

- การขายตั๋ว
- การดำเนินงานของเที่ยวบิน
- การใช้ Capacity ของเครื่องบิน

ทำให้สามารถเปรียบเทียบการใช้งานเครื่องบินแต่ละ Manufacturer และ Model ได้

---

## 2.4 DIM_FARE_CLASS

**ชื่อ Model:** `dim_fare_class`

**วัตถุประสงค์:**  
ใช้สำหรับจำแนกข้อมูลตามประเภทชั้นโดยสาร

**Grain:**  
1 แถวแทน 1 Fare Class

| Attribute | รายละเอียด |
|---|---|
| fare_class_key | Surrogate Key ของ Fare Class |
| fare_class | ชื่อประเภทชั้นโดยสาร |

Fare Class ที่ใช้ในระบบ ได้แก่

- Business
- Comfort
- Economy

Dimension นี้สามารถใช้ร่วมกับข้อมูล Ticket Sales เพื่อวิเคราะห์

- รายได้ตาม Fare Class
- จำนวน Ticket Flight ตาม Fare Class
- สัดส่วนรายได้ของแต่ละ Fare Class
- รูปแบบการจองล่วงหน้าในแต่ละ Fare Class
- Route × Fare Class

---

## 2.5 DIM_FLIGHT_STATUS

**ชื่อ Model:** `dim_flight_status`

**วัตถุประสงค์:**  
ใช้สำหรับจำแนกสถานะด้านการดำเนินงานของเที่ยวบิน หรือ **Operational Flight Status**

**Grain:**  
1 แถวแทน 1 Flight Status

| Attribute | รายละเอียด |
|---|---|
| status_key | Surrogate Key ของสถานะเที่ยวบิน |
| status_name | ชื่อสถานะเที่ยวบิน |

สถานะเที่ยวบินที่รองรับในระบบ ได้แก่

- Arrived
- Scheduled
- On Time
- Cancelled
- Departed
- Delayed

`dim_flight_status` เป็น Dimension สำหรับจำแนกประเภทของสถานะเที่ยวบิน และแตกต่างจาก Measure ด้านความล่าช้า

ตัวอย่างเช่น

- `status_name = Delayed`
- `departure_delay_minutes = 125`

โดย `Delayed` เป็น Dimension Value ส่วน `125 นาที` เป็น Measure ที่ใช้บอกระดับความล่าช้า

Dimension นี้เชื่อมกับ `fact_flight_operations` เพื่อใช้วิเคราะห์การดำเนินงานของเที่ยวบินตามสถานะ

---

# 3. Fact Tables

## 3.1 FACT_TICKET_SALES

**ชื่อ Model:** `fact_ticket_sales`

### Grain

1 แถวแทน **1 Ticket × 1 Flight Segment**

ดังนั้น Ticket เดียวสามารถมีหลายแถวได้ หาก Ticket นั้นประกอบด้วยเที่ยวบินหลายช่วง

### Dimension Keys

| Foreign Key | Dimension |
|---|---|
| date_key | dim_date |
| departure_airport_key | dim_airport |
| arrival_airport_key | dim_airport |
| aircraft_key | dim_aircraft |
| fare_class_key | dim_fare_class |

### Transaction Identifiers

| Attribute | รายละเอียด |
|---|---|
| ticket_no | หมายเลขตั๋ว |
| flight_id | รหัสเที่ยวบิน |

### Measures / Analytical Attributes

| Attribute | ความหมาย | ประเภท |
|---|---|---|
| amount | ยอดขายตั๋วของ Ticket Flight Segment | Additive Measure |
| ticket_flight_count | จำนวน Ticket Flight โดยแต่ละแถวมีค่า 1 | Additive Measure |
| booking_lead_days | จำนวนวันที่มีการจองล่วงหน้าก่อนวันเดินทาง | Analytical Attribute |

### การวิเคราะห์ที่รองรับ

Fact Table นี้สามารถใช้ตอบคำถาม เช่น

- เส้นทางใดสร้างรายได้จากการขายตั๋วสูงที่สุด
- Fare Class ใดสร้างรายได้สูงที่สุด
- Fare Class แต่ละประเภทมีสัดส่วนรายได้เท่าใด
- รายได้มีแนวโน้มเปลี่ยนแปลงอย่างไรในแต่ละเดือน
- ภูมิภาคต้นทาง–ปลายทางคู่ใดมี Demand สูง
- ผู้โดยสารมักจองตั๋วล่วงหน้ากี่วัน
- รูปแบบการจองล่วงหน้าแตกต่างกันอย่างไรตาม Fare Class
- Route × Fare Class ใดสร้างรายได้สูงแม้จำนวนตั๋วไม่สูง

---

## 3.2 FACT_FLIGHT_OPERATIONS

**ชื่อ Model:** `fact_flight_operations`

### Grain

1 แถวแทน **1 เที่ยวบิน**

### Dimension Keys

| Foreign Key | Dimension |
|---|---|
| date_key | dim_date |
| departure_airport_key | dim_airport |
| arrival_airport_key | dim_airport |
| aircraft_key | dim_aircraft |
| status_key | dim_flight_status |

### Identifiers

| Attribute | รายละเอียด |
|---|---|
| flight_id | รหัสเที่ยวบิน |
| flight_no | หมายเลขเที่ยวบิน |

### Operational Attributes

ข้อมูลสำหรับการวิเคราะห์การดำเนินงานของเที่ยวบินประกอบด้วย เช่น

- `scheduled_departure`
- `scheduled_arrival`
- `actual_departure`
- `actual_arrival`
- `departure_daypart`
- `departure_is_weekend`

### Measures

| Measure | ความหมาย | Measure Type |
|---|---|---|
| flight_count | จำนวนเที่ยวบิน โดยแต่ละแถวมีค่า 1 | Additive |
| scheduled_duration_minutes | ระยะเวลาเดินทางตามตาราง | Non-Additive |
| actual_duration_minutes | ระยะเวลาเดินทางจริง | Non-Additive |
| departure_delay_minutes | จำนวนนาทีที่ออกเดินทางล่าช้า | Non-Additive |
| arrival_delay_minutes | จำนวนนาทีที่เดินทางถึงล่าช้า | Non-Additive |

### Flags

สามารถมี Operational Flags เช่น

- `scheduled_duration_over_2h`
- `departure_delay_over_2h`
- `arrival_delay_over_2h`

เพื่อแยกเที่ยวบินที่มี Duration หรือ Delay สูงกว่า 2 ชั่วโมงออกจากเที่ยวบินทั่วไป

### การ Aggregate Delay

Measure ประเภท Delay ไม่ควรนำค่ามารวมด้วย `SUM()` เพื่อใช้ตีความโดยตรง

ควรวิเคราะห์ด้วยค่าเฉลี่ย เช่น

`AVG(departure_delay_minutes)`

หรือ

`AVG(arrival_delay_minutes)`

เพื่อเปรียบเทียบระดับความล่าช้าในแต่ละ Route, Region หรือ Daypart

### การวิเคราะห์ที่รองรับ

Fact Table นี้สามารถใช้ตอบคำถาม เช่น

- ช่วงเวลาใดของวันมีจำนวนเที่ยวบินมากที่สุด
- Weekday และ Weekend มีจำนวนเที่ยวบินแตกต่างกันอย่างไร
- Aircraft Manufacturer และ Model ใดถูกใช้งานมากที่สุด
- Route ใดมี Departure Delay และ Arrival Delay เฉลี่ยสูง
- Region × Daypart ใดมีความล่าช้าเฉลี่ยสูง
- มีเที่ยวบินที่ Delay มากกว่า 2 ชั่วโมงจำนวนเท่าใด

---

## 3.3 FACT_SEAT_UTILIZATION

**ชื่อ Model:** `fact_seat_utilization`

Fact นี้ถูกออกแบบใหม่จากแนวคิดเดิมของ `fact_seat_inventory` เพื่อให้สามารถวิเคราะห์การใช้ Capacity ของเที่ยวบินได้จริง และลดความซ้ำซ้อนกับข้อมูล Ticket Sales

### Grain

1 แถวแทน **1 เที่ยวบิน**

### Dimension Keys

Dimension Key ที่สามารถใช้ร่วมกับ Fact นี้ ได้แก่

| Foreign Key | Dimension |
|---|---|
| date_key | dim_date |
| departure_airport_key | dim_airport |
| arrival_airport_key | dim_airport |
| aircraft_key | dim_aircraft |

### Measures

| Measure | ความหมาย | Measure Type |
|---|---|---|
| seat_capacity | จำนวนที่นั่งทั้งหมดที่เครื่องบินสามารถรองรับได้ | Additive ตาม Grain ที่เหมาะสม |
| ticket_flight_count | จำนวน Ticket Flight ของเที่ยวบิน | Additive |
| boarded_count | จำนวนผู้โดยสารที่มี Boarding Pass / ขึ้นเครื่องตามข้อมูล | Additive |
| available_seats | จำนวนที่นั่งที่ยังไม่ถูกใช้งาน | Additive |
| ticketed_load_pct | อัตราการใช้ Capacity เมื่อพิจารณาจาก Ticket | Non-Additive |
| boarded_load_pct | อัตราการใช้ Capacity เมื่อพิจารณาจากผู้โดยสารที่ขึ้นเครื่องจริง | Non-Additive |

### available_seats

สามารถคำนวณจาก

`seat_capacity - boarded_count`

### ความแตกต่างจาก Fact อื่น

`fact_ticket_sales`

→ วิเคราะห์ด้านการขายและรายได้

`fact_flight_operations`

→ วิเคราะห์ด้านเวลา สถานะ และการดำเนินงาน

`fact_seat_utilization`

→ วิเคราะห์ด้าน Capacity และการใช้ที่นั่ง

การแยก Business Process ดังกล่าวช่วยให้ Fact Table ทั้ง 3 ตารางมีหน้าที่ชัดเจนและไม่ซ้ำกัน

### การวิเคราะห์ที่รองรับ

Fact Table นี้สามารถใช้ตอบคำถาม เช่น

- Route ใดมีอัตราการใช้ที่นั่งจริงสูงหรือต่ำ
- จำนวน Ticket ที่ขายกับจำนวนผู้โดยสารที่ขึ้นเครื่องจริงแตกต่างกันมากเพียงใด
- Region × Aircraft Manufacturer/Model ใดมีอัตราการใช้ที่นั่งสูง
- Route × Time ใดมี Demand สูงและ Load สูงจนใกล้เต็ม

---

# 4. Shared Dimensions

เนื่องจาก Data Warehouse นี้เป็น Galaxy Schema จึงมี Dimension ที่ถูกใช้ร่วมกันระหว่างหลาย Fact Table

| Dimension | fact_ticket_sales | fact_flight_operations | fact_seat_utilization |
|---|:---:|:---:|:---:|
| dim_date | ✓ | ✓ | ✓ |
| dim_airport | ✓ | ✓ | ✓ |
| dim_aircraft | ✓ | ✓ | ✓ |
| dim_fare_class | ✓ | - | - |
| dim_flight_status | - | ✓ | - |

การใช้ Shared Dimension ทำให้ Fact Table หลายตารางสามารถวิเคราะห์ข้อมูลภายใต้มุมมองเดียวกันได้

ตัวอย่างเช่น `dim_aircraft` สามารถใช้ร่วมกันเพื่อเปรียบเทียบ

- รายได้ตาม Aircraft
- จำนวนเที่ยวบินตาม Aircraft
- Capacity และ Load ตาม Aircraft

และ `dim_airport` สามารถทำหน้าที่เป็นทั้ง Departure Airport และ Arrival Airport ในหลาย Fact Table

---

# 5. Fact Grain Summary

| Fact Table | Grain |
|---|---|
| fact_ticket_sales | 1 Ticket × 1 Flight Segment |
| fact_flight_operations | 1 Flight |
| fact_seat_utilization | 1 Flight |

การกำหนด Grain ของ Fact Table อย่างชัดเจนช่วยป้องกันปัญหาการนับข้อมูลซ้ำ และช่วยให้การ Aggregate ข้อมูลมีความถูกต้อง

ถึงแม้ `fact_flight_operations` และ `fact_seat_utilization` จะมี Grain ระดับ 1 Flight เหมือนกัน แต่ทั้งสอง Fact แทน Business Process ต่างกัน

- `fact_flight_operations` → Flight Operation
- `fact_seat_utilization` → Capacity Utilization

---

# 6. Measure Classification

Measure ใน Data Warehouse สามารถแบ่งตามลักษณะการ Aggregate ได้

## Additive Measures

Measure ที่สามารถใช้ `SUM()` ได้ตาม Grain และ Dimension ที่เหมาะสม เช่น

- `fact_ticket_sales.amount`
- `fact_ticket_sales.ticket_flight_count`
- `fact_flight_operations.flight_count`
- `fact_seat_utilization.ticket_flight_count`
- `fact_seat_utilization.boarded_count`
- `fact_seat_utilization.available_seats`

ตัวอย่างเช่น `amount` สามารถนำมารวมเพื่อหายอดขายรวม หรือยอดขายตาม Route และ Fare Class ได้

## Non-Additive / Average-Based Measures

Measure ที่ไม่ควรนำมารวมด้วย `SUM()` เพื่อใช้ตีความโดยตรง ได้แก่

- `fact_flight_operations.scheduled_duration_minutes`
- `fact_flight_operations.actual_duration_minutes`
- `fact_flight_operations.departure_delay_minutes`
- `fact_flight_operations.arrival_delay_minutes`
- `fact_seat_utilization.ticketed_load_pct`
- `fact_seat_utilization.boarded_load_pct`

ตัวอย่างเช่น

`AVG(departure_delay_minutes)`

ใช้หาค่าเฉลี่ยความล่าช้าในการออกเดินทาง

และ

`AVG(boarded_load_pct)`

ใช้เปรียบเทียบระดับการใช้ Capacity ระหว่าง Route หรือ Aircraft

---

# 7. Dimension Hierarchies

Dimension ที่มีระดับสำหรับการวิเคราะห์มีดังนี้

| Dimension | Hierarchy / Level |
|---|---|
| dim_date | Year → Quarter → Month → Date |
| dim_airport | Country → Analysis Region → City → Airport |
| dim_aircraft | Manufacturer → Aircraft Model / Aircraft Code |
| dim_fare_class | Fare Class |
| dim_flight_status | Flight Status |

`dim_date` รองรับการ Roll-up และ Drill-down ตามระดับเวลา

ตัวอย่างการ Drill-down:

**Year → Quarter → Month → Date**

ตัวอย่างการ Roll-up:

**Date → Month → Quarter → Year**

`dim_airport` สามารถ Drill-down จากระดับประเทศไปยัง Region เมือง และสนามบิน

`dim_aircraft` สามารถวิเคราะห์จากบริษัทผู้ผลิตลงไปยัง Aircraft Model ได้

สำหรับ `dim_fare_class` และ `dim_flight_status` ไม่มี Hierarchy หลายระดับ เนื่องจากเป็น Dimension สำหรับการจำแนกประเภทข้อมูลโดยตรง

---

# 8. Galaxy Schema Relationships

ความสัมพันธ์หลักของ Multidimensional Model มีดังนี้

### DIM_DATE

เชื่อมกับ

- `fact_ticket_sales` ผ่าน `date_key`
- `fact_flight_operations` ผ่าน `date_key`
- `fact_seat_utilization` ผ่าน `date_key`

### DIM_AIRPORT

ใช้เป็น Role-Playing Dimension

เชื่อมกับ `fact_ticket_sales` ผ่าน

- `departure_airport_key`
- `arrival_airport_key`

เชื่อมกับ `fact_flight_operations` ผ่าน

- `departure_airport_key`
- `arrival_airport_key`

และเชื่อมกับ `fact_seat_utilization` ผ่าน

- `departure_airport_key`
- `arrival_airport_key`

### DIM_AIRCRAFT

เชื่อมกับ

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_utilization`

ผ่าน `aircraft_key`

### DIM_FARE_CLASS

เชื่อมกับ

- `fact_ticket_sales`

ผ่าน `fare_class_key`

### DIM_FLIGHT_STATUS

เชื่อมกับ

- `fact_flight_operations`

ผ่าน `status_key`

โครงสร้างดังกล่าวทำให้ Dimension หลายตารางสามารถถูกใช้ร่วมกันระหว่าง Fact Table และสนับสนุนการวิเคราะห์ข้อมูลแบบหลายมิติ

---

# 9. Business Question Mapping

| Q | Business Question | Fact Table | Dimension / Attribute หลัก | Measure |
|---|---|---|---|---|
| Q1 | เส้นทางใดสร้างรายได้จากการขายตั๋วสูงที่สุด | fact_ticket_sales | Departure Airport + Arrival Airport | amount |
| Q2 | Fare Class ใดสร้างรายได้สูงที่สุด และมีสัดส่วนรายได้เท่าใด | fact_ticket_sales | dim_fare_class | amount |
| Q3 | รายได้จากการขายตั๋วมีแนวโน้มเปลี่ยนแปลงอย่างไรในแต่ละเดือน | fact_ticket_sales | dim_date | amount |
| Q4 | ภูมิภาคต้นทาง–ปลายทางคู่ใดมีความต้องการเดินทางสูงที่สุด | fact_ticket_sales | Departure Region + Arrival Region | ticket_flight_count |
| Q5 | เส้นทางใดมีอัตราการใช้ที่นั่งของผู้โดยสารจริงสูงและต่ำที่สุด | fact_seat_utilization | Departure Airport + Arrival Airport | boarded_load_pct |
| Q6 | เที่ยวบินใดมีช่องว่างระหว่างจำนวนตั๋วที่ขายกับจำนวนผู้โดยสารที่ขึ้นเครื่องจริงมากที่สุด | fact_seat_utilization | Flight | ticket_flight_count, boarded_count |
| Q7 | ช่วงเวลาใดของวันมีจำนวนเที่ยวบินและปริมาณผู้โดยสารสูงที่สุด | fact_flight_operations + fact_seat_utilization | Departure Daypart | flight_count, boarded_count |
| Q8 | วันธรรมดากับวันหยุดสุดสัปดาห์มีความต้องการเดินทางแตกต่างกันอย่างไร | fact_ticket_sales / fact_seat_utilization | dim_date | ticket_flight_count / boarded_count |
| Q9 | ผู้โดยสารมักจองตั๋วล่วงหน้ากี่วัน และแตกต่างกันอย่างไรในแต่ละ Fare Class | fact_ticket_sales | dim_fare_class | booking_lead_days |
| Q10 | Aircraft Manufacturer และรุ่นเครื่องบินใดถูกใช้งานกับเที่ยวบินมากที่สุด | fact_flight_operations | dim_aircraft | flight_count |
| Q11 | เส้นทางใดมีความล่าช้าในการออกเดินทางและถึงปลายทางเฉลี่ยสูงที่สุด | fact_flight_operations | Departure Airport + Arrival Airport | departure_delay_minutes, arrival_delay_minutes |
| Q12 | ในแต่ละภูมิภาคและช่วงเวลาของวัน ช่วงใดมีความล่าช้าในการออกเดินทางเฉลี่ยสูงที่สุด | fact_flight_operations | Analysis Region × Daypart | departure_delay_minutes |
| Q13 | ในแต่ละเส้นทาง Fare Class ใดสร้างรายได้สูง แต่มีจำนวนตั๋วขายไม่สูงตามไปด้วย | fact_ticket_sales | Route × dim_fare_class | amount, ticket_flight_count |
| Q14 | ในแต่ละภูมิภาค Aircraft Manufacturer/Model ใดมีอัตราการใช้ที่นั่งจริงสูงที่สุด | fact_seat_utilization | Analysis Region × dim_aircraft | boarded_load_pct |
| Q15 | เส้นทางและช่วงเวลาใดมีความต้องการเดินทางสูง แต่มีอัตราการใช้ที่นั่งสูงจนใกล้เต็มอย่างต่อเนื่อง | fact_seat_utilization | Route × Time | boarded_count, boarded_load_pct |

Business Question ชุดใหม่นี้ออกแบบให้ไม่ได้มุ่งเพียงการหา “ค่าสูงสุด” แต่เน้นให้สามารถนำผลการวิเคราะห์ไปประกอบการตัดสินใจ เช่น

- วางแผนเส้นทาง
- จัดสรร Capacity
- ปรับตารางเที่ยวบิน
- วิเคราะห์ Demand
- วางกลยุทธ์ราคา
- วิเคราะห์ Fleet
- ตรวจสอบ Operational Issues

---

# 10. สรุป

Airline Data Warehouse ถูกออกแบบในรูปแบบ **Galaxy Schema** ซึ่งประกอบด้วย Dimension Table จำนวน 5 ตาราง และ Fact Table จำนวน 3 ตาราง

Dimension Table ประกอบด้วย

- `dim_date`
- `dim_airport`
- `dim_aircraft`
- `dim_fare_class`
- `dim_flight_status`

โดย Dimension ได้รับการปรับปรุงจาก Version เดิม ได้แก่

- `dim_date` เพิ่ม `is_weekend` และ `day_type`
- `dim_airport` เพิ่ม `country` และ `analysis_region`
- `dim_aircraft` เพิ่ม `manufacturer`
- `dim_airport` ถูกกำหนดบทบาทเป็น Role-Playing Dimension สำหรับ Departure และ Arrival อย่างชัดเจน
- `dim_flight_status` ใช้แทน Operational Status ของเที่ยวบิน

Fact Table ประกอบด้วย

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_utilization`

โดย Fact แต่ละตัวมี Business Process ที่แตกต่างกัน ได้แก่

- Ticket Sales → รายได้และ Demand
- Flight Operations → เวลา สถานะ Duration และ Delay
- Seat Utilization → Capacity และการใช้ที่นั่ง

Fact Table แต่ละตารางมี Grain ที่กำหนดไว้อย่างชัดเจน ช่วยลดความเสี่ยงในการนับข้อมูลซ้ำ และทำให้การ Aggregate มีความถูกต้อง

Dimension หลายตารางถูกใช้ร่วมกันระหว่าง Fact Table ทำให้สามารถวิเคราะห์ข้อมูลในมุมมองต่าง ๆ เช่น

- เวลา
- Weekday / Weekend
- สนามบิน
- Region
- Route
- เครื่องบิน
- Manufacturer
- Fare Class
- Flight Status
- Delay
- Capacity
- Load Percentage

ได้อย่างสอดคล้องกัน

Multidimensional Model ใหม่นี้จึงรองรับ Business Questions ชุดใหม่และการสร้าง Dashboard จาก Data Warehouse โดยตรงได้ดีกว่า Model เดิม
