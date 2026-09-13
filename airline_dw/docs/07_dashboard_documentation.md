# Dashboard Documentation

## 1. ภาพรวม Dashboard

Dashboard นี้ถูกพัฒนาด้วย Streamlit เพื่อใช้สำหรับนำเสนอและวิเคราะห์ข้อมูลจาก Airline Data Warehouse โดยเชื่อมต่อกับฐานข้อมูล DuckDB โดยตรง

Dashboard สามารถใช้วิเคราะห์ข้อมูลด้านยอดขายตั๋ว เส้นทางบิน สนามบิน เครื่องบิน จำนวนที่นั่ง สถานะเที่ยวบิน และความล่าช้าของเที่ยวบิน

เทคโนโลยีที่ใช้ประกอบด้วย

- Streamlit สำหรับพัฒนา Dashboard
- Plotly สำหรับสร้างกราฟแบบ Interactive
- DuckDB สำหรับจัดเก็บและ Query ข้อมูล Data Warehouse
- dbt สำหรับสร้าง Staging, Dimension และ Fact Models
- pandas สำหรับจัดการข้อมูลที่นำมาแสดงผล

---

## 2. การเชื่อมต่อกับ Data Warehouse

Dashboard เชื่อมต่อกับฐานข้อมูล DuckDB โดยตรงผ่านไฟล์

`dev.duckdb`

โดยใช้ Python package `duckdb`

ตัว Dashboard ไม่ได้อ่านข้อมูลจาก CSV สำหรับการแสดงผล แต่ Query ข้อมูลจาก Fact และ Dimension Tables ที่สร้างขึ้นใน Data Warehouse

Fact Tables ที่ใช้ ได้แก่

- `fact_ticket_sales`
- `fact_flight_operations`
- `fact_seat_inventory`

Dimension Tables ที่ใช้ ได้แก่

- `dim_date`
- `dim_airport`
- `dim_aircraft`
- `dim_fare_class`
- `dim_flight_status`

---

## 3. Business Questions ที่ Dashboard รองรับ

Dashboard ถูกออกแบบให้รองรับ Business Questions ทั้งหมด 15 ข้อ

### Q1 ยอดขายตั๋วรวมเป็นเท่าใด?

แสดงผลในรูปแบบ KPI โดยคำนวณจาก

`SUM(amount)`

จาก `fact_ticket_sales`

### Q2 จำนวน Ticket Flight ทั้งหมดเท่าใด?

แสดงผลในรูปแบบ KPI โดยใช้

`SUM(ticket_flight_count)`

จาก `fact_ticket_sales`

### Q3 Fare Class ใดสร้างยอดขายสูงที่สุด?

เปรียบเทียบยอดขายระหว่าง Fare Class เช่น

- Economy
- Comfort
- Business

โดยใช้ข้อมูลจาก `fact_ticket_sales` และ `dim_fare_class`

### Q4 Fare Class ใดมีจำนวน Ticket Flight มากที่สุด?

เปรียบเทียบจำนวน Ticket Flight ในแต่ละ Fare Class

### Q5 ยอดขายตั๋วเปลี่ยนแปลงอย่างไรตามช่วงเวลา?

แสดงแนวโน้มยอดขายตามเดือน โดยเชื่อม

`fact_ticket_sales`

กับ

`dim_date`

### Q6 สนามบินต้นทางใดมีจำนวน Ticket Flight มากที่สุด?

วิเคราะห์จำนวน Ticket Flight จำแนกตามสนามบินต้นทาง

### Q7 สนามบินปลายทางใดมีจำนวน Ticket Flight มากที่สุด?

วิเคราะห์จำนวน Ticket Flight จำแนกตามสนามบินปลายทาง

### Q8 เส้นทางต้นทาง–ปลายทางใดมีจำนวน Ticket Flight มากที่สุด?

วิเคราะห์ Route โดยจับคู่

`Departure Airport → Arrival Airport`

และเรียงตามจำนวน Ticket Flight

### Q9 เส้นทางใดสร้างยอดขายตั๋วสูงที่สุด?

วิเคราะห์ยอดขายของแต่ละเส้นทางจาก `fact_ticket_sales`

### Q10 Aircraft Model ใดถูกใช้กับเที่ยวบินมากที่สุด?

ใช้ `fact_flight_operations` ร่วมกับ `dim_aircraft`

เพื่อเปรียบเทียบจำนวนเที่ยวบินของเครื่องบินแต่ละรุ่น

