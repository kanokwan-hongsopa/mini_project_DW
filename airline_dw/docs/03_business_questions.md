# 03 Business Questions

## 1. วัตถุประสงค์

Business Questions ถูกกำหนดขึ้นเพื่อเป็นแนวทางในการออกแบบ Data Warehouse และใช้กำหนด Dimension, Fact และ Measure ที่จำเป็นสำหรับการวิเคราะห์ข้อมูลของสายการบิน

โครงการนี้กำหนด Business Questions จำนวน 15 ข้อ โดยครอบคลุมการวิเคราะห์ด้านรายได้และการขายตั๋ว ความต้องการเดินทาง เส้นทางและภูมิภาค การใช้ที่นั่ง ช่วงเวลาการเดินทาง พฤติกรรมการจอง การใช้งานเครื่องบิน และความล่าช้าของเที่ยวบิน

นอกจากนี้ Q12–Q15 ถูกกำหนดเป็น Multidimensional / Challenge Questions ซึ่งวิเคราะห์หลายมิติร่วมกัน เพื่อให้สามารถนำผลการวิเคราะห์ไปใช้สนับสนุนการตัดสินใจทางธุรกิจได้ละเอียดมากขึ้น

---

## 2. Business Questions

| Q | Business Question | ข้อมูล/มิติหลักที่ใช้ | Measure / ข้อมูลวัดผล | ประโยชน์ทางธุรกิจ |
|---|---|---|---|---|
| Q1 | เส้นทางใดสร้างรายได้จากการขายตั๋วสูงที่สุด? | Departure Airport + Arrival Airport | amount | ระบุเส้นทางรายได้หลัก เพื่อรักษา Capacity และให้ความสำคัญกับเส้นทางที่สร้างรายได้ |
| Q2 | Fare Class ใดสร้างรายได้สูงที่สุด และมีสัดส่วนรายได้เท่าใด? | Fare Class | amount, revenue share | ใช้วางกลยุทธ์ราคา โปรโมชั่น และสัดส่วนที่นั่งแต่ละ Class |
| Q3 | รายได้จากการขายตั๋วมีแนวโน้มเปลี่ยนแปลงอย่างไรในแต่ละเดือน? | Date | amount | มองเห็นช่วงรายได้สูง–ต่ำ เพื่อวางแผนการขายและโปรโมชั่นตามช่วงเวลา |
| Q4 | ภูมิภาคต้นทาง–ปลายทางคู่ใดมีความต้องการเดินทางสูงที่สุด? | Departure Region + Arrival Region | ticket_count | ช่วยวางแผน Network และจัดสรรเที่ยวบินระหว่างภูมิภาคที่มี Demand สูง |
| Q5 | เส้นทางใดมีอัตราการใช้ที่นั่งของผู้โดยสารจริง (boarded_load_pct) สูงและต่ำที่สุด? | Route | boarded_load_pct, seat_capacity, boarded_count | เส้นทางที่มีอัตราต่ำอาจพิจารณาปรับ Capacity หรือตาราง ส่วนเส้นทางที่มีอัตราสูงอาจพิจารณาเพิ่ม Capacity |
| Q6 | เที่ยวบินใดมีช่องว่างระหว่างจำนวนตั๋วที่ขายกับจำนวนผู้โดยสารที่ขึ้นเครื่องจริงมากที่สุด? | Flight | ticket_flight_count, boarded_count | ใช้วิเคราะห์ Booked-but-not-boarded / No-show Proxy และผลต่อการใช้ Capacity |
| Q7 | ช่วงเวลาใดของวันมีจำนวนเที่ยวบินและปริมาณผู้โดยสารสูงที่สุด? | Departure Daypart | flight_count, boarded_count | ช่วยวางแผนทรัพยากรในช่วงเวลาที่มี Traffic สูง |
| Q8 | วันธรรมดากับวันหยุดสุดสัปดาห์มีความต้องการเดินทางแตกต่างกันอย่างไร? | Weekday / Weekend | ticket_count หรือ boarded_count | ใช้จัดตารางเที่ยวบินและ Capacity ให้เหมาะกับรูปแบบ Demand |
| Q9 | ผู้โดยสารมักจองตั๋วล่วงหน้ากี่วัน และรูปแบบการจองล่วงหน้าแตกต่างกันอย่างไรในแต่ละ Fare Class? | Booking Lead Days + Fare Class | booking_lead_days | ใช้ออกแบบ Advance-purchase Pricing และโปรโมชั่นสำหรับลูกค้าแต่ละกลุ่ม |
| Q10 | Aircraft Manufacturer และรุ่นเครื่องบินใดถูกใช้งานกับเที่ยวบินมากที่สุด? | Manufacturer + Aircraft Model | flight_count | เห็นรูปแบบการใช้งาน Fleet เพื่อประกอบการวางแผนเครื่องบินและทรัพยากรที่เกี่ยวข้อง |
| Q11 | เส้นทางใดมีความล่าช้าในการออกเดินทางและถึงปลายทางเฉลี่ยสูงที่สุด? | Route | avg departure_delay_minutes, avg arrival_delay_minutes | ระบุเส้นทางที่ควรตรวจสอบด้าน Schedule และ Operation โดยไม่สรุปว่าสนามบินเป็นสาเหตุของความล่าช้า |

---

## 3. Multidimensional / Challenge Questions

Q12–Q15 เป็นคำถามที่ใช้หลายมิติร่วมกัน เพื่อวิเคราะห์ความสัมพันธ์ของข้อมูลในระดับที่ละเอียดกว่าคำถามพื้นฐาน

