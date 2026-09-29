# 05 การวิเคราะห์เชิงธุรกิจ (Business Insights)

## ภาพรวม

เอกสารนี้นำเสนอผลการวิเคราะห์เชิงธุรกิจจาก Airline Data Warehouse เวอร์ชันล่าสุด โดยใช้ Fact Table หลัก 3 ตาราง ได้แก่

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_utilization`

ร่วมกับ Dimension ที่เกี่ยวข้อง ได้แก่

- `dim_date`
- `dim_airport`
- `dim_aircraft`
- `dim_fare_class`
- `dim_flight_status`

การวิเคราะห์ครอบคลุม Business Questions Q1–Q15 ชุดล่าสุด โดยแบ่งเป็นคำถามพื้นฐาน Q1–Q11 และ Multidimensional / Challenge Questions Q12–Q15

---

## Q1. เส้นทางใดสร้างรายได้จากการขายตั๋วสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- มิติหลัก: Departure Airport + Arrival Airport
- Measure: `amount`

### ผลการวิเคราะห์

เส้นทางที่สร้างรายได้สูงที่สุดคือ **DME → KHV**

- รายได้รวม: **753,478,300**
- จำนวน Ticket Flight: **9,647**

### Business Insight

DME → KHV เป็นเส้นทางที่สร้างรายได้สูงที่สุดในข้อมูลที่นำมาวิเคราะห์ จึงเป็นเส้นทางสำคัญในด้านรายได้ และสามารถใช้ประกอบการวางแผน Capacity การจัดตารางเที่ยวบิน และการบริหารเส้นทางได้

---

## Q2. Fare Class ใดสร้างรายได้สูงที่สุด และมีสัดส่วนรายได้เท่าใด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_fare_class`
- Measure: `amount`
- ค่าที่คำนวณเพิ่มเติม: Revenue Share

### ผลการวิเคราะห์

| Fare Class | สัดส่วนรายได้ |
|---|---:|
| Economy | 70.76% |
| Business | 26.51% |
| Comfort | 2.73% |

### Business Insight

Economy Class เป็น Fare Class ที่สร้างรายได้สูงที่สุดและมีสัดส่วนรายได้มากที่สุดในข้อมูลชุดนี้ ขณะที่ Business แม้มีจำนวนตั๋วน้อยกว่า แต่ยังสร้างรายได้ในสัดส่วนที่มีนัยสำคัญ

---

## Q3. รายได้จากการขายตั๋วมีแนวโน้มเปลี่ยนแปลงอย่างไรในแต่ละเดือน?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_date`
- Measure: `amount`

### ผลการวิเคราะห์

| เดือน | รายได้รวม |
|---|---:|
| กรกฎาคม 2017 | 4,958,534,400 |
| สิงหาคม 2017 | 13,520,127,500 |
| กันยายน 2017 | 2,288,319,000 |

### Business Insight

รายได้สูงที่สุดอยู่ในเดือนสิงหาคม 2017 ขณะที่เดือนกันยายนมีรายได้ต่ำกว่าอย่างชัดเจน อย่างไรก็ตาม ช่วงข้อมูลของเดือนกันยายนอาจเป็นข้อมูลไม่เต็มเดือน จึงไม่ควรสรุปว่าเป็นเดือนที่มี Demand ต่ำที่สุดโดยไม่ตรวจสอบช่วงวันที่เพิ่มเติม

---

## Q4. ภูมิภาคต้นทาง–ปลายทางคู่ใดมีความต้องการเดินทางสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- มิติหลัก: Departure Region + Arrival Region
- Measure: `ticket_flight_count`

### ผลการวิเคราะห์

คู่ภูมิภาคที่มีความต้องการเดินทางสูงที่สุดคือ **Western Russia → Western Russia**

- จำนวน Ticket Flight: **512,461**

### Business Insight

การเดินทางภายใน Western Russia มีปริมาณ Ticket Flight สูงที่สุดในข้อมูลชุดนี้ แสดงให้เห็นถึง Demand ภายในภูมิภาคที่เด่นชัด และสามารถใช้ประกอบการวางแผน Network และการจัดสรรเที่ยวบินได้

---

## Q5. เส้นทางใดมีอัตราการใช้ที่นั่งของผู้โดยสารจริงสูงและต่ำที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_seat_utilization`
- Dimension: `dim_airport`
- Measure:
  - `boarded_count`
  - `seat_capacity`
  - `boarded_load_pct`

### ผลการวิเคราะห์

เส้นทางที่มี Boarded Load สูงที่สุดจากผล Query ที่ตรวจสอบแล้วคือ **SVX → SCW**

- Boarded Count: **3,779**
- Seat Capacity: **7,930**
- จำนวนเที่ยวบิน: **61**
- Boarded Load: **47.65%**

