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
3. `fact_seat_inventory`

การออกแบบนี้ช่วยให้สามารถวิเคราะห์ข้อมูลได้หลายมุมมอง เช่น

- ยอดขายตั๋ว
- จำนวน Ticket Flight
- ช่วงเวลา
- สนามบินต้นทางและปลายทาง
- เส้นทางการบิน
- ชั้นโดยสาร
- รุ่นเครื่องบิน
- สถานะเที่ยวบิน
- ความล่าช้าของเที่ยวบิน
- จำนวนและสัดส่วนที่นั่ง

---

# 2. Dimension Tables

## 2.1 DIM_DATE

**ชื่อ Model:** `dim_date`

**วัตถุประสงค์:**  
ใช้สำหรับการวิเคราะห์ข้อมูลตามช่วงเวลา เช่น วัน สัปดาห์ เดือน ไตรมาส และปี

**Grain:**  
1 แถวแทน 1 วันที่

| Attribute | รายละเอียด |
|---|---|
| date_key | Surrogate Key ของวันที่ |
| full_date | วันที่เต็ม |
| day | วันที่ของเดือน |
| day_name | ชื่อวัน |
| week | สัปดาห์ของปี |
| month | หมายเลขเดือน |
| month_name | ชื่อเดือน |
| quarter | ไตรมาส |
| year | ปี |

### Hierarchy

Hierarchy หลักของ `dim_date` คือ

**Year → Quarter → Month → Date**

Hierarchy นี้สามารถใช้สำหรับการ Roll-up และ Drill-down ตามช่วงเวลาได้

ตัวอย่างเช่น จากข้อมูลระดับปี สามารถเจาะลงไปเป็นไตรมาส เดือน และวันที่ได้ตามลำดับ

---

## 2.2 DIM_AIRPORT

**ชื่อ Model:** `dim_airport`

**วัตถุประสงค์:**  
ใช้สำหรับวิเคราะห์ข้อมูลตามสนามบินต้นทาง สนามบินปลายทาง และเส้นทางการบิน

**Grain:**  
1 แถวแทน 1 สนามบิน

| Attribute | รายละเอียด |
|---|---|
| airport_key | Surrogate Key ของสนามบิน |
| airport_code | รหัสสนามบิน |
| airport_name | ชื่อสนามบิน |
| city | เมืองที่สนามบินตั้งอยู่ |
| coordinates | พิกัดของสนามบิน |
| timezone | เขตเวลาของสนามบิน |

### Hierarchy

สามารถใช้ข้อมูลในระดับ

**City → Airport**

เพื่อวิเคราะห์ข้อมูลจากระดับเมืองลงไปถึงสนามบินแต่ละแห่ง

### Role-Playing Dimension

`dim_airport` ถูกใช้เป็น **Role-Playing Dimension** เนื่องจาก Dimension เดียวกันถูกใช้ใน Fact Table มากกว่าหนึ่งบทบาท ได้แก่

- Departure Airport
- Arrival Airport

โดยเชื่อมผ่าน Foreign Key

- `departure_airport_key` → `dim_airport.airport_key`
- `arrival_airport_key` → `dim_airport.airport_key`

ทำให้สามารถวิเคราะห์ข้อมูลทั้งในมุมของสนามบินต้นทางและสนามบินปลายทางได้โดยไม่จำเป็นต้องสร้าง Dimension แยกออกเป็นสองตาราง

---

## 2.3 DIM_AIRCRAFT

**ชื่อ Model:** `dim_aircraft`

**วัตถุประสงค์:**  
ใช้สำหรับวิเคราะห์ข้อมูลตามรุ่นและคุณลักษณะของเครื่องบิน

**Grain:**  
1 แถวแทน 1 Aircraft Code

| Attribute | รายละเอียด |
|---|---|
| aircraft_key | Surrogate Key ของเครื่องบิน |
| aircraft_code | รหัสเครื่องบิน |
| model | รุ่นของเครื่องบิน |
| range | ระยะทางสูงสุดที่เครื่องบินสามารถบินได้ |

