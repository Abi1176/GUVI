# Zomato Food Delivery Data Insights
1. Project Overview
As a data scientist at Zomato, the goal of this project is to enhance operational efficiency and improve customer satisfaction by analyzing food delivery data. The interactive Streamlit tool enables seamless data entry and management of orders, customers, restaurants, and deliveries. The system supports robust database operations like adding columns or creating new tables dynamically while maintaining compatibility with existing code.
2. Source Code
This project consists of multiple Python scripts for dataset generation, database management, and Streamlit app development. The key components are:
a. Dataset Generation (datasetGenerator.py)
Generates synthetic food delivery data.
Exports data in CSV format for initial database seeding.
b. Database Management (DBConnection.py)
Establishes a connection to an MySQL Database.
Provides functions to create, update, and query tables dynamically.
Ensures compatibility with existing schema.
c. Streamlit App (ZomatoStreamlit.py)
Interactive interface for data entry and real-time analysis.
Allows users to insert, update, and view records.
Supports on-the-fly schema modifications.
3. Streamlit App
The Streamlit app is the front-end of this tool, designed to provide a user-friendly interface for managing and analyzing food delivery data.
Key Features:
Data Entry: Users can add new records for orders, customers, restaurants, and deliveries.
Dynamic Table Management: Ability to create new tables or add columns dynamically.
Visual Analytics: Data visualization through interactive charts.
SQL Query Execution: Run custom SQL queries for deeper insights.
 
 
 
4. Database Schema
The SQL database includes the following tables:
a. tbl_customers
Column Name
Data Type
Description
customer_id
INT
Auto-increment primary key for each customer.
name
VARCHAR(255)
Name of the customer.
email
VARCHAR(255)
Email address of the customer, must be unique.
phone
VARCHAR(20)
Phone number of the customer, must be unique.
location
TEXT
Customer's location details.
signup_date
DATE
The date when the customer signed up.
is_premium
BOOLEAN
Whether the customer is a premium member (true/false).
preferred_cuisine
VARCHAR(100)
Preferred cuisine of the customer (e.g., Italian, Chinese).
total_orders
INT
Total number of orders placed by the customer.
average_rating
DECIMAL(3,2)
Average rating given by the customer, ranging from 0.00 to 5.00.

 
b. tbl_delivery_persons
Column Name
Data Type
Description
delivery_person_id
INT
Auto-increment primary key for each delivery person.
name
VARCHAR(255)
Name of the delivery person.
contact_number
VARCHAR(20)
Contact number of the delivery person, must be unique.
vehicle_type
ENUM('Bike','Scooter','Motorcycle','Electric Bike','Electric Scooter','Moped')
Type of vehicle used by the delivery person.
total_deliveries
INT
Total number of deliveries made by the delivery person, must be non-negative.
average_rating
DECIMAL(2,1)
Average rating of the delivery person, ranging from 1.0 to 5.0.
location
TEXT
Delivery person's location details.

 
c. tbl_order_details
Column Name
Data Type
Description
order_id
INT
Auto-increment primary key for each order.
customer_id
INT
Foreign key referencing the customer_id from the tbl_customers table.
restaurant_id
INT
Foreign key referencing the restaurant_id from the tbl_restaurant table.
order_date
DATETIME
The date and time when the order was placed.
delivery_time
DATETIME
The date and time when the delivery is completed.
status
ENUM('Pending', 'Delivered', 'Cancelled')
Status of the order (e.g., Pending, Delivered, Cancelled).
total_amount
DECIMAL(10,2)
Total amount for the order.
payment_mode
ENUM('Credit Card', 'Cash', 'UPI')
Mode of payment (e.g., Credit Card, Cash, UPI).
discount_applied
DECIMAL(10,2)
The discount applied to the order, if any.
feedback_rating
DECIMAL(2,1)
Feedback rating for the order, ranging from 1.0 to 5.0.

 
d. tbl_deliveries
Column Name
Data Type
Description
delivery_id
INT
Auto-increment primary key for each delivery record.
order_id
INT
Foreign key referencing the order_id from the tbl_order_details table.
delivery_person_id
INT
Foreign key referencing the delivery_person_id from the tbl_delivery_persons table.
delivery_status
ENUM('Pending', 'Delivered', 'Cancelled')
Status of the delivery (e.g., On the way, Delivered, or Failed).
distance
DECIMAL(5,2)
Distance traveled for the delivery, must be a positive value.
delivery_time
INT
Delivery time in minutes, must be a positive value.
estimated_time
INT
Estimated delivery time in minutes, must be a positive value.
delivery_fee
DECIMAL(10,2)
Delivery fee charged for the delivery, must be a positive value.
vehicle_type
ENUM('Bike','Scooter','Motorcycle','Electric Bike','Electric Scooter','Moped')
Type of vehicle used for delivery

 
e. tbl_restaurant
Column Name
Data Type
Description
restaurant_id
INT
Auto-increment primary key for each restaurant.
name
VARCHAR(255)
Name of the restaurant.
cuisine_type
VARCHAR(100)
Type of cuisine served at the restaurant (e.g., Italian, Chinese).
location
TEXT
Location details of the restaurant.
owner_name
VARCHAR(255)
Name of the restaurant owner.
average_delivery_time
INT
Average time taken for delivery from the restaurant, must be a non-negative value.
contact_number
VARCHAR(20)
Contact number for the restaurant, must be unique.
rating
DECIMAL(2,1)
Rating of the restaurant, ranging from 1.0 to 5.0.
total_orders
INT
Total number of orders placed at the restaurant.
is_active
BOOLEAN
Whether the restaurant is currently active (true/false).

 