นอกจากนี้ยังพบเส้นทางบางส่วนที่มี Boarded Load ต่ำมากหรือเป็น 0%

### Business Insight

เส้นทางที่มี Boarded Load ต่ำอาจสะท้อน Capacity ที่สูงเมื่อเทียบกับจำนวนผู้โดยสารจริง ขณะที่เส้นทางที่มี Load สูงกว่าสามารถนำไปพิจารณาเรื่อง Capacity และความถี่เที่ยวบินได้

> ควรใช้ Weighted Load = `SUM(boarded_count) / SUM(seat_capacity)`

---

## Q6. เที่ยวบินใดมีช่องว่างระหว่างจำนวนตั๋วที่ขายกับจำนวนผู้โดยสารที่ขึ้นเครื่องจริงมากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_seat_utilization`
- มิติหลัก: Flight
- Measure:
  - `ticket_flight_count`
  - `boarded_count`
  - `booked_not_boarded_count`

### ผลการวิเคราะห์

เที่ยวบินที่มีช่องว่างสูงที่สุดคือ **Flight ID 260 — DME → OVB**

- Ticket Flight Count: **370**
- Boarded Count: **0**
- Booked-not-boarded Gap: **370**

### Business Insight

ผลลัพธ์นี้ช่วยระบุเที่ยวบินที่จำนวนตั๋วที่ขายมีความแตกต่างจากจำนวนผู้โดยสารที่ขึ้นเครื่องจริงอย่างมาก ซึ่งสามารถใช้เป็นจุดเริ่มต้นในการตรวจสอบพฤติกรรม Booked-but-not-boarded

> `booked_not_boarded_count` เป็นเพียง Proxy ไม่ควรสรุปว่าเป็น No-show ทุกกรณีโดยตรง

---

## Q7. ช่วงเวลาใดของวันมีจำนวนเที่ยวบินและปริมาณผู้โดยสารสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- มิติหลัก: `departure_daypart`
- Measure:
  - `flight_count`
  - `boarded_count`

### ผลการวิเคราะห์

| Daypart | จำนวนเที่ยวบิน | Boarded Count |
|---|---:|---:|
| Afternoon | 17,789 | 278,118 |
| Morning | 10,326 | 197,640 |
| Evening | 5,006 | 103,928 |

### Business Insight

ช่วง Afternoon มีทั้งจำนวนเที่ยวบินและจำนวนผู้โดยสารสูงที่สุด จึงเป็นช่วงเวลาที่มี Traffic สูงและอาจต้องใช้ทรัพยากรด้าน Operation มากกว่าช่วงเวลาอื่น

---

## Q8. วันธรรมดากับวันหยุดสุดสัปดาห์มีความต้องการเดินทางแตกต่างกันอย่างไร?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- มิติหลัก: Weekday / Weekend
- Measure:
  - `flight_count`
  - `boarded_count`
  - Average Boarded per Flight

### ผลการวิเคราะห์

| Day Type | Flights | Boarded | Avg Boarded / Flight |
|---|---:|---:|---:|
| Weekday | 23,555 | 411,231 | 17.46 |
| Weekend | 9,566 | 168,455 | 17.61 |

### Business Insight

วันธรรมดามีจำนวนเที่ยวบินและจำนวนผู้โดยสารรวมสูงกว่าวันหยุดสุดสัปดาห์ แต่ค่าเฉลี่ยผู้โดยสารต่อเที่ยวบินของทั้งสองกลุ่มใกล้เคียงกัน

---

## Q9. ผู้โดยสารมักจองตั๋วล่วงหน้ากี่วัน และแตกต่างกันอย่างไรในแต่ละ Fare Class?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_fare_class`
- Measure: `booking_lead_days`

### ผลการวิเคราะห์

| Fare Class | Avg Lead Days | Median | Min | Max | Ticket Flight |
|---|---:|---:|---:|---:|---:|
| Economy | 20.31 | 19.56 | -27.60 | 65.41 | 920,793 |
| Business | 20.25 | 19.47 | -23.37 | 57.08 | 107,642 |
| Comfort | 19.99 | 19.20 | -10.04 | 55.09 | 17,291 |

### Business Insight

ผู้โดยสารในทุก Fare Class มีพฤติกรรมการจองล่วงหน้าใกล้เคียงกัน โดยเฉลี่ยประมาณ 20 วัน

### Data Quality Note

พบค่า `booking_lead_days` ติดลบบางรายการ ซึ่งเป็นค่าที่ผิดปกติในเชิงธุรกิจ จึงควรตรวจสอบแหล่งข้อมูลหรือ Logic ของการคำนวณเพิ่มเติม

---