Dimension นี้ถูกใช้งานร่วมกันระหว่าง

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_inventory`

จึงสามารถใช้วิเคราะห์ข้อมูลทั้งยอดขาย จำนวนเที่ยวบิน และจำนวนที่นั่งตามรุ่นเครื่องบินได้

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

Dimension นี้ถูกใช้งานร่วมกันระหว่าง

- `fact_ticket_sales`
- `fact_seat_inventory`

ทำให้สามารถวิเคราะห์ทั้งยอดขายตั๋วและโครงสร้างที่นั่งตาม Fare Class ได้

---

## 2.5 DIM_FLIGHT_STATUS

**ชื่อ Model:** `dim_flight_status`

**วัตถุประสงค์:**  
ใช้สำหรับจำแนกสถานะของเที่ยวบิน

**Grain:**  
1 แถวแทน 1 Flight Status

| Attribute | รายละเอียด |
|---|---|
| status_key | Surrogate Key ของสถานะเที่ยวบิน |
| status_name | ชื่อสถานะเที่ยวบิน |

ตัวอย่างสถานะเที่ยวบินที่ใช้ในการวิเคราะห์ ได้แก่

- Arrived
- Scheduled
- On Time
- Cancelled
- Departed
- Delayed

Dimension นี้เชื่อมกับ `fact_flight_operations` เพื่อใช้วิเคราะห์จำนวนเที่ยวบินตามสถานะ

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

### Measures

| Measure | ความหมาย | Measure Type |
|---|---|---|
| amount | ยอดขายตั๋วของ Ticket Flight Segment | Additive |
| ticket_flight_count | จำนวน Ticket Flight โดยแต่ละแถวมีค่า 1 | Additive |

### การวิเคราะห์ที่รองรับ

Fact Table นี้สามารถใช้ตอบคำถาม เช่น

- ยอดขายตั๋วรวม
- จำนวน Ticket Flight
- ยอดขายตาม Fare Class
- จำนวน Ticket Flight ตาม Fare Class
- ยอดขายตามช่วงเวลา
- สนามบินต้นทางยอดนิยม
- สนามบินปลายทางยอดนิยม
- เส้นทางที่มี Ticket Flight มากที่สุด
- เส้นทางที่สร้างยอดขายสูงที่สุด

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

- `scheduled_departure`
- `scheduled_arrival`
- `actual_departure`
- `actual_arrival`

### Measures

| Measure | ความหมาย | Measure Type |
|---|---|---|
| departure_delay_minutes | จำนวนนาทีที่เที่ยวบินออกเดินทางล่าช้า | Non-Additive |
| arrival_delay_minutes | จำนวนนาทีที่เที่ยวบินเดินทางถึงล่าช้า | Non-Additive |
| flight_count | จำนวนเที่ยวบิน โดยแต่ละแถวมีค่า 1 | Additive |

Measure ประเภท Delay เหมาะกับการวิเคราะห์ด้วยค่าเฉลี่ย เช่น `AVG()` มากกว่าการนำค่ามารวมด้วย `SUM()`

### การวิเคราะห์ที่รองรับ

Fact Table นี้สามารถใช้ตอบคำถาม เช่น

- Aircraft Model ใดถูกใช้กับเที่ยวบินมากที่สุด
- Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด
- สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด

---

## 3.3 FACT_SEAT_INVENTORY

**ชื่อ Model:** `fact_seat_inventory`

### Grain

1 แถวแทน **1 Aircraft × 1 Fare Class**

จำนวนที่นั่งถูก Aggregate จากข้อมูลที่นั่งตาม Aircraft และ Fare Class

### Dimension Keys

| Foreign Key | Dimension |
|---|---|
| aircraft_key | dim_aircraft |
| fare_class_key | dim_fare_class |

### Measures

| Measure | ความหมาย | Measure Type |
|---|---|---|
| seat_count | จำนวนที่นั่งของ Aircraft ใน Fare Class นั้น | Additive |

### การวิเคราะห์ที่รองรับ

Fact Table นี้สามารถใช้ตอบคำถาม เช่น

- Aircraft Model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด
- Aircraft Model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร

### หมายเหตุ

Fact Table นี้ไม่มี Date Dimension เนื่องจากข้อมูลที่นั่งเป็นข้อมูลโครงสร้างของ Aircraft และไม่ได้เป็นเหตุการณ์ที่เกิดขึ้นตามช่วงเวลา

---

# 4. Shared Dimensions

เนื่องจาก Data Warehouse นี้เป็น Galaxy Schema จึงมี Dimension ที่ถูกใช้ร่วมกันระหว่างหลาย Fact Table

| Dimension | fact_ticket_sales | fact_flight_operations | fact_seat_inventory |
|---|:---:|:---:|:---:|
| dim_date | ✓ | ✓ | - |
| dim_airport | ✓ | ✓ | - |
| dim_aircraft | ✓ | ✓ | ✓ |
| dim_fare_class | ✓ | - | ✓ |
| dim_flight_status | - | ✓ | - |

การใช้ Shared Dimension ทำให้ Fact Table หลายตารางสามารถวิเคราะห์ข้อมูลภายใต้มุมมองเดียวกันได้

ตัวอย่างเช่น `dim_aircraft` ถูกใช้ร่วมกันในทั้ง 3 Fact Table จึงสามารถนำมาใช้เปรียบเทียบข้อมูลระหว่าง

- ยอดขายตั๋วตาม Aircraft
- จำนวนเที่ยวบินตาม Aircraft
- จำนวนที่นั่งตาม Aircraft

---

# 5. Fact Grain Summary

| Fact Table | Grain |
|---|---|
| fact_ticket_sales | 1 Ticket × 1 Flight Segment |
| fact_flight_operations | 1 Flight |
| fact_seat_inventory | 1 Aircraft × 1 Fare Class |

การกำหนด Grain ของ Fact Table อย่างชัดเจนช่วยป้องกันปัญหาการนับข้อมูลซ้ำ และช่วยให้การ Aggregate ข้อมูลมีความถูกต้อง

---

# 6. Measure Classification

Measure ใน Data Warehouse สามารถแบ่งได้เป็น Additive Measure และ Non-Additive Measure

## Additive Measures

Additive Measure สามารถนำมารวมค่าด้วย `SUM()` ได้ตาม Dimension ที่เกี่ยวข้อง

ประกอบด้วย

- `fact_ticket_sales.amount`
- `fact_ticket_sales.ticket_flight_count`
- `fact_flight_operations.flight_count`
- `fact_seat_inventory.seat_count`

ตัวอย่างเช่น `amount` สามารถนำมารวมเพื่อหายอดขายตั๋วรวม หรือยอดขายตาม Fare Class ได้

## Non-Additive Measures

Measure ประเภท Delay ไม่ควรนำค่ามารวมด้วย `SUM()` เพื่อใช้ตีความโดยตรง แต่เหมาะกับการวิเคราะห์ด้วยค่าเฉลี่ย เช่น `AVG()`

ประกอบด้วย

- `fact_flight_operations.departure_delay_minutes`
- `fact_flight_operations.arrival_delay_minutes`

ตัวอย่างเช่น สามารถใช้ `AVG(departure_delay_minutes)` เพื่อหาความล่าช้าเฉลี่ยของสนามบินต้นทาง

---

# 7. Dimension Hierarchies

Dimension ที่มีระดับสำหรับการวิเคราะห์มีดังนี้

| Dimension | Hierarchy / Level |
|---|---|
| dim_date | Year → Quarter → Month → Date |
| dim_airport | City → Airport |
| dim_aircraft | Aircraft Model / Aircraft Code |
| dim_fare_class | Fare Class |
| dim_flight_status | Flight Status |

`dim_date` เป็น Dimension ที่มี Hierarchy ชัดเจนที่สุด และรองรับการ Roll-up และ Drill-down ตามระดับเวลา

ตัวอย่างการ Drill-down ของ Time Dimension:

**Year → Quarter → Month → Date**

ตัวอย่างการ Roll-up:

**Date → Month → Quarter → Year**

สำหรับ `dim_fare_class` และ `dim_flight_status` ไม่มี Hierarchy หลายระดับ เนื่องจากเป็น Dimension สำหรับการจำแนกประเภทข้อมูลโดยตรง

---

# 8. Galaxy Schema Relationships

ความสัมพันธ์หลักของ Multidimensional Model มีดังนี้

### DIM_DATE

เชื่อมกับ

- `fact_ticket_sales` ผ่าน `date_key`
- `fact_flight_operations` ผ่าน `date_key`

### DIM_AIRPORT

เชื่อมกับ `fact_ticket_sales` ผ่าน

- `departure_airport_key`
- `arrival_airport_key`

และเชื่อมกับ `fact_flight_operations` ผ่าน

- `departure_airport_key`
- `arrival_airport_key`

### DIM_AIRCRAFT

เชื่อมกับ

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_inventory`

