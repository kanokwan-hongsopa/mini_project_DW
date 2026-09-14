# 05 การวิเคราะห์เชิงธุรกิจ (Business Insights)

## ภาพรวม

เอกสารนี้นำเสนอผลการวิเคราะห์เชิงธุรกิจจาก Airline Data Warehouse โดยใช้ข้อมูลจาก Fact Table ได้แก่ `fact_ticket_sales`, `fact_flight_operations` และ `fact_seat_inventory` ร่วมกับ Dimension ที่เกี่ยวข้อง ได้แก่ `dim_date`, `dim_airport`, `dim_aircraft`, `dim_fare_class` และ `dim_flight_status`

การวิเคราะห์ครอบคลุมคำถามทางธุรกิจข้อที่ 1–15 โดยมุ่งเน้นการวิเคราะห์ยอดขายตั๋ว จำนวน Ticket Flight ประสิทธิภาพของแต่ละ Fare Class แนวโน้มยอดขายตามช่วงเวลา กิจกรรมของสนามบิน เส้นทางการบิน การใช้งานเครื่องบิน จำนวนและสัดส่วนที่นั่ง สถานะเที่ยวบิน และความล่าช้าของเที่ยวบิน

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

## 9. เส้นทางใดสร้างยอดขายตั๋วสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- Measure: `amount`
- บทบาทของ Dimension:
  - Departure Airport
  - Arrival Airport

### ผลการวิเคราะห์

**DME → KHV**

- ต้นทาง: Domodedovo International Airport
- ปลายทาง: Khabarovsk-Novy Airport
- ยอดขายตั๋วรวม: **753,478,300**

เส้นทางที่มียอดขายรองลงมาคือ **KHV → DME** โดยมียอดขายรวม **733,797,800**

### Business Insight
เส้นทาง **DME → KHV** สร้างยอดขายตั๋วสูงที่สุดในข้อมูลที่นำมาวิเคราะห์ ขณะเดียวกันเส้นทางย้อนกลับ **KHV → DME** ก็มียอดขายอยู่ในระดับสูง

จึงแสดงให้เห็นว่าเส้นทางระหว่าง DME และ KHV เป็นเส้นทางที่มีความสำคัญในด้านรายได้ของข้อมูลชุดนี้

---

## 10. Aircraft Model ใดถูกใช้กับเที่ยวบินมากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- Dimension: `dim_aircraft`
- Measure: `flight_count`

### ผลการวิเคราะห์

| Aircraft Model | จำนวนเที่ยวบิน |
|---|---:|
| Cessna 208 Caravan | 9,273 |
| Bombardier CRJ-200 | 9,048 |
| Sukhoi Superjet-100 | 8,504 |

### Business Insight
**Cessna 208 Caravan (CN1)** เป็น Aircraft Model ที่ถูกใช้กับเที่ยวบินมากที่สุด โดยมีจำนวน **9,273 เที่ยวบิน**

รองลงมาคือ Bombardier CRJ-200 จำนวน 9,048 เที่ยวบิน และ Sukhoi Superjet-100 จำนวน 8,504 เที่ยวบิน

ผลการวิเคราะห์แสดงให้เห็นว่า Cessna 208 Caravan มีการใช้งานสูงที่สุดในชุดข้อมูล ซึ่งสามารถนำไปใช้ประกอบการวิเคราะห์การใช้งานเครื่องบินและการวางแผนด้านการบำรุงรักษาได้

---

## 11. Aircraft Model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด?

### ข้อมูลที่ใช้
- Fact Table: `fact_seat_inventory`
- Dimension: `dim_aircraft`
- Measure: `seat_count`

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
**Boeing 777-300** มีจำนวนที่นั่งสูงที่สุด โดยมี **402 ที่นั่ง** ขณะที่ **Cessna 208 Caravan** มีจำนวนที่นั่งน้อยที่สุด คือ **12 ที่นั่ง**

ผลลัพธ์แสดงให้เห็นถึงความแตกต่างด้านความจุของ Aircraft แต่ละรุ่น ซึ่งสามารถใช้ประกอบการวิเคราะห์ความเหมาะสมของเครื่องบินกับความต้องการของแต่ละเส้นทางได้

---

## 12. Aircraft Model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร?

### ข้อมูลที่ใช้
- Fact Table: `fact_seat_inventory`
- Dimension:
  - `dim_aircraft`
  - `dim_fare_class`
