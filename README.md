# Zomato Food Delivery Data Insights

**1. Project Overview**

As a data scientist at Zomato, the goal of this project is to enhance operational efficiency and improve customer satisfaction by analyzing food delivery data. The interactive Streamlit tool enables seamless data entry and management of orders, customers, restaurants, and deliveries. The system supports robust database operations like adding columns or creating new tables dynamically while maintaining compatibility with existing code.


**2. Source Code**

This project consists of multiple Python scripts for dataset generation, database management, and Streamlit app development. The key components are:

**a. Dataset Generation (DatasetCreation.py)**

Generates synthetic food delivery data.
Exports data in CSV format for initial database seeding.

**b. Database Management (DBConnection.py)**

Establishes a connection to an MySQL Database.
Provides functions to create, update, and query tables dynamically.
Ensures compatibility with existing schema.

**c. Streamlit App (ZomatoStreamlit.py)**

Interactive interface for data entry and real-time analysis.
Allows users to insert, update, and view records.
Supports on-the-fly schema modifications.


**3. Streamlit App**
The Streamlit app is the front-end of this tool, designed to provide a user-friendly interface for managing and analyzing food delivery data.

**Key Features:**

**Data Entry:** Users can add new records for orders, customers, restaurants, and deliveries.

**Dynamic Table Management: **Ability to create new tables or add columns dynamically.

**Visual Analytics:** Data visualization through interactive charts.

**SQL Query Execution:** Run custom SQL queries for deeper insights.
 
 
**4. Database Schema**

The SQL database includes the following tables:

**a. tbl_customers**

       customer_id
       
       name
       
       email
       
       phone
       
       location
       
       signup_date
       
       is_premium
       
       preferred_cuisine
       
       total_orders
       
       average_rating
       
**Explanation:**

customer_id: Auto-incrementing primary key.

name: Stores the full name (up to 255 characters).

email: Unique constraint to ensure no duplicate emails.

phone: Unique constraint to ensure no duplicate phone numbers.

location: Text field to store the customer’s address.

signup_date: Date field for when the customer signed up.

is_premium: Boolean field (defaults to FALSE).

preferred_cuisine: Stores cuisine preference (e.g., "Italian", "Chinese").

total_orders: Integer field, defaults to 0.

average_rating: Decimal (3,2) ensures ratings are stored as X.XX and are between 0.00 and 5.00.

 
**b. tbl_delivery_persons**

     delivery_person_id
     
     name
     
     contact_number
     
     vehicle_type
     
     total_deliveries
     
     average_rating
     
     location
     
**Explanation:**

delivery_person_id: Auto-incrementing primary key.

name: Stores the full name of the delivery person.

contact_number: Unique constraint ensures no duplicate contact numbers.

vehicle_type: Enum field specifying the type of vehicle used.

total_deliveries: Integer field, defaults to 0, must be ≥ 0.

average_rating: Decimal (2,1) field for storing ratings between 1.0 and 5.0.

location: Text field for storing the current base location.

 
**c. tbl_order_details**

   order_id
   
   customer_id
   
   restaurant_id
   
   order_date
   
   delivery_time
   
   status
   
   total_amount
   
   payment_mode
   
   discount_applied
   
   feedback_rating
   
**Explanation:**

order_id: Auto-incrementing primary key.

customer_id: Foreign key referencing customers.customer_id.

restaurant_id: Foreign key referencing tbl_restaurant.restaurant_id.

order_date: Timestamp of when the order was placed.

delivery_time: Timestamp of when the order was delivered (nullable).

status: Enum field allowing only Pending, Delivered, or Cancelled, with a default of Pending.

total_amount: Decimal field to store order total (must be ≥ 0).

payment_mode: Enum field for allowed payment methods.

discount_applied: Decimal field for any discount applied (must be ≥ 0).

feedback_rating: Decimal (2,1) for storing ratings between 1.0 and 5.0.

ON DELETE CASCADE: Ensures orders are deleted if the corresponding customer or restaurant is removed.


**d. tbl_deliveries**

   delivery_id
   
   order_id
   
   delivery_person_id
   
   delivery_status
   
   distance
   
   delivery_time
   
   estimated_time
   
   delivery_fee
   
   vehicle_type
   
**Explanation:**

delivery_id: Auto-incrementing primary key.

order_id: Foreign key referencing tbl_order_details.order_id (ensures each delivery is linked to an order).

delivery_person_id: Foreign key referencing tbl_delivery_persons.delivery_person_id (nullable, as not every order may have an assigned delivery person).

delivery_status: Enum field for delivery progress (On the way, Delivered, Failed), with a default value of On the way.

distance: Decimal (5,2) to store distance in kilometers.

delivery_time: Integer field to store actual delivery duration (must be ≥ 0).

estimated_time: Integer field to store estimated delivery duration (must be ≥ 0).

delivery_fee: Decimal field to store delivery charges (must be ≥ 0).

vehicle_type: Enum field specifying vehicle type (e.g., Bike, Car, Scooter, Bicycle).