| Q | Challenge Business Question | มิติที่ใช้ | Measure / ข้อมูลวัดผล | ประโยชน์ทางธุรกิจ |
|---|---|---|---|---|
| Q12 ⭐ | ในแต่ละภูมิภาคและช่วงเวลาของวัน ช่วงใดมีความล่าช้าในการออกเดินทางเฉลี่ยสูงที่สุด? | Region × Daypart | avg departure_delay_minutes | ระบุทั้งพื้นที่และช่วงเวลาที่มีความล่าช้าสูง เพื่อนำไปปรับ Schedule และ Operational Planning ได้เฉพาะจุด |
| Q13 ⭐ | ในแต่ละเส้นทาง Fare Class ใดสร้างรายได้สูง แต่มีจำนวนตั๋วขายไม่สูงตามไปด้วย? | Route × Fare Class | revenue, ticket_count | ช่วยแยกเส้นทางและ Class ที่สร้างมูลค่าต่อตั๋วสูง เพื่อนำไปวาง Pricing และ Product Mix |
| Q14 ⭐ | ในแต่ละภูมิภาค Aircraft Manufacturer/Model ใดมีอัตราการใช้ที่นั่งจริงสูงที่สุด? | Region × Aircraft Manufacturer/Model | boarded_load_pct | ใช้ประกอบการตัดสินใจจัดเครื่องบินที่มี Capacity เหมาะกับ Demand ของแต่ละพื้นที่ |
| Q15 ⭐ | เส้นทางและช่วงเวลาใดมีความต้องการเดินทางสูง แต่มีอัตราการใช้ที่นั่งสูงจนใกล้เต็มอย่างต่อเนื่อง? | Route × Time | ticket_count, boarded_count, boarded_load_pct | หาเส้นทาง–ช่วงเวลาที่อาจมี Demand สูงเมื่อเทียบกับ Capacity เพื่อประกอบการพิจารณาเพิ่มเที่ยวบินหรือใช้เครื่องที่มีความจุมากขึ้น |

---

## 4. การจัดกลุ่ม Business Questions

### 4.1 Revenue and Sales Analysis

ประกอบด้วย Q1–Q3

ใช้วิเคราะห์รายได้จากการขายตั๋ว เส้นทางที่สร้างรายได้ Fare Class และแนวโน้มรายได้ตามช่วงเวลา

### 4.2 Demand and Capacity Analysis

ประกอบด้วย Q4–Q8

ใช้วิเคราะห์ความต้องการเดินทางระหว่างภูมิภาค การใช้ที่นั่ง ความแตกต่างระหว่างจำนวนตั๋วกับผู้โดยสารที่ขึ้นเครื่องจริง ช่วงเวลาที่มี Traffic สูง และความแตกต่างระหว่างวันธรรมดากับวันหยุดสุดสัปดาห์

### 4.3 Booking and Fleet Analysis

ประกอบด้วย Q9–Q10

ใช้วิเคราะห์พฤติกรรมการจองล่วงหน้าของผู้โดยสาร และรูปแบบการใช้งาน Aircraft Manufacturer และ Aircraft Model

### 4.4 Flight Operations Analysis

ประกอบด้วย Q11

ใช้วิเคราะห์ความล่าช้าในการออกเดินทางและเดินทางถึงของแต่ละเส้นทาง เพื่อระบุเส้นทางที่ควรนำไปตรวจสอบด้าน Schedule และ Operation เพิ่มเติม

### 4.5 Multidimensional / Challenge Analysis

ประกอบด้วย Q12–Q15

ใช้วิเคราะห์หลายมิติร่วมกัน ได้แก่ Region, Daypart, Route, Fare Class, Aircraft Manufacturer/Model, Time, Revenue, Demand, Delay และ Load Percentage เพื่อให้สามารถวิเคราะห์ข้อมูลเชิงลึกและสนับสนุนการตัดสินใจได้ละเอียดมากขึ้น

---

## 5. ความเชื่อมโยงกับ Enriched Dataset

Business Questions ชุดใหม่นี้ถูกออกแบบให้ใช้ประโยชน์จากคอลัมน์ที่เพิ่มเข้ามาใน Enriched Dataset เช่น:

- `departure_region` และ `arrival_region`
- `aircraft_model` และ `manufacturer`
- `booking_lead_days`
- `departure_daypart`
- `departure_is_weekend`
- `departure_delay_minutes` และ `arrival_delay_minutes`
- `seat_capacity`
- `ticket_flight_count`
- `boarded_count`
- `ticketed_load_pct`
- `boarded_load_pct`

คอลัมน์เหล่านี้ช่วยให้ Data Warehouse สามารถตอบคำถามเกี่ยวกับ Revenue, Demand, Capacity, Booking Behavior, Fleet Usage และ Flight Operations รวมถึงรองรับ Multidimensional Analysis ได้มากขึ้น

---

## 6. สรุป

Business Questions ทั้ง 15 ข้อถูกใช้เป็นพื้นฐานในการออกแบบ Airline Data Warehouse และกำหนดข้อมูลที่จำเป็นสำหรับ Dimension, Fact และ Measure

Q1–Q11 เป็นคำถามสำหรับการวิเคราะห์ด้านรายได้ ความต้องการเดินทาง Capacity พฤติกรรมการจอง Fleet และการดำเนินงานของเที่ยวบิน ส่วน Q12–Q15 เป็น Multidimensional / Challenge Questions ที่นำหลายมิติมาวิเคราะห์ร่วมกัน

Business Questions เหล่านี้จะถูกนำไปใช้ในการออกแบบ Multidimensional Model การสร้าง Fact และ Dimension Tables การวิเคราะห์ Business Insights และการพัฒนา Dashboard ในขั้นตอนถัดไป