- Measure: `seat_count`
- ค่าที่คำนวณเพิ่มเติม: `seat_percentage`

### ผลการวิเคราะห์

โดยรวมพบว่า **Economy เป็น Fare Class ที่มีสัดส่วนที่นั่งสูงที่สุดใน Aircraft ทุก Model**

ตัวอย่างสัดส่วนที่สำคัญ:

| Aircraft Model | Fare Class | จำนวนที่นั่ง | สัดส่วน |
|---|---|---:|---:|
| Boeing 777-300 | Economy | 324 | 80.60% |
| Boeing 777-300 | Comfort | 48 | 11.94% |
| Boeing 777-300 | Business | 30 | 7.46% |
| Boeing 767-300 | Economy | 192 | 86.49% |
| Boeing 767-300 | Business | 30 | 13.51% |
| Boeing 737-300 | Economy | 118 | 90.77% |
| Boeing 737-300 | Business | 12 | 9.23% |
| Bombardier CRJ-200 | Economy | 50 | 100.00% |
| Cessna 208 Caravan | Economy | 12 | 100.00% |

### Business Insight
Economy เป็น Fare Class หลักของ Aircraft ทุก Model ในข้อมูลที่นำมาวิเคราะห์

ขณะที่ **Boeing 777-300** มีการจัดสรรที่นั่งหลากหลายที่สุด โดยประกอบด้วย Economy, Comfort และ Business ซึ่งแสดงให้เห็นถึงการรองรับผู้โดยสารหลายระดับบริการในเครื่องบินรุ่นดังกล่าว

---

## 13. Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- Dimension: `dim_flight_status`
- Measure: `flight_count`

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
สถานะ **Arrived** มีจำนวนมากที่สุด โดยมี **16,707 เที่ยวบิน** รองลงมาคือ Scheduled จำนวน **15,383 เที่ยวบิน**

ส่วนสถานะ Delayed มีจำนวน **41 เที่ยวบิน** ผลการวิเคราะห์สถานะเที่ยวบินช่วยให้เห็นภาพรวมของสถานะการดำเนินงานของเที่ยวบินที่จัดเก็บอยู่ใน Data Warehouse

---

## 14. สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- Dimension: `dim_airport`
- Measure: `departure_delay_minutes`
- บทบาทของ Dimension: Departure Airport
- เงื่อนไขการวิเคราะห์: `departure_delay_minutes > 0`

### ผลการวิเคราะห์

| Airport | เมือง | ความล่าช้าเฉลี่ย (นาที) | จำนวนเที่ยวบินที่ล่าช้า |
|---|---|---:|---:|
| ULY — Ulyanovsk East Airport | Ulyanovsk | 25.73 | 92 |
| BQS — Ignatyevo Airport | Blagoveschensk | 24.38 | 29 |
| LPK — Lipetsk Airport | Lipetsk | 22.68 | 22 |

### Business Insight
เมื่อพิจารณาเฉพาะเที่ยวบินที่มีความล่าช้ามากกว่า 0 นาที พบว่า **ULY — Ulyanovsk East Airport** มีเวลาออกเดินทางล่าช้าเฉลี่ยสูงที่สุดที่ **25.73 นาที** จากเที่ยวบินที่ล่าช้า **92 เที่ยวบิน**

จึงเป็นสนามบินที่มีค่าความล่าช้าเฉลี่ยสูงที่สุดตามเงื่อนไขของการวิเคราะห์ และสามารถนำไปใช้เป็นจุดเริ่มต้นสำหรับการวิเคราะห์สาเหตุของความล่าช้าเพิ่มเติมได้

---

## 15. ในแต่ละช่วงเวลา เส้นทางต้นทาง–ปลายทางและ Fare Class ใดสร้างยอดขายตั๋วสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension:
  - `dim_date`
  - `dim_airport`
  - `dim_fare_class`
- Measure: `amount`
- บทบาทของ `dim_airport`:
  - Departure Airport
  - Arrival Airport

### ผลการวิเคราะห์

| ช่วงเวลา | เส้นทาง | Fare Class | ยอดขายตั๋ว |
|---|---|---|---:|
| กรกฎาคม 2017 | DME → KHV | Economy | 144,234,400 |
| สิงหาคม 2017 | DME → KHV | Economy | 335,543,100 |
| กันยายน 2017 | KHV → DME | Economy | 60,210,500 |

### Business Insight
ในทั้งสามเดือน **Economy เป็น Fare Class ที่สร้างยอดขายสูงที่สุดในเส้นทางอันดับหนึ่งของแต่ละเดือน**

