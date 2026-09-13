# 02 - พจนานุกรมข้อมูล (Data Dictionary)

## BOOKINGS

**ระดับข้อมูล (Grain):** 1 แถว แทนการจอง 1 รายการ

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| book_ref | VARCHAR | PK | รหัสอ้างอิงการจอง |
| book_date | TIMESTAMP | - | วันที่และเวลาที่ทำรายการจอง |
| total_amount | DECIMAL(18,2) | - | ยอดรวมของรายการจอง |

---

## TICKETS

**ระดับข้อมูล (Grain):** 1 แถว แทนตั๋วโดยสาร 1 ใบ

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| ticket_no | VARCHAR | PK | หมายเลขตั๋วโดยสาร |
| book_ref | VARCHAR | FK | รหัสการจองที่เชื่อมโยงกับตาราง bookings |
| passenger_id | VARCHAR | - | รหัสผู้โดยสาร |

ความสัมพันธ์:

`book_ref → bookings.book_ref`

---

## TICKET_FLIGHTS

**ระดับข้อมูล (Grain):** 1 แถว แทนตั๋ว 1 ใบสำหรับเที่ยวบิน 1 ช่วง

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| ticket_no | VARCHAR | PK, FK | หมายเลขตั๋วโดยสาร |
| flight_id | INTEGER | PK, FK | รหัสเที่ยวบิน |
| fare_conditions | VARCHAR | - | ประเภทชั้นโดยสาร เช่น Economy, Comfort หรือ Business |
| amount | DECIMAL(18,2) | - | ราคาตั๋วสำหรับเที่ยวบินช่วงนั้น |

Composite Primary Key:

`ticket_no + flight_id`

ความสัมพันธ์:

- `ticket_no → tickets.ticket_no`
- `flight_id → flights.flight_id`
---

## FLIGHTS

**ระดับข้อมูล (Grain):** 1 แถว แทนเที่ยวบิน 1 เที่ยว

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| flight_id | INTEGER | PK | รหัสเที่ยวบิน |
| flight_no | VARCHAR | - | หมายเลขเที่ยวบิน |
| scheduled_departure | TIMESTAMP | - | วันและเวลาออกเดินทางตามกำหนด |
| scheduled_arrival | TIMESTAMP | - | วันและเวลาถึงตามกำหนด |
| departure_airport | VARCHAR | FK | รหัสสนามบินต้นทาง |
| arrival_airport | VARCHAR | FK | รหัสสนามบินปลายทาง |
| status | VARCHAR | - | สถานะของเที่ยวบิน |
| aircraft_code | VARCHAR | FK | รหัสเครื่องบินที่ใช้ในเที่ยวบิน |
| actual_departure | TIMESTAMP | - | วันและเวลาออกเดินทางจริง |
| actual_arrival | TIMESTAMP | - | วันและเวลาถึงจริง |

ความสัมพันธ์:

- `departure_airport → airports_data.airport_code`
- `arrival_airport → airports_data.airport_code`
- `aircraft_code → aircrafts_data.aircraft_code`

---

## BOARDING_PASSES

**ระดับข้อมูล (Grain):** 1 แถว แทน Boarding Pass ของตั๋ว 1 ใบในเที่ยวบิน 1 เที่ยว

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| ticket_no | VARCHAR | PK, FK | หมายเลขตั๋วโดยสาร |
| flight_id | INTEGER | PK, FK | รหัสเที่ยวบิน |
| boarding_no | INTEGER | - | ลำดับการขึ้นเครื่อง |
| seat_no | VARCHAR | - | หมายเลขที่นั่งของผู้โดยสาร |

Composite Primary Key:

`ticket_no + flight_id`

ความสัมพันธ์:

- `(ticket_no, flight_id) → ticket_flights.(ticket_no, flight_id)`

---

## AIRPORTS_DATA

**ระดับข้อมูล (Grain):** 1 แถว แทนสนามบิน 1 แห่ง

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| airport_code | VARCHAR | PK | รหัสสนามบิน |
| airport_name | VARCHAR | - | ชื่อสนามบิน |
| city | VARCHAR | - | เมืองที่สนามบินตั้งอยู่ |
| coordinates | VARCHAR | - | พิกัดตำแหน่งของสนามบิน |
| timezone | VARCHAR | - | เขตเวลาของสนามบิน |

---

## AIRCRAFTS_DATA

**ระดับข้อมูล (Grain):** 1 แถว แทนเครื่องบิน 1 รุ่น/รหัสเครื่องบิน

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| aircraft_code | VARCHAR | PK | รหัสเครื่องบิน |
| model | VARCHAR | - | รุ่นของเครื่องบิน |
| range | INTEGER | - | ระยะทางสูงสุดที่เครื่องบินสามารถบินได้ |

---

## SEATS

**ระดับข้อมูล (Grain):** 1 แถว แทนที่นั่ง 1 ที่นั่งของเครื่องบินแต่ละรหัส

| ชื่อคอลัมน์ | ชนิดข้อมูล | Key | คำอธิบาย |
|---|---|---|---|
| aircraft_code | VARCHAR | PK, FK | รหัสเครื่องบิน |
| seat_no | VARCHAR | PK | หมายเลขที่นั่ง |
| fare_conditions | VARCHAR | - | ประเภทชั้นโดยสาร เช่น Economy, Comfort หรือ Business |

Composite Primary Key:

`aircraft_code + seat_no`

ความสัมพันธ์:

- `aircraft_code → aircrafts_data.aircraft_code`

---

## สรุปความสัมพันธ์ระหว่างตาราง

- `bookings.book_ref → tickets.book_ref`
- `tickets.ticket_no → ticket_flights.ticket_no`
- `flights.flight_id → ticket_flights.flight_id`
- `ticket_flights.(ticket_no, flight_id) → boarding_passes.(ticket_no, flight_id)`
- `airports_data.airport_code → flights.departure_airport`
- `airports_data.airport_code → flights.arrival_airport`
- `aircrafts_data.aircraft_code → flights.aircraft_code`
- `aircrafts_data.aircraft_code → seats.aircraft_code`