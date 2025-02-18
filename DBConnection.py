
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

            query = "SELECT * FROM tbl_order_details"
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

    
    def insert_customers(self,customer):
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
            preferred_cuisine,
            total_orders,
            average_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, customer)
            self.conn.commit()
            print("Customer inserted successfully!")
        except Error as e:
            print(f"Error inserting customer: {e}")
            
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


     