เส้นทาง **DME → KHV** มีรายได้สูงที่สุดในเดือนกรกฎาคมและสิงหาคม โดยเฉพาะเดือนสิงหาคมที่มียอดขาย **335,543,100** ขณะที่เดือนกันยายนเส้นทาง **KHV → DME** มียอดขายสูงที่สุดที่ **60,210,500**

ผลการวิเคราะห์แสดงให้เห็นว่าเส้นทางระหว่าง DME และ KHV มีความสำคัญต่อยอดขายตั๋วในช่วงเวลาที่นำมาวิเคราะห์

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
| Q9 เส้นทางที่สร้างยอดขายสูงที่สุด | DME → KHV — 753,478,300 |
| Q10 Aircraft Model ที่ถูกใช้มากที่สุด | Cessna 208 Caravan — 9,273 เที่ยวบิน |
| Q11 Aircraft Model ที่มีจำนวนที่นั่งมากที่สุด | Boeing 777-300 — 402 ที่นั่ง |
| Q12 ภาพรวมสัดส่วน Fare Class | Economy มีสัดส่วนที่นั่งสูงที่สุดใน Aircraft ทุก Model |
| Q13 Flight Status ที่มีจำนวนมากที่สุด | Arrived — 16,707 เที่ยวบิน |
| Q14 สนามบินที่มีความล่าช้าเฉลี่ยสูงที่สุด | ULY — 25.73 นาที |
| Q15 เส้นทางและ Fare Class ที่สร้างยอดขายสูงสุดรายเดือน | ก.ค. DME → KHV Economy, ส.ค. DME → KHV Economy, ก.ย. KHV → DME Economy |

## บทสรุป

จากการวิเคราะห์คำถามทางธุรกิจทั้ง 15 ข้อ พบว่า **Economy Class มีบทบาทสำคัญในข้อมูลชุดนี้** โดยมีทั้งยอดขายรวมและจำนวน Ticket Flight สูงที่สุด รวมถึงเป็น Fare Class ที่มีสัดส่วนที่นั่งสูงที่สุดใน Aircraft ทุก Model

เมื่อวิเคราะห์ตามช่วงเวลา พบว่า **เดือนสิงหาคม 2017** มียอดขายตั๋วรวมสูงที่สุดในช่วงข้อมูลที่นำมาวิเคราะห์ ขณะที่การวิเคราะห์ยอดขายแยกตามเดือน เส้นทาง และ Fare Class พบว่าเส้นทาง **DME → KHV ใน Economy Class** สร้างยอดขายสูงที่สุดในเดือนกรกฎาคมและสิงหาคม ส่วนเดือนกันยายนเป็น **KHV → DME ใน Economy Class**

ในด้านสนามบิน **SVO (Sheremetyevo International Airport)** มีจำนวน Ticket Flight สูงที่สุดทั้งในฐานะสนามบินต้นทางและสนามบินปลายทาง และเส้นทาง **SVO → LED** เป็นเส้นทางที่มีจำนวน Ticket Flight สูงที่สุด ขณะที่เมื่อพิจารณาด้านยอดขาย เส้นทาง **DME → KHV** สร้างยอดขายตั๋วสูงที่สุด

ด้านการดำเนินงานของเที่ยวบิน พบว่า **Cessna 208 Caravan** เป็น Aircraft Model ที่ถูกใช้กับเที่ยวบินมากที่สุด ขณะที่ **Boeing 777-300** มีจำนวนที่นั่งมากที่สุด สำหรับสถานะเที่ยวบิน พบว่า Arrived เป็นสถานะที่มีจำนวนมากที่สุด และเมื่อวิเคราะห์เฉพาะเที่ยวบินที่ออกเดินทางล่าช้า พบว่า **ULY — Ulyanovsk East Airport** มีความล่าช้าเฉลี่ยสูงที่สุดที่ 25.73 นาที

ผลการวิเคราะห์ทั้งหมดแสดงให้เห็นว่า Airline Data Warehouse สามารถใช้วิเคราะห์ข้อมูลได้หลายมิติ ทั้งด้านยอดขาย Fare Class ช่วงเวลา สนามบิน เส้นทาง Aircraft จำนวนที่นั่ง สถานะเที่ยวบิน และความล่าช้า เพื่อสนับสนุนการวิเคราะห์ข้อมูลเชิงธุรกิจและการตัดสินใจได้
