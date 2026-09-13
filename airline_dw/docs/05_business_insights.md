# 05 การวิเคราะห์เชิงธุรกิจ (Business Insights)

## ภาพรวม

เอกสารนี้นำเสนอผลการวิเคราะห์เชิงธุรกิจจาก Airline Data Warehouse โดยใช้ข้อมูลจาก `fact_ticket_sales` ร่วมกับ Dimension ที่เกี่ยวข้อง ได้แก่ `dim_date`, `dim_airport` และ `dim_fare_class`

การวิเคราะห์ครอบคลุมคำถามทางธุรกิจข้อที่ 1–8 โดยมุ่งเน้นการวิเคราะห์ยอดขายตั๋ว จำนวน Ticket Flight ประสิทธิภาพของแต่ละ Fare Class แนวโน้มยอดขายตามช่วงเวลา กิจกรรมของสนามบิน และเส้นทางการบินที่ได้รับความนิยม

---

## 1. ยอดขายตั๋วรวมเป็นเท่าใด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Measure: `amount`

### ผลการวิเคราะห์
**ยอดขายตั๋วรวม = 20,766,980,900**

### Business Insight
จากข้อมูลใน Data Warehouse พบว่ายอดขายตั๋วรวมทั้งหมดเท่ากับ **20,766,980,900**

ค่านี้แสดงถึงยอดขายรวมที่เกิดจากรายการ Ticket Flight ทั้งหมดที่ถูกจัดเก็บอยู่ใน Data Warehouse

---

## 2. จำนวน Ticket Flight ทั้งหมดเท่าใด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Measure: `ticket_flight_count`

### ผลการวิเคราะห์
**จำนวน Ticket Flight ทั้งหมด = 1,045,726 รายการ**

### Business Insight
จากข้อมูลพบว่ามี Ticket Flight ทั้งหมด **1,045,726 รายการ**

โดย Grain ของ `fact_ticket_sales` กำหนดให้ 1 แถวแทน 1 Ticket × 1 Flight Segment ดังนั้นจึงสามารถรวมค่า `ticket_flight_count` เพื่อหาจำนวนรายการ Ticket Flight ทั้งหมดได้

---

## 3. Fare Class ใดสร้างยอดขายสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_fare_class`
- Measure: `amount`

### ผลการวิเคราะห์

| Fare Class | ยอดขายรวม |
|---|---:|
| Economy | 14,695,684,400 |
| Business | 5,505,179,600 |
| Comfort | 566,116,900 |

### Business Insight
**Economy Class สร้างยอดขายสูงที่สุด** โดยมียอดขายรวม **14,695,684,400**

ผลการวิเคราะห์แสดงให้เห็นว่า Economy เป็น Fare Class ที่มีบทบาทสำคัญต่อยอดขายรวม เนื่องจากมีจำนวน Ticket Flight สูงกว่ากลุ่มอื่นอย่างมาก

---

## 4. Fare Class ใดมีจำนวน Ticket Flight มากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_fare_class`
- Measure: `ticket_flight_count`

### ผลการวิเคราะห์

| Fare Class | จำนวน Ticket Flight |
|---|---:|
| Economy | 920,793 |
| Business | 107,642 |
| Comfort | 17,291 |

### Business Insight
**Economy Class มีจำนวน Ticket Flight มากที่สุด** โดยมีจำนวนทั้งหมด **920,793 รายการ**

จึงสามารถสรุปได้ว่า Economy เป็น Fare Class หลักในด้านปริมาณ Ticket Flight ของข้อมูลชุดนี้

---

## 5. ยอดขายตั๋วเปลี่ยนแปลงอย่างไรตามช่วงเวลา?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_date`
- Measure: `amount`

### ผลการวิเคราะห์

| ปี | เดือน | ยอดขายรวม |
|---|---|---:|
| 2017 | กรกฎาคม | 4,983,243,300 |
| 2017 | สิงหาคม | 13,509,694,600 |
| 2017 | กันยายน | 2,274,043,000 |

### Business Insight
ยอดขายตั๋วสูงที่สุดในช่วงข้อมูลที่นำมาวิเคราะห์คือ **เดือนสิงหาคม 2017** โดยมียอดขายรวม **13,509,694,600**

เดือนกรกฎาคมมียอดขาย **4,983,243,300** และเดือนกันยายนมียอดขาย **2,274,043,000**

ผลลัพธ์แสดงให้เห็นว่ายอดขายมีความแตกต่างกันอย่างชัดเจนในแต่ละเดือน อย่างไรก็ตาม ข้อมูลเพียงส่วนนี้ยังไม่สามารถระบุสาเหตุของการเพิ่มขึ้นหรือลดลงของยอดขายได้ และช่วงข้อมูลของแต่ละเดือนอาจไม่ได้ครอบคลุมจำนวนวันเท่ากันทั้งหมด

