# 03_Business_Questions

## 1. วัตถุประสงค์

Business Questions ถูกกำหนดขึ้นเพื่อเป็นแนวทางในการออกแบบ Data Warehouse และใช้กำหนด Dimension, Fact และ Measure ที่จำเป็นสำหรับการวิเคราะห์ข้อมูลของสายการบิน

โครงการนี้กำหนด Business Questions จำนวน 15 ข้อ ครอบคลุมการวิเคราะห์ด้านยอดขายตั๋ว สนามบินและเส้นทาง เครื่องบิน ที่นั่ง สถานะเที่ยวบิน และความล่าช้าของเที่ยวบิน

---

## 2. Business Questions

| Q | Business Question | Dimension ที่ใช้ | Measure |
|---|---|---|---|
| Q1 | ยอดขายตั๋วรวมเป็นเท่าใด? | - | amount |
| Q2 | จำนวน Ticket Flight ทั้งหมดเท่าใด? | - | ticket_flight_count |
| Q3 | Fare Class ใดสร้างยอดขายสูงที่สุด? | dim_fare_class | amount |
| Q4 | Fare Class ใดมีจำนวน Ticket Flight มากที่สุด? | dim_fare_class | ticket_flight_count |
| Q5 | ยอดขายตั๋วเปลี่ยนแปลงอย่างไรตามช่วงเวลา? | dim_date | amount |
| Q6 | สนามบินต้นทางใดมีจำนวน Ticket Flight มากที่สุด? | dim_airport | ticket_flight_count |
| Q7 | สนามบินปลายทางใดมีจำนวน Ticket Flight มากที่สุด? | dim_airport | ticket_flight_count |
| Q8 | เส้นทางต้นทาง–ปลายทางใดมีจำนวน Ticket Flight มากที่สุด? | dim_airport | ticket_flight_count |
| Q9 | เส้นทางใดสร้างยอดขายตั๋วสูงที่สุด? | dim_airport | amount |
| Q10 | Aircraft Model ใดถูกใช้กับเที่ยวบินมากที่สุด? | dim_aircraft | flight_count |
| Q11 | Aircraft Model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด? | dim_aircraft | seat_count |
| Q12 | Aircraft Model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร? | dim_aircraft, dim_fare_class | seat_count |
| Q13 | Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด? | dim_flight_status | flight_count |
| Q14 | สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด? | dim_airport | departure_delay_minutes |
| Q15 | ในแต่ละช่วงเวลา เส้นทางต้นทาง–ปลายทางและ Fare Class ใดสร้างยอดขายตั๋วสูงที่สุด? | dim_date, dim_airport, dim_fare_class | amount |

---

## 3. การจัดกลุ่ม Business Questions

### 3.1 Sales Analysis

ประกอบด้วย Q1–Q5

ใช้สำหรับวิเคราะห์ยอดขาย จำนวน Ticket Flight ชั้นโดยสาร และแนวโน้มยอดขายตามช่วงเวลา

### 3.2 Airport and Route Analysis

ประกอบด้วย Q6–Q9

ใช้สำหรับวิเคราะห์สนามบินต้นทาง สนามบินปลายทาง เส้นทางที่มีผู้โดยสารมาก และเส้นทางที่สร้างยอดขายสูง

### 3.3 Aircraft and Seat Analysis

ประกอบด้วย Q10–Q12

ใช้สำหรับวิเคราะห์การใช้งานเครื่องบิน จำนวนที่นั่ง และสัดส่วนที่นั่งแต่ละ Fare Class

### 3.4 Flight Operations Analysis

ประกอบด้วย Q13–Q14

ใช้สำหรับวิเคราะห์สถานะเที่ยวบินและความล่าช้าของเที่ยวบิน

### 3.5 Multidimensional Analysis

ประกอบด้วย Q15

ใช้สำหรับวิเคราะห์ข้อมูลหลายมิติร่วมกัน ได้แก่ เวลา เส้นทาง Fare Class และยอดขาย

---

## 4. สรุป

Business Questions ทั้ง 15 ข้อถูกใช้เป็นพื้นฐานในการออกแบบ Airline Data Warehouse โดยคำถามแต่ละข้อเชื่อมโยงกับ Dimension และ Measure ที่เหมาะสม

Business Questions เหล่านี้ถูกนำไปใช้ในการออกแบบ Multidimensional Model และนำไปวิเคราะห์ผลจริงในขั้นตอน Business Insights และ Dashboard