ผ่าน `aircraft_key`

### DIM_FARE_CLASS

เชื่อมกับ

- `fact_ticket_sales`
- `fact_seat_inventory`

ผ่าน `fare_class_key`

### DIM_FLIGHT_STATUS

เชื่อมกับ

- `fact_flight_operations`

ผ่าน `status_key`

โครงสร้างดังกล่าวทำให้ Dimension หลายตารางสามารถถูกใช้ร่วมกันระหว่าง Fact Table และสนับสนุนการวิเคราะห์ข้อมูลแบบหลายมิติ

---

# 9. Business Question Mapping

| Business Question | Fact Table | Dimension หลัก | Measure |
|---|---|---|---|
| Q1 ยอดขายตั๋วรวมเป็นเท่าใด | fact_ticket_sales | - | amount |
| Q2 จำนวน Ticket Flight ทั้งหมดเท่าใด | fact_ticket_sales | - | ticket_flight_count |
| Q3 Fare Class ใดสร้างยอดขายสูงที่สุด | fact_ticket_sales | dim_fare_class | amount |
| Q4 Fare Class ใดมีจำนวน Ticket Flight มากที่สุด | fact_ticket_sales | dim_fare_class | ticket_flight_count |
| Q5 ยอดขายตั๋วเปลี่ยนแปลงอย่างไรตามช่วงเวลา | fact_ticket_sales | dim_date | amount |
| Q6 สนามบินต้นทางใดมีจำนวน Ticket Flight มากที่สุด | fact_ticket_sales | dim_airport | ticket_flight_count |
| Q7 สนามบินปลายทางใดมีจำนวน Ticket Flight มากที่สุด | fact_ticket_sales | dim_airport | ticket_flight_count |
| Q8 เส้นทางต้นทาง–ปลายทางใดมีจำนวน Ticket Flight มากที่สุด | fact_ticket_sales | dim_airport | ticket_flight_count |
| Q9 เส้นทางใดสร้างยอดขายตั๋วสูงที่สุด | fact_ticket_sales | dim_airport | amount |
| Q10 Aircraft Model ใดถูกใช้กับเที่ยวบินมากที่สุด | fact_flight_operations | dim_aircraft | flight_count |
| Q11 Aircraft Model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด | fact_seat_inventory | dim_aircraft | seat_count |
| Q12 Aircraft Model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร | fact_seat_inventory | dim_aircraft, dim_fare_class | seat_count |
| Q13 Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด | fact_flight_operations | dim_flight_status | flight_count |
| Q14 สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด | fact_flight_operations | dim_airport | departure_delay_minutes |
| Q15 ในแต่ละช่วงเวลา เส้นทางต้นทาง–ปลายทางและ Fare Class ใดสร้างยอดขายตั๋วสูงที่สุด | fact_ticket_sales | dim_date, dim_airport, dim_fare_class | amount |