## Q10. Aircraft Manufacturer และรุ่นเครื่องบินใดถูกใช้งานกับเที่ยวบินมากที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- Dimension: `dim_aircraft`
- มิติหลัก:
  - Manufacturer
  - Aircraft Model
- Measure: `flight_count`

### ผลการวิเคราะห์

| Manufacturer | Aircraft Model | จำนวนเที่ยวบิน |
|---|---|---:|
| Cessna | Cessna 208 Caravan | 9,273 |
| Bombardier | CRJ-200 | 9,048 |
| Sukhoi | Superjet-100 | 8,504 |
| Airbus | A321-200 | 1,952 |
| Boeing | 737-300 | 1,274 |
| Airbus | A319-100 | 1,239 |
| Boeing | 767-300 | 1,221 |
| Boeing | 777-300 | 610 |

### Business Insight

Cessna 208 Caravan เป็น Aircraft Model ที่ถูกใช้งานกับเที่ยวบินมากที่สุด รองลงมาคือ Bombardier CRJ-200 และ Sukhoi Superjet-100

---

## Q11. เส้นทางใดมีความล่าช้าในการออกเดินทางและถึงปลายทางเฉลี่ยสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- Dimension: `dim_airport`
- มิติหลัก: Route
- Measure:
  - Average `departure_delay_minutes`
  - Average `arrival_delay_minutes`
  - `flight_count`

### ผลการวิเคราะห์

| Route | Avg Departure Delay | Avg Arrival Delay | Flights |
|---|---:|---:|---:|
| VKO → DYR | 108.75 | 107.25 | 4 |
| KLF → OVB | 89.60 | 91.80 | 5 |
| CNN → LED | 76.00 | 78.20 | 5 |

### Business Insight

VKO → DYR มีความล่าช้าเฉลี่ยสูงที่สุดจากผล Query ที่ตรวจสอบแล้ว แต่มีจำนวนเที่ยวบินเพียง 4 เที่ยวบิน จึงควรพิจารณา `total_flights` ร่วมด้วย

ผลลัพธ์นี้ใช้เพื่อระบุเส้นทางที่ควรตรวจสอบด้าน Schedule และ Operation โดยไม่ควรสรุปว่าสนามบินเป็นสาเหตุของความล่าช้าโดยตรง

---

# Multidimensional / Challenge Questions

## Q12. ในแต่ละภูมิภาคและช่วงเวลาของวัน ช่วงใดมีความล่าช้าในการออกเดินทางเฉลี่ยสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_flight_operations`
- Dimension: `dim_airport`
- มิติหลัก: Region × Daypart
- Measure: Average `departure_delay_minutes`

### ผลการวิเคราะห์

| Departure Region | Daypart | Avg Departure Delay | Flights |
|---|---|---:|---:|
| Far East | Afternoon | 14.99 | 502 |
| Siberia | Morning | 13.90 | 639 |
| Western Russia | Evening | 13.29 | 1,499 |
| Ural | Afternoon | 12.57 | 1,959 |

### Business Insight

แต่ละภูมิภาคมีช่วงเวลาที่มี Delay เฉลี่ยสูงแตกต่างกัน จึงสามารถใช้ข้อมูลนี้ในการวางแผน Operation แบบเจาะจงทั้งพื้นที่และช่วงเวลาได้

---

## Q13. ในแต่ละเส้นทาง Fare Class ใดสร้างรายได้สูง แต่มีจำนวนตั๋วขายไม่สูงตามไปด้วย?

### ข้อมูลที่ใช้
- Fact Table: `fact_ticket_sales`
- Dimension:
  - `dim_airport`
  - `dim_fare_class`
- มิติหลัก: Route × Fare Class
- Measure:
  - `total_revenue`
  - `ticket_count`
  - `revenue_per_ticket`

### Logic เวอร์ชันล่าสุด

ใช้เกณฑ์ดังนี้

- `total_revenue >= median(total_revenue)`
- `ticket_count <= median(ticket_count)`

และใช้ `revenue_per_ticket` ประกอบการตีความ

### Business Insight

การวิเคราะห์นี้ช่วยระบุกลุ่ม Route × Fare Class ที่สร้างมูลค่ารวมสูง แม้จำนวนตั๋วไม่ได้สูงตามไปด้วย ซึ่งสามารถนำไปใช้ประกอบการออกแบบ Pricing และ Product Mix ได้

---

## Q14. ในแต่ละภูมิภาค Aircraft Manufacturer/Model ใดมีอัตราการใช้ที่นั่งจริงสูงที่สุด?

### ข้อมูลที่ใช้
- Fact Table: `fact_seat_utilization`
- Dimension:
  - `dim_airport`
  - `dim_aircraft`
- มิติหลัก: Region × Aircraft Manufacturer/Model
- Measure: Weighted `boarded_load_pct`

### ผลการวิเคราะห์

