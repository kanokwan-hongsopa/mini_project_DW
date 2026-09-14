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

โปรเจกต์ใช้รูปแบบ Galaxy Schema

Dimension Tables
dim_date
dim_airport
dim_aircraft
dim_fare_class
dim_flight_status
Fact Tables
fact_ticket_sales
fact_flight_operations
fact_seat_inventory
<img width="2205" height="1661" alt="Untitled Diagram drawio (25)" src="https://github.com/user-attachments/assets/d980e549-26cd-4dfc-89ed-e4b6e11e1b0b" />


