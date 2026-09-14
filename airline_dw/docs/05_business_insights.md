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
## Q9: เส้นทางใดสร้างยอดขายตั๋วสูงที่สุด?

**Fact ที่ใช้:** `fact_ticket_sales`  
**Dimension ที่ใช้:** `dim_airport`
**Measure ที่ใช้:** `SUM(amount)` – ยอดขายตั๋วรวมของแต่ละเส้นทาง

### ผลการวิเคราะห์
เส้นทาง **DME → KHV** จาก Domodedovo International Airport ไปยัง Khabarovsk-Novy Airport สร้างยอดขายตั๋วสูงที่สุด โดยมียอดขายรวม **753,478,300**

เส้นทางที่มียอดขายรองลงมาคือ **KHV → DME** ซึ่งมียอดขายรวม **733,797,800**

### Business Insight
เส้นทางระหว่าง DME และ KHV เป็นเส้นทางที่มีความสำคัญด้านรายได้ โดยเฉพาะเส้นทาง DME → KHV ที่สร้างยอดขายสูงที่สุดในชุดข้อมูล จึงเป็นเส้นทางที่ควรให้ความสำคัญในการวางแผนด้านการขายและการให้บริการ

---

## Q10: Aircraft Model ใดถูกใช้กับเที่ยวบินมากที่สุด?

**Fact ที่ใช้:** `fact_flight_operations`  
**Dimension ที่ใช้:** `dim_aircraft`
**Measure ที่ใช้:** `SUM(flight_count)` – จำนวนเที่ยวบินทั้งหมดของ Aircraft แต่ละรุ่น

### ผลการวิเคราะห์
เครื่องบินรุ่น **Cessna 208 Caravan (CN1)** ถูกใช้กับเที่ยวบินมากที่สุด จำนวน **9,273 เที่ยวบิน**

รองลงมาคือ:
- Bombardier CRJ-200 จำนวน 9,048 เที่ยวบิน
- Sukhoi Superjet-100 จำนวน 8,504 เที่ยวบิน

### Business Insight
Cessna 208 Caravan เป็นเครื่องบินที่มีจำนวนการใช้งานสูงที่สุดในชุดข้อมูล แสดงให้เห็นว่าเครื่องบินรุ่นนี้มีบทบาทสำคัญต่อการดำเนินงานของเที่ยวบิน และอาจต้องให้ความสำคัญกับการวางแผนการใช้งานและการบำรุงรักษา

---

## Q11: Aircraft Model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด?

**Fact ที่ใช้:** `fact_seat_inventory`  
**Dimension ที่ใช้:** `dim_aircraft`
**Measure ที่ใช้:** `SUM(seat_count)` – จำนวนที่นั่งทั้งหมดของ Aircraft แต่ละรุ่น

### ผลการวิเคราะห์

| Aircraft Model | จำนวนที่นั่ง |
|---|---:|
| Boeing 777-300 | 402 |
| Boeing 767-300 | 222 |
| Airbus A321-200 | 170 |
| Airbus A320-200 | 140 |
| Boeing 737-300 | 130 |
| Airbus A319-100 | 116 |
| Sukhoi Superjet-100 | 97 |
| Bombardier CRJ-200 | 50 |
| Cessna 208 Caravan | 12 |

### Business Insight
**Boeing 777-300** มีความจุสูงที่สุด จำนวน **402 ที่นั่ง** ขณะที่ **Cessna 208 Caravan** มีความจุน้อยที่สุด จำนวน **12 ที่นั่ง** แสดงให้เห็นถึงความแตกต่างของขนาดและความจุของเครื่องบินแต่ละรุ่น ซึ่งสามารถนำไปใช้ประกอบการวางแผนเลือกเครื่องบินให้เหมาะสมกับความต้องการของแต่ละเส้นทาง

---

## Q12: Aircraft Model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร?

**Fact ที่ใช้:** `fact_seat_inventory`  
**Dimension ที่ใช้:** `dim_aircraft`, `dim_fare_class`
**Measure ที่ใช้:** `SUM(seat_count)` และ `seat_percentage` – จำนวนและสัดส่วนที่นั่งของแต่ละ Fare Class

### ผลการวิเคราะห์
โดยรวมพบว่า **Economy เป็น Fare Class ที่มีสัดส่วนที่นั่งสูงที่สุดในเครื่องบินทุกแบบ**

ตัวอย่างที่สำคัญ:
- Boeing 777-300: Economy 80.60%, Comfort 11.94%, Business 7.46%
- Boeing 767-300: Economy 86.49%, Business 13.51%
- Boeing 737-300: Economy 90.77%, Business 9.23%
- Bombardier CRJ-200: Economy 100%
- Cessna 208 Caravan: Economy 100%