ON DELETE CASCADE for order_id: If an order is deleted, the corresponding delivery is also removed.

ON DELETE SET NULL for delivery_person_id: If a delivery person is removed, their deliveries remain, but the delivery_person_id is set to NULL.
 
**e. tbl_restaurant**

    restaurant_id
    
    name
    
    cuisine_type
    
    location
    
    owner_name
    
    average_delivery_time
    
    contact_number
    
    rating
    
    total_orders
    
    is_active
    
**Explanation:**

restaurant_id: Auto-incrementing primary key.

name: Stores the restaurant name (up to 255 characters).

cuisine_type: Cuisine category (e.g., Indian, Chinese).

location: Stores the restaurant’s location.

owner_name: Stores the name of the restaurant owner.

average_delivery_time: Integer field representing the average delivery time (must be ≥ 0).

contact_number: Unique constraint to ensure no duplicate contact numbers.

rating: Decimal (2,1) ensures ratings are stored as X.X and are between 1.0 and 5.0.

total_orders: Integer field, defaults to 0.

is_active: Boolean field, defaults to TRUE.

**5. SQL Queries for Data Analysis**

Below are 20 SQL queries to analyze food delivery trends:

**Total number of orders placed:**
SELECT COUNT(*) FROM tbl_order_details;

**Most popular restaurant:**
SELECT restaurant_id, COUNT(*) as order_count FROM tbl_order_details GROUP BY restaurant_id ORDER BY order_count DESC LIMIT 1;

**Average order value:**
SELECT AVG(total_amount) From tbl_order_details;

**Count of customers who placed more than 5 orders:**
SELECT customer_id, COUNT(*) From tbl_order_details GROUP BY customer_id HAVING COUNT(*) > 5;

**Number of pending orders:**
SELECT COUNT(*) From tbl_order_details WHERE status = 'Pending';

**Orders by cuisine type:**
SELECT r.cuisine_type, COUNT(o.order_id) From tbl_order_details o JOIN tbl_restaurant r ON o.restaurant_id = r.restaurant_id GROUP BY r.cuisine_type;

**Top 5 customers based on total spending:**
SELECT customer_id, SUM(total_amount) AS total_spent From tbl_order_details GROUP BY customer_id ORDER BY total_spent DESC LIMIT 5;

**Orders completed within 30 minutes:**
SELECT COUNT(*) FROM tbl_deliveries WHERE delivery_time - order_date <= INTERVAL '30 MINUTES';

**Percentage of completed deliveries:**
SELECT (COUNT(*) FILTER(WHERE delivery_status = 'Completed') * 100.0) / COUNT(*) AS completion_rate FROM tbl_deliveries;

**Average delivery time:**
SELECT AVG(EXTRACT(EPOCH FROM delivery_time - order_date) / 60) AS avg_delivery_time FROM tbl_deliveries;

**Restaurant with the highest revenue:**
SELECT restaurant_id, SUM(total_amount) From tbl_order_details GROUP BY restaurant_id ORDER BY SUM(total_amount) DESC LIMIT 1;

**Orders by month:**
SELECT DATE_TRUNC('month', order_date) AS month, COUNT(*) From tbl_order_details GROUP BY month;

**Customer retention rate:**
SELECT COUNT(DISTINCT customer_id) * 100.0 / (SELECT COUNT(*) FROM tbl_customers) From tbl_order_details;

**Percentage of orders that include delivery:**
SELECT (COUNT(DISTINCT order_id) * 100.0) / (SELECT COUNT(*) From tbl_order_details) FROM tbl_deliveries;

**Restaurant with the most late deliveries:**
SELECT restaurant_id, COUNT(*) FROM tbl_deliveries WHERE delivery_status = 'Pending' GROUP BY restaurant_id ORDER BY COUNT(*) DESC LIMIT 1;

**Average number of items per order:**
SELECT AVG(item_count) From tbl_order_details;

**Peak order hours:**
SELECT EXTRACT(HOUR FROM order_date) AS hour, COUNT(*) From tbl_order_details GROUP BY hour ORDER BY COUNT(*) DESC;

**Revenue per customer:**
SELECT customer_id, SUM(total_amount) From tbl_order_details GROUP BY customer_id;

**Most frequently ordered item:**
SELECT cuisine_type, COUNT(*) FROM tbl_restaurant GROUP BY item_name ORDER BY COUNT(*) DESC LIMIT 1;

**Order frequency per restaurant:**
SELECT restaurant_id, COUNT(*) From tbl_order_details GROUP BY restaurant_id ORDER BY COUNT(*) DESC;

 
**6. Instructions to Run the Project**

**Prerequisites**

Install Python 3.8+

**Install dependencies using:**

pip install streamlit pandas numpy sqlalchemy

Set up the database using the schema provided.

**Run the Streamlit App**

streamlit run app.py


**Conclusion**

This tool empowers Zomato’s team with efficient food delivery data management, real-time analytics, and enhanced customer insights.
 


