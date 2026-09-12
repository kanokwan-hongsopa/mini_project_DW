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