| Region | Aircraft | Boarded Load |
|---|---|---:|
| Far East | Sukhoi Superjet-100 | 23.80% |
| Siberia | Airbus A321-200 | 31.49% |
| Ural | Airbus A319-100 | 33.50% |
| Western Russia | Boeing 777-300 | 35.38% |

### Business Insight

Aircraft Model ที่มี Boarded Load สูงที่สุดแตกต่างกันในแต่ละภูมิภาค แสดงให้เห็นว่าความเหมาะสมของ Fleet อาจแตกต่างตาม Demand ของแต่ละพื้นที่

---

## Q15. เส้นทางและช่วงเวลาใดมีความต้องการเดินทางสูง และมีอัตราการใช้ที่นั่งสูงอย่างต่อเนื่อง?

### ข้อมูลที่ใช้
- Fact Table: `fact_seat_utilization`
- Dimension:
  - `dim_date`
  - `dim_airport`
- มิติหลัก: Route × Daypart × Month
- Measure:
  - `ticket_flight_count`
  - `boarded_count`
  - `seat_capacity`
  - `boarded_load_pct`

### Logic เวอร์ชันล่าสุด

พิจารณาเป็นรายเดือนก่อน แล้วเลือก Route × Daypart ที่

- `boarded_count` สูงกว่าค่าเฉลี่ยของข้อมูลรายเดือน
- `boarded_load_pct` สูงกว่าค่าเฉลี่ยของข้อมูลรายเดือน
- เกิดเงื่อนไขดังกล่าวซ้ำอย่างน้อย 2 เดือน

จากนั้นสรุปด้วย

- `active_months`
- `ticket_flight_count`
- `boarded_count`
- `avg_boarded_load_pct`

### Business Insight

การวิเคราะห์นี้ช่วยระบุ Route × Daypart ที่มี Demand และการใช้ Capacity สูงเกิดซ้ำมากกว่าหนึ่งช่วงเวลา ซึ่งสามารถใช้ประกอบการพิจารณาเพิ่มความถี่เที่ยวบินหรือปรับขนาดเครื่องบินได้

---

# สรุป Business Insights

| Q | ผลลัพธ์สำคัญ |
|---|---|
| Q1 | DME → KHV สร้างรายได้สูงสุด 753,478,300 |
| Q2 | Economy มีสัดส่วนรายได้สูงสุด 70.76% |
| Q3 | สิงหาคม 2017 มีรายได้สูงสุดในช่วงข้อมูลที่วิเคราะห์ |
| Q4 | Western Russia → Western Russia มี Ticket Flight สูงสุด 512,461 |
| Q5 | SVX → SCW มี Boarded Load 47.65% |
| Q6 | Flight ID 260 DME → OVB มี Booked-not-boarded Gap 370 |
| Q7 | Afternoon มี Traffic สูงสุด |
| Q8 | Weekday มียอดรวมสูงกว่า Weekend แต่ Avg Boarded/Flight ใกล้เคียงกัน |
| Q9 | ทุก Fare Class จองล่วงหน้าเฉลี่ยประมาณ 20 วัน |
| Q10 | Cessna 208 Caravan ถูกใช้งานมากที่สุด 9,273 เที่ยวบิน |
| Q11 | VKO → DYR มี Avg Departure Delay สูงสุดจากผล Query แต่มีเพียง 4 เที่ยวบิน |
| Q12 | Far East × Afternoon มี Avg Departure Delay สูงสุด 14.99 นาที |
| Q13 | ใช้ Median Threshold + Revenue per Ticket |
| Q14 | Aircraft ที่มี Boarded Load สูงสุดแตกต่างกันตามภูมิภาค |
| Q15 | วิเคราะห์ Route × Daypart แบบรายเดือนและต้องเกิดซ้ำอย่างน้อย 2 เดือน |

---

# บทสรุป

Airline Data Warehouse เวอร์ชันล่าสุดสามารถรองรับการวิเคราะห์ได้ทั้งด้านรายได้ ความต้องการเดินทาง รูปแบบการจอง การใช้ Capacity การดำเนินงานของเที่ยวบิน Fleet Usage และความล่าช้า

Fact Table หลักประกอบด้วย

- `fact_ticket_sales` สำหรับ Revenue / Ticket Demand / Booking Behavior
- `fact_flight_operations` สำหรับ Flight Operations / Delay / Daypart
- `fact_seat_utilization` สำหรับ Capacity / Boarded Load / Booked-not-boarded

Challenge Questions Q12–Q15 แสดงให้เห็นการวิเคราะห์แบบหลายมิติ เช่น Region × Daypart, Route × Fare Class, Region × Aircraft และ Route × Time ซึ่งช่วยสนับสนุนการตัดสินใจเชิงธุรกิจได้ละเอียดมากขึ้น