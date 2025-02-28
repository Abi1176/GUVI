
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
class ZomatoClass:
    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.conn = None
        self.cursor = None
        self.create_connection()

    def create_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database
            )
            if self.conn.is_connected():
                print("Connected to MySQL database")
                self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


    def fetch_orders(self):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()

            query = "SELECT * FROM tbl_order_details order by order_id desc"
            df = pd.read_sql(query, self.conn)
            return df
        except Error as e:
            print(f"Error fetching orders: {e}")
            return pd.DataFrame()

    def fetch_restaurant(self):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()

            query = "SELECT * FROM tbl_restaurant"
            df = pd.read_sql(query, self.conn)
            return df
        except Error as e:
            print(f"Error fetching restaurants: {e}")
            return pd.DataFrame()

    def insert_order(self, order):
        #Inserts a new order into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = """
            INSERT INTO tbl_order_details ( customer_id,	restaurant_id, order_date,
            delivery_time,
            status,
            total_amount,
            payment_mode,
            discount_applied,
            feedback_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, order)
            self.conn.commit()
            print("Order inserted successfully!")
        except Error as e:
            print(f"Error inserting order: {e}")
    
    def insert_customers(self,name, email, phone, address, date, ispremium, preferedcuisine):
    #Inserts a new customer into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = """
            INSERT INTO tbl_customers(name,
            email,
            phone,
            location,
            signup_date,
            is_premium,
            preferred_cuisine
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, phone, address, date, ispremium, preferedcuisine))
            self.conn.commit()
            print("Customer inserted successfully!")
        except Error as e:
            print(f"Error inserting customer: {e}")

    def update_customers(self,name, email, phone, location,ispremium, preferedcuisine, customer_id):
    #Updates an existing customer in the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = """
            UPDATE tbl_customers
            SET name = %s,
            email = %s,
            phone = %s,
            location = %s,
            is_premium = %s,
            preferred_cuisine = %s
        WHERE customer_id = %s
            """
            self.cursor.execute(query, (name, email, phone, location, ispremium, preferedcuisine, customer_id))
            self.conn.commit()

            print("Customer updated successfully!")
        except Error as e:
            print(f"Error updating customer: {e}")

    def delete_customers(self,customer_id): 
    #Deletes an existing customer from the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = "DELETE FROM tbl_customers WHERE customer_id = %s"
            self.cursor.execute(query, (customer_id,))
            # Check if a row was actually deleted
            if self.cursor.rowcount == 0:
                print("No customer found with the given ID. Nothing deleted.")
            else:
                self.conn.commit()
            print("Customer deleted successfully!")
        except Error as e:
            print(f"Error deleting customer: {e}")

    def delete_customer_by_name(self,name): 
    #Deletes an existing customer from the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = "DELETE FROM tbl_customers WHERE name = %s"
            self.cursor.execute(query, (name,))
            self.conn.commit()
            print("Customer deleted successfully!")
        except Error as e:
            print(f"Error deleting customer: {e}")

    def insert_Delivery_Persons(self,delivery_person):
    #Inserts a new customer into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = """
            INSERT INTO tbl_delivery_persons(name,
            contact_number,
            vehicle_type,
            total_deliveries,
            average_rating,
            location)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, delivery_person)
            self.conn.commit()
            print("Delivery person details inserted successfully!")
        except Error as e:
            print(f"Error inserting delivery person: {e}")

    def insert_Restaurants(self,restaurant):
    #Inserts a new Restaurant into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = """
            INSERT INTO tbl_restaurant(name,
            cuisine_type,
            location,
            owner_name,
            average_delivery_time,
            contact_number,
            rating,
            total_orders,
            is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, restaurant)
            self.conn.commit()
            print("Restaurant details inserted successfully!")
        except Error as e:
            print(f"Error inserting restaurant: {e}")

    def insert_deliverys(self,delivery):
    #Inserts a new delivery into the database.
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = """
            INSERT INTO tbl_deliveries(order_id,
            delivery_person_id,
            delivery_status,
            distance,
            delivery_time,
            estimated_time,
            delivery_fee,
            vehicle_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, delivery)
            self.conn.commit()
            print("Delivery details inserted successfully!")
        except Error as e:
            print(f"Error inserting delivery: {e}")     

    def get_all_active_restaurants(self):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = "SELECT name,cuisine_type,location,contact_number FROM tbl_restaurant WHERE is_active=1"
            df = pd.read_sql(query, self.conn)
            return df
        except Error as e:
            print(f"Error fetching active restaurants: {e}")
            return pd.DataFrame()

    def delete_order(self, order_id):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = "DELETE FROM tbl_order_details WHERE order_id = %s"
            self.cursor.execute(query, (order_id,))
            self.conn.commit()
            print("Order deleted successfully!")
        except Error as e:
            print(f"Error deleting order: {e}")

    def delete_restaurant(self, restaurant_id):
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            query = "DELETE FROM tbl_restaurant WHERE restaurant_id = %s"
            self.cursor.execute(query, (restaurant_id,))
            self.conn.commit()
            print("Restaurant deleted successfully!")
        except Error as e:
            print(f"Error deleting restaurant: {e}")

    #Helper function to run queries and return DataFrame.
    def fetch_data(self, query):
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return pd.DataFrame(rows, columns=columns)

    #  Total Customers
    def get_total_customers(self):
        return self.fetch_data("SELECT COUNT(*) AS total_customers FROM tbl_customers;")

    #get all customers with join query
    def get_all_customers(self):
        return self.fetch_data("""
            SELECT  c.name, c.email, c.phone, c.location, c.signup_date, c.is_premium, c.preferred_cuisine, c.total_orders, c.average_rating,c.customer_id
            FROM tbl_customers c order by c.customer_id desc;
        """)


    #  New Customers This Month
    def get_new_customers(self):
        return self.fetch_data("""
            SELECT COUNT(*) AS new_customers 
            FROM tbl_customers 
            WHERE signup_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH);
        """)

    # Top 5 Customers by Order Count
    def get_top_customers(self):
        return self.fetch_data("""
            SELECT name, total_orders, average_rating
            FROM tbl_customers 
            ORDER BY total_orders DESC 
            LIMIT 5;
        """)

    # Monthly Order Trend
    def get_orders_per_month(self):
        return self.fetch_data("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS order_count 
            FROM tbl_order_details 
            GROUP BY month 
            ORDER BY month;
        """)

    # Peak Order Hours
    def get_peak_hours(self):
        return self.fetch_data("""
            SELECT HOUR(order_date) AS hour, COUNT(*) AS order_count 
            FROM tbl_order_details 
            GROUP BY hour 
            ORDER BY order_count DESC 
            LIMIT 5;
        """)

    # Revenue Trend
    def get_revenue_trend(self):
        return self.fetch_data("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(total_amount) AS revenue 
            FROM tbl_order_details 
            GROUP BY month 
            ORDER BY month;
        """)

    # Top Restaurants by Revenue
    def get_top_restaurants(self):
        return self.fetch_data("""
            SELECT r.name, SUM(o.total_amount) AS total_revenue 
            FROM tbl_restaurant r
            JOIN tbl_order_details o ON r.restaurant_id = o.restaurant_id
            GROUP BY r.name 
            ORDER BY total_revenue DESC 
            LIMIT 5;
        """)

    # Order Status Distribution
    def get_status_distribution(self):
        return self.fetch_data("""
            SELECT status, COUNT(*) AS count 
            FROM tbl_order_details 
            GROUP BY status;
        """)

    # Top Delivery Persons by Rating
    def get_top_delivery_persons(self):
        return self.fetch_data("""
            SELECT name, total_deliveries, average_rating 
            FROM tbl_delivery_persons
            ORDER BY average_rating DESC 
            LIMIT 5;
        """)

    # Delivery Performance Analysis
    def get_delivery_performance(self):
        return self.fetch_data("""
            SELECT vehicle_type, AVG(delivery_time - estimated_time) AS avg_delay, COUNT(*) AS total_deliveries
            FROM tbl_deliveries 
            GROUP BY vehicle_type;
        """)

    #get_delivery_performance_by_person()
    def get_delivery_performance_by_person(self):
        return self.fetch_data("""
            SELECT d.delivery_person_id, dp.name, dp.vehicle_type, AVG(d.delivery_time - d.estimated_time) AS avg_delay, COUNT(*) AS total_deliveries
            FROM tbl_deliveries d
            JOIN tbl_delivery_persons dp ON d.delivery_person_id = dp.delivery_person_id
            GROUP BY d.delivery_person_id;
        """)


    #most common customer location
    def get_common_location(self):
        return self.fetch_data("""
            SELECT location, COUNT(*) AS count
            FROM tbl_customers
            GROUP BY location
            ORDER BY count DESC
            LIMIT 1;
        """)

    #most common cuisine type
    def get_common_cuisine(self):
        return self.fetch_data("""
            SELECT cuisine_type, COUNT(*) AS count
            FROM tbl_restaurant
            GROUP BY cuisine_type
            ORDER BY count DESC
            LIMIT 1;
        """)

    #most common delivery person location
    def get_common_delivery_location(self):
        return self.fetch_data("""
            SELECT location, COUNT(*) AS count
            FROM tbl_delivery_persons
            GROUP BY location
            ORDER BY count DESC
            LIMIT 1;
        """)

    #Monthly Order Trend
    def get_monthly_order_trend(self):
        return self.fetch_data("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS order_count
            FROM tbl_order_details
            GROUP BY month
            ORDER BY month;
        """)

    #peek orders per month
    def get_peak_orders_per_month(self):
        return self.fetch_data("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS order_count
            FROM tbl_order_details
            GROUP BY month
            ORDER BY order_count DESC
            LIMIT 1;
        """)
    
    #peek orders per day
    def get_peak_orders_per_day(self):
        return self.fetch_data("""
            SELECT DAYNAME(order_date) AS day, COUNT(*) AS order_count
            FROM tbl_order_details
            GROUP BY day
            ORDER BY order_count DESC
            LIMIT 1;
        """)
    
    #get_daily_orders
    def get_daily_orders(self):
        return self.fetch_data("""
            SELECT DATE_FORMAT(order_date, '%Y-%m-%d') AS day, COUNT(*) AS order_count
            FROM tbl_order_details
            GROUP BY day
            ORDER BY day;
        """)

    #get_hourly_order_trend
    def get_hourly_order_trend(self):
        return self.fetch_data("""
            SELECT HOUR(order_date) AS hour, COUNT(*) AS order_count
            FROM tbl_order_details
            GROUP BY hour
            ORDER BY hour;
        """)
    
    #getPremium Members
    def get_premium_members(self):
        return self.fetch_data("""
            SELECT name, email, phone, location, signup_date, preferred_cuisine,is_premium
            FROM tbl_customers
            WHERE is_premium = 1;
        """)
    #get_common_delivery_person
    def get_common_delivery_person(self):
        return self.fetch_data("""
            SELECT name, contact_number, vehicle_type, total_deliveries, average_rating, location
            FROM tbl_delivery_persons
            ORDER BY total_deliveries DESC
            LIMIT 1;
        """)
    
    #get_popular_restaurant
    def 
