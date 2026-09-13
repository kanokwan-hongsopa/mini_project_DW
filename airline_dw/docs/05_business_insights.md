# 05 Business Insights

## Overview

This document presents business insights derived from the Airline Data Warehouse.  
The analysis primarily uses `fact_ticket_sales` together with related dimension tables, including `dim_date`, `dim_airport`, and `dim_fare_class`.

The analysis covers Business Questions 1–8, focusing on ticket sales, ticket flight volume, fare class performance, sales trends, airport activity, and popular routes.

---

## 1. What is the total ticket sales revenue?

### Business Question
ยอดขายตั๋วรวมเป็นเท่าใด?

### Data Used
- Fact Table: `fact_ticket_sales`
- Measure: `amount`

### Result
**Total Ticket Sales = 20,766,980,900**

### Business Insight
The total ticket sales revenue in the dataset is **20,766,980,900**.  
This value represents the overall revenue generated from all ticket-flight transactions recorded in the Data Warehouse.

---

## 2. How many Ticket Flights are there in total?

### Business Question
จำนวน Ticket Flight ทั้งหมดเท่าใด?

### Data Used
- Fact Table: `fact_ticket_sales`
- Measure: `ticket_flight_count`

### Result
**Total Ticket Flights = 1,045,726**

### Business Insight
There are **1,045,726 Ticket Flights** in the dataset.

The grain of `fact_ticket_sales` is one Ticket × Flight segment per row. Therefore, the `ticket_flight_count` measure can be aggregated to determine the total number of ticket-flight transactions.

---

## 3. Which Fare Class generates the highest ticket sales?

### Business Question
Fare Class ใดสร้างยอดขายสูงที่สุด?

### Data Used
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_fare_class`
- Measure: `amount`

### Result

| Fare Class | Total Sales |
|---|---:|
| Economy | 14,695,684,400 |
| Business | 5,505,179,600 |
| Comfort | 566,116,900 |

### Business Insight
**Economy Class generates the highest ticket sales**, with total sales of **14,695,684,400**.

Although Economy tickets generally represent a lower service class than Business, their substantially higher transaction volume contributes to the largest overall sales value.

---

## 4. Which Fare Class has the highest number of Ticket Flights?

### Business Question
Fare Class ใดมีจำนวนตั๋วมากที่สุด?

### Data Used
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_fare_class`
- Measure: `ticket_flight_count`

### Result

| Fare Class | Ticket Flights |
|---|---:|
| Economy | 920,793 |
| Business | 107,642 |
| Comfort | 17,291 |

### Business Insight
**Economy Class has the highest number of Ticket Flights**, with **920,793 transactions**.

Economy therefore represents the dominant Fare Class in terms of passenger ticket-flight volume within this dataset.

---

## 5. How do ticket sales change over time?

### Business Question
ยอดขายตั๋วเปลี่ยนแปลงอย่างไรตามช่วงเวลา?

### Data Used
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_date`
- Measure: `amount`

### Result

| Year | Month | Total Sales |
|---|---|---:|
| 2017 | July | 4,983,243,300 |
| 2017 | August | 13,509,694,600 |
| 2017 | September | 2,274,043,000 |

### Business Insight
Ticket sales reached their highest observed level in **August 2017**, with total sales of **13,509,694,600**.

July recorded **4,983,243,300**, while September recorded **2,274,043,000**.

The results show substantial variation in ticket sales across the observed months. However, the results alone do not establish the cause of these differences, and the dataset may not represent complete calendar months for every period.

---

## 6. Which departure airport has the highest number of Ticket Flights?

### Business Question
สนามบินต้นทางใดมีจำนวน Ticket Flight มากที่สุด?

### Data Used
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- Measure: `ticket_flight_count`
- Dimension Role: Departure Airport

### Result
**SVO — Sheremetyevo International Airport, Moscow**

**Total Ticket Flights = 155,073**

### Business Insight
**SVO (Sheremetyevo International Airport)** has the highest number of departing Ticket Flights, with **155,073 transactions**.

This indicates that SVO is the most active departure airport by ticket-flight volume within the analyzed dataset.

---

## 7. Which arrival airport has the highest number of Ticket Flights?

### Business Question
สนามบินปลายทางใดมีจำนวน Ticket Flight มากที่สุด?

### Data Used
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- Measure: `ticket_flight_count`
- Dimension Role: Arrival Airport

### Result
**SVO — Sheremetyevo International Airport, Moscow**

**Total Ticket Flights = 150,086**

### Business Insight
**SVO (Sheremetyevo International Airport)** also has the highest number of arriving Ticket Flights, with **150,086 transactions**.

The results show that SVO has high activity in both departure and arrival roles within the dataset.

---

## 8. Which departure-arrival route has the highest number of Ticket Flights?

### Business Question
เส้นทางต้นทาง–ปลายทางใดมีจำนวน Ticket Flight มากที่สุด?

### Data Used
- Fact Table: `fact_ticket_sales`
- Dimension: `dim_airport`
- Measure: `ticket_flight_count`
- Dimension Roles:
  - Departure Airport
  - Arrival Airport

### Result

**SVO → LED**

- Departure: Moscow
- Arrival: St. Petersburg
- Total Ticket Flights: **16,461**

### Business Insight
The route with the highest number of Ticket Flights is **SVO → LED (Moscow → St. Petersburg)**, with **16,461 transactions**.

This makes SVO–LED the highest-volume directional route in the analyzed ticket-flight data.

---

## Summary of Key Business Insights

| Business Question | Key Result |
|---|---|
| Q1 Total Ticket Sales | 20,766,980,900 |
| Q2 Total Ticket Flights | 1,045,726 |
| Q3 Highest Sales Fare Class | Economy — 14,695,684,400 |
| Q4 Highest Volume Fare Class | Economy — 920,793 |
| Q5 Highest Sales Period | August 2017 — 13,509,694,600 |
| Q6 Top Departure Airport | SVO — 155,073 |
| Q7 Top Arrival Airport | SVO — 150,086 |
| Q8 Top Route | SVO → LED — 16,461 |

## Conclusion

The analysis shows that **Economy Class is the dominant Fare Class** in both total sales and Ticket Flight volume. Ticket sales reached their highest observed monthly value in **August 2017**.

**SVO (Sheremetyevo International Airport)** is the leading airport for both departure and arrival Ticket Flight volume, while **SVO → LED (Moscow → St. Petersburg)** is the highest-volume directional route in the analyzed dataset.

These insights demonstrate how the Airline Data Warehouse can support multidimensional analysis across sales, Fare Class, time, airports, and routes.