### Q11 Aircraft Model แต่ละรุ่นมีจำนวนที่นั่งเท่าใด?

ใช้ `fact_seat_inventory` เพื่อวิเคราะห์จำนวนที่นั่งของเครื่องบินแต่ละรุ่น

### Q12 Aircraft Model แต่ละรุ่นมีสัดส่วนที่นั่งแต่ละ Fare Class อย่างไร?

วิเคราะห์โครงสร้างที่นั่งของเครื่องบินโดยแบ่งตาม Fare Class

### Q13 Flight Status แต่ละประเภทมีจำนวนเที่ยวบินเท่าใด?

ใช้ `fact_flight_operations` และ `dim_flight_status`

เพื่อแสดงจำนวนเที่ยวบินในแต่ละสถานะ

### Q14 สนามบินต้นทางใดมีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด?

คำนวณค่าเฉลี่ย

`departure_delay_minutes`

ของแต่ละสนามบินต้นทาง โดยพิจารณาเฉพาะเที่ยวบินที่มีความล่าช้ามากกว่า 0 นาที

### Q15 ในแต่ละช่วงเวลา เส้นทางต้นทาง–ปลายทางและ Fare Class ใดสร้างยอดขายตั๋วสูงที่สุด?

เป็นการวิเคราะห์แบบหลายมิติ โดยใช้

- Date
- Departure Airport
- Arrival Airport
- Fare Class
- Ticket Sales

และจัดอันดับยอดขายในแต่ละช่วงเวลา

---

## 4. ตัวกรองข้อมูล

Dashboard มี Interactive Filters เพื่อให้ผู้ใช้สามารถวิเคราะห์ข้อมูลตามเงื่อนไขที่ต้องการ

ตัวกรองประกอบด้วย

- ช่วงวันที่
- สนามบินต้นทาง
- สนามบินปลายทาง
- ชั้นโดยสาร
- รุ่นเครื่องบิน

ตัวกรองถูกออกแบบเป็น Cascading Filters

เมื่อผู้ใช้เลือกสนามบินต้นทาง ระบบจะแสดงเฉพาะสนามบินปลายทางที่มีข้อมูลจริง

เมื่อเลือกเส้นทางแล้ว ระบบจะแสดงเฉพาะ Fare Class และ Aircraft Model ที่สัมพันธ์กับข้อมูลที่เลือก

วิธีนี้ช่วยลดการเลือก Combination ที่ไม่มีข้อมูลอยู่จริงใน Data Warehouse

---

## 5. Date Range

ผู้ใช้สามารถกำหนดช่วงวันที่ที่ต้องการวิเคราะห์ได้จาก Date Range Filter

ข้อมูลใน KPI และกราฟที่เกี่ยวข้องกับเวลา จะปรับเปลี่ยนตามช่วงวันที่ที่เลือก

Date Range ใช้ `dim_date` เป็น Dimension หลักสำหรับการวิเคราะห์ตามเวลา

---

## 6. Drill-down

Dashboard มีฟังก์ชัน Drill-down สำหรับการวิเคราะห์เส้นทาง

ผู้ใช้สามารถเลือก Route เช่น

`AAA → BBB`

แล้วดูรายละเอียดของ Route นั้นแยกตาม Fare Class

ข้อมูลที่แสดงประกอบด้วย

- Fare Class
- Total Sales
- Ticket Flights

ทำให้สามารถวิเคราะห์จากภาพรวมของ Route ลงไปสู่รายละเอียดภายใน Route ได้

---

## 7. รูปแบบการแสดงผล

Dashboard ใช้ Visualization หลายประเภท เช่น

- KPI Cards
- Donut Chart
- Horizontal Bar Chart
- Stacked Bar Chart
- Area / Trend Chart
- Data Table

การเลือกใช้กราฟแตกต่างกันตามลักษณะของ Business Question เพื่อให้ข้อมูลสามารถอ่านและเปรียบเทียบได้ง่าย

---

## 8. การดาวน์โหลดข้อมูล

Dashboard รองรับการดาวน์โหลดข้อมูลบางส่วนในรูปแบบ CSV

เช่น

- Route Drill-down Result
- Multidimensional Analysis Result

เพื่อให้ผู้ใช้สามารถนำผลการวิเคราะห์ไปใช้งานต่อได้

---

## 9. วิธีรัน Dashboard

ติดตั้ง dependencies จาก root ของ repository

```bash
pip install -r requirements.txt