### Business Insight
Economy เป็นชั้นโดยสารหลักของเครื่องบินทุกแบบในชุดข้อมูล ขณะที่ Boeing 777-300 มีการจัดสรรที่นั่งหลากหลายที่สุด โดยมีทั้ง Economy, Comfort และ Business สะท้อนให้เห็นถึงการรองรับผู้โดยสารหลายระดับบริการในเครื่องบินที่มีความจุสูง

---

## Q13: Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด?

**Fact ที่ใช้:** `fact_flight_operations`  
**Dimension ที่ใช้:** `dim_flight_status`
**Measure ที่ใช้:** `SUM(flight_count)` – จำนวนเที่ยวบินในแต่ละสถานะ

### ผลการวิเคราะห์

| Flight Status | จำนวนเที่ยวบิน |
|---|---:|
| Arrived | 16,707 |
| Scheduled | 15,383 |
| On Time | 518 |
| Cancelled | 414 |
| Departed | 58 |
| Delayed | 41 |

### Business Insight
สถานะ **Arrived** มีจำนวนมากที่สุดที่ **16,707 เที่ยวบิน** รองลงมาคือ Scheduled จำนวน 15,383 เที่ยวบิน ขณะที่สถานะ Delayed มีจำนวน 41 เที่ยวบิน การวิเคราะห์สถานะเหล่านี้ช่วยให้เห็นภาพรวมของการดำเนินงานของเที่ยวบินในชุดข้อมูล

---

## Q14: สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด?

**Fact ที่ใช้:** `fact_flight_operations`  
**Dimension ที่ใช้:** `dim_airport`
**Measure ที่ใช้:** `AVG(departure_delay_minutes)` และ `COUNT(*)` – ค่าเฉลี่ยเวลาล่าช้าและจำนวนเที่ยวบินที่ล่าช้า

### ผลการวิเคราะห์
เมื่อพิจารณาเฉพาะเที่ยวบินที่มี `departure_delay_minutes > 0` พบว่า **ULY – Ulyanovsk East Airport** มีเวลาออกเดินทางล่าช้าเฉลี่ยสูงที่สุดที่ **25.73 นาที** จากเที่ยวบินที่ล่าช้า **92 เที่ยวบิน**

รองลงมาคือ:
- BQS – Ignatyevo Airport: 24.38 นาที
- LPK – Lipetsk Airport: 22.68 นาที

### Business Insight
Ulyanovsk East Airport มีค่าเฉลี่ยความล่าช้าในการออกเดินทางสูงที่สุดในกลุ่มเที่ยวบินที่เกิดความล่าช้า จึงเป็นสนามบินที่ควรได้รับความสนใจในการวิเคราะห์สาเหตุของความล่าช้าและการปรับปรุงประสิทธิภาพการดำเนินงาน

---

## Q15: ในแต่ละช่วงเวลา เส้นทางต้นทาง–ปลายทางและ Fare Class ใดสร้างยอดขายตั๋วสูงที่สุด?

**Fact ที่ใช้:** `fact_ticket_sales`  
**Dimension ที่ใช้:** `dim_date`, `dim_airport`, `dim_fare_class`
**Measure ที่ใช้:** `SUM(amount)` – ยอดขายตั๋วรวมตามเดือน เส้นทาง และ Fare Class

### ผลการวิเคราะห์

| ช่วงเวลา | เส้นทาง | Fare Class | ยอดขายตั๋ว |
|---|---|---|---:|
| July 2017 | DME → KHV | Economy | 144,234,400 |
| August 2017 | DME → KHV | Economy | 335,543,100 |
| September 2017 | KHV → DME | Economy | 60,210,500 |

### Business Insight
ในทั้งสามเดือน **Economy เป็น Fare Class ที่สร้างยอดขายสูงที่สุดในเส้นทางอันดับหนึ่งของแต่ละเดือน**

เส้นทาง **DME → KHV** ครองอันดับหนึ่งในเดือน July และ August โดยเฉพาะ August ที่มียอดขายสูงถึง **335,543,100** ส่วน September เปลี่ยนเป็นเส้นทาง **KHV → DME** ที่มียอดขายสูงที่สุด **60,210,500**

ผลดังกล่าวแสดงให้เห็นว่าเส้นทางระหว่าง DME และ KHV มีความสำคัญต่อยอดขายตั๋วในช่วงเวลาที่วิเคราะห์