Business Question ทั้ง 15 ข้อสามารถตอบได้จาก Fact และ Dimension ที่ออกแบบไว้ใน Data Warehouse

---

# 10. สรุป

Airline Data Warehouse ถูกออกแบบในรูปแบบ **Galaxy Schema** ซึ่งประกอบด้วย Dimension Table จำนวน 5 ตาราง และ Fact Table จำนวน 3 ตาราง

Dimension Table ประกอบด้วย

- `dim_date`
- `dim_airport`
- `dim_aircraft`
- `dim_fare_class`
- `dim_flight_status`

Fact Table ประกอบด้วย

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_inventory`

Fact Table แต่ละตารางมี Grain ที่กำหนดไว้อย่างชัดเจน และถูกออกแบบให้รองรับ Business Question ที่แตกต่างกัน

Dimension หลายตารางถูกใช้ร่วมกันระหว่าง Fact Table ทำให้สามารถวิเคราะห์ข้อมูลในมุมมองต่าง ๆ เช่น เวลา สนามบิน เครื่องบิน ชั้นโดยสาร และสถานะเที่ยวบินได้อย่างสอดคล้องกัน

การออกแบบนี้รองรับการวิเคราะห์ข้อมูลด้านยอดขายตั๋ว การดำเนินงานเที่ยวบิน และโครงสร้างที่นั่ง รวมทั้งรองรับการวิเคราะห์แบบหลายมิติผ่าน Galaxy Schema