---

## 6. สนามบินต้นทางใดมีจำนวน Ticket Flight มากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- Measure: `ticket_flight_count`
- บทบาทของ Dimension: Departure Airport

### ผลการวิเคราะห์
**SVO — Sheremetyevo International Airport, Moscow**

**จำนวน Ticket Flight = 155,073 รายการ**

### Business Insight
สนามบิน **SVO (Sheremetyevo International Airport)** มีจำนวน Ticket Flight ขาออกสูงที่สุด โดยมีทั้งหมด **155,073 รายการ**

จึงเป็นสนามบินต้นทางที่มีปริมาณ Ticket Flight สูงที่สุดในข้อมูลที่นำมาวิเคราะห์

---

## 7. สนามบินปลายทางใดมีจำนวน Ticket Flight มากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- Measure: `ticket_flight_count`
- บทบาทของ Dimension: Arrival Airport

### ผลการวิเคราะห์
**SVO — Sheremetyevo International Airport, Moscow**

**จำนวน Ticket Flight = 150,086 รายการ**

### Business Insight
สนามบิน **SVO (Sheremetyevo International Airport)** มีจำนวน Ticket Flight ขาเข้าสูงที่สุด โดยมีทั้งหมด **150,086 รายการ**

เมื่อพิจารณาร่วมกับผลการวิเคราะห์ข้อที่ 6 จะเห็นว่า SVO มีปริมาณ Ticket Flight สูงทั้งในบทบาทสนามบินต้นทางและสนามบินปลายทาง

---

## 8. เส้นทางต้นทาง–ปลายทางใดมีจำนวน Ticket Flight มากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- Measure: `ticket_flight_count`
- บทบาทของ Dimension:
  - Departure Airport
  - Arrival Airport

### ผลการวิเคราะห์

**SVO → LED**

- ต้นทาง: Moscow
- ปลายทาง: St. Petersburg
- จำนวน Ticket Flight: **16,461 รายการ**

### Business Insight
เส้นทางที่มีจำนวน Ticket Flight สูงที่สุดคือ **SVO → LED (Moscow → St. Petersburg)** โดยมีจำนวนทั้งหมด **16,461 รายการ**

ดังนั้นเส้นทาง SVO → LED จึงเป็นเส้นทางแบบมีทิศทางที่มีปริมาณ Ticket Flight สูงที่สุดในข้อมูลที่นำมาวิเคราะห์

---

## สรุปผลการวิเคราะห์เชิงธุรกิจ

| คำถามทางธุรกิจ | ผลลัพธ์สำคัญ |
|---|---|
| Q1 ยอดขายตั๋วรวม | 20,766,980,900 |
| Q2 จำนวน Ticket Flight ทั้งหมด | 1,045,726 |
| Q3 Fare Class ที่มียอดขายสูงที่สุด | Economy — 14,695,684,400 |
| Q4 Fare Class ที่มี Ticket Flight มากที่สุด | Economy — 920,793 |
| Q5 ช่วงเวลาที่มียอดขายสูงที่สุด | สิงหาคม 2017 — 13,509,694,600 |
| Q6 สนามบินต้นทางอันดับ 1 | SVO — 155,073 |
| Q7 สนามบินปลายทางอันดับ 1 | SVO — 150,086 |
| Q8 เส้นทางที่มี Ticket Flight มากที่สุด | SVO → LED — 16,461 |

## บทสรุป

จากการวิเคราะห์พบว่า **Economy Class เป็น Fare Class หลักของข้อมูลชุดนี้** โดยมีทั้งยอดขายรวมและจำนวน Ticket Flight สูงที่สุด

เมื่อวิเคราะห์ตามช่วงเวลา พบว่า **เดือนสิงหาคม 2017** มียอดขายสูงที่สุดในช่วงข้อมูลที่นำมาวิเคราะห์

ในด้านสนามบิน **SVO (Sheremetyevo International Airport)** มีจำนวน Ticket Flight สูงที่สุดทั้งในฐานะสนามบินต้นทางและสนามบินปลายทาง ขณะที่เส้นทาง **SVO → LED (Moscow → St. Petersburg)** เป็นเส้นทางที่มีจำนวน Ticket Flight สูงที่สุด

ผลการวิเคราะห์เหล่านี้แสดงให้เห็นว่า Airline Data Warehouse สามารถนำมาใช้วิเคราะห์ข้อมูลในหลายมิติ เช่น ยอดขาย Fare Class ช่วงเวลา สนามบิน และเส้นทางการบิน เพื่อสนับสนุนการวิเคราะห์ข้อมูลเชิงธุรกิจได้