5. SQL Queries for Data Analysis
Below are 20 SQL queries to analyze food delivery trends:
Total number of orders placed:
SELECT COUNT(*) FROM tbl_order_details;
Most popular restaurant:
SELECT restaurant_id, COUNT(*) as order_count FROM tbl_order_details GROUP BY restaurant_id ORDER BY order_count DESC LIMIT 1;
Average order value:
SELECT AVG(total_amount) From tbl_order_details;
Count of customers who placed more than 5 orders:
SELECT customer_id, COUNT(*) From tbl_order_details GROUP BY customer_id HAVING COUNT(*) > 5;
Number of pending orders:
SELECT COUNT(*) From tbl_order_details WHERE status = 'Pending';
Orders by cuisine type:
SELECT r.cuisine_type, COUNT(o.order_id) From tbl_order_details o JOIN tbl_restaurant r ON o.restaurant_id = r.restaurant_id GROUP BY r.cuisine_type;
Top 5 customers based on total spending:
SELECT customer_id, SUM(total_amount) AS total_spent From tbl_order_details GROUP BY customer_id ORDER BY total_spent DESC LIMIT 5;
Orders completed within 30 minutes:
SELECT COUNT(*) FROM tbl_deliveries WHERE delivery_time - order_date <= INTERVAL '30 MINUTES';
Percentage of completed deliveries:
SELECT (COUNT(*) FILTER(WHERE delivery_status = 'Completed') * 100.0) / COUNT(*) AS completion_rate FROM tbl_deliveries;
Average delivery time:
SELECT AVG(EXTRACT(EPOCH FROM delivery_time - order_date) / 60) AS avg_delivery_time FROM tbl_deliveries;
Restaurant with the highest revenue:
SELECT restaurant_id, SUM(total_amount) From tbl_order_details GROUP BY restaurant_id ORDER BY SUM(total_amount) DESC LIMIT 1;
Orders by month:
SELECT DATE_TRUNC('month', order_date) AS month, COUNT(*) From tbl_order_details GROUP BY month;
Customer retention rate:
SELECT COUNT(DISTINCT customer_id) * 100.0 / (SELECT COUNT(*) FROM tbl_customers) From tbl_order_details;
Percentage of orders that include delivery:
SELECT (COUNT(DISTINCT order_id) * 100.0) / (SELECT COUNT(*) From tbl_order_details) FROM tbl_deliveries;
Restaurant with the most late deliveries:
SELECT restaurant_id, COUNT(*) FROM tbl_deliveries WHERE delivery_status = 'Pending' GROUP BY restaurant_id ORDER BY COUNT(*) DESC LIMIT 1;
Average number of items per order:
SELECT AVG(item_count) From tbl_order_details;
Peak order hours:
SELECT EXTRACT(HOUR FROM order_date) AS hour, COUNT(*) From tbl_order_details GROUP BY hour ORDER BY COUNT(*) DESC;
Revenue per customer:
SELECT customer_id, SUM(total_amount) From tbl_order_details GROUP BY customer_id;
Most frequently ordered item:
SELECT cuisine_type, COUNT(*) FROM tbl_restaurant GROUP BY item_name ORDER BY COUNT(*) DESC LIMIT 1;
Order frequency per restaurant:
SELECT restaurant_id, COUNT(*) From tbl_order_details GROUP BY restaurant_id ORDER BY COUNT(*) DESC;
 
6. Instructions to Run the Project
Prerequisites
Install Python 3.8+
Install dependencies using:
pip install streamlit pandas numpy sqlalchemy
Set up the database using the schema provided.
Run the Streamlit App
streamlit run app.py

 Conclusion
This tool empowers Zomato’s team with efficient food delivery data management, real-time analytics, and enhanced customer insights.
 


