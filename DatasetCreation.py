import streamlit as st
import mysql.connector
from mysql.connector import Error
from faker import Faker
import pandas as pd
import random

# Initialize Faker
fake = Faker()

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

    def execute_query(self, query):
    #execute with given query    
        try:
            if self.conn is None or not self.conn.is_connected():
                self.create_connection()
            self.cursor.execute(query)
            self.conn.commit()
            print("Query executed successfully!")
        except Error as e:
            print(f"Error executing query: {e}")
            
#Inserts Delivery Persons data into the database
# Initialize db config
config = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "user": "2B9qSGSxQso7gBp.root",
    "port": 4000,
    "password": "nLUDS0fz3HRQatbm",
    "database": "SAMPLEZOM"
}

db_obj = ZomatoClass(**config)

# function for creating Chennai Address
from faker import Faker
from faker.providers import BaseProvider
fake = Faker()
fake = Faker('en_IN')

class ChennaiAddressProvider(BaseProvider):
    def chennai_address(self):
        chennai_localities = [
            "T. Nagar", "Adyar", "Velachery", "Anna Nagar", "Mylapore", "Guindy",
            "Tambaram", "Perungudi", "Kodambakkam", "Nungambakkam", "Kilpauk","Chrompet"
        ]
        street = self.generator.street_name()
        locality = self.random_element(chennai_localities)
        return f"{street}, {locality}, Chennai, Tamil Nadu, India - {self.generator.postcode()}"
    
class TwoWheelerProvider(BaseProvider):
    def two_wheeler(self):
        two_wheelers = ["Bike", "Scooter", "Motorcycle", "Electric Bike", "Electric Scooter", "Moped"]
        return self.random_element(two_wheelers)


fake.add_provider(TwoWheelerProvider)

fake.add_provider(ChennaiAddressProvider)

# Create deliveryPersons table and insert data
deliveryPersonTable = []
for _ in range(1, 500):
    deliveryPersonTable.append((
        fake.name(),
        fake.unique.phone_number(),
        fake.two_wheeler(),
        random.randint(0, 300),
        random.uniform(0, 5),
        fake.chennai_address()
    ))
    db_obj.insert_Delivery_Persons(deliveryPersonTable[-1])

#Inserts customers data into the database
# Initialize db config
config = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "user": "2B9qSGSxQso7gBp.root",
    "port": 4000,
    "password": "nLUDS0fz3HRQatbm",
    "database": "SAMPLEZOM"
}

db_obj = ZomatoClass(**config)

# function for creating Chennai Address
from faker import Faker
from faker.providers import BaseProvider

class ChennaiAddressProvider(BaseProvider):
    def chennai_address(self):
        chennai_localities = [
            "T. Nagar", "Adyar", "Velachery", "Anna Nagar", "Mylapore", "Guindy",
            "Tambaram", "Perungudi", "Kodambakkam", "Nungambakkam", "Kilpauk","Chrompet"
        ]
        street = self.generator.street_name()
        locality = self.random_element(chennai_localities)
        return f"{street}, {locality}, Chennai, Tamil Nadu, India - {self.generator.postcode()}"

fake = Faker('en_IN')
fake.add_provider(ChennaiAddressProvider)

# Create customer table and insert data
CustTable = []
for _ in range(295, 500):
    CustTable.append((
        fake.name(),
        fake.unique.email(),
        fake.unique.phone_number(),
        fake.chennai_address(),
        fake.date_this_decade(),
        random.choice([True, False]),
        random.choice(["North Indian", "South Indian", "Chinese", "Italian", "Continental"]),
        random.randint(0, 100),
        random.uniform(0, 5)
    ))
    db_obj.insert_customers(CustTable[-1])
#Inserts Restaurant data into the database
# Initialize db config
config = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "user": "2B9qSGSxQso7gBp.root",
    "port": 4000,
    "password": "nLUDS0fz3HRQatbm",
    "database": "SAMPLEZOM"
}

db_obj = ZomatoClass(**config)

# function for creating Chennai Address
from faker import Faker
from faker.providers import BaseProvider

class ChennaiAddressProvider(BaseProvider):
    def chennai_address(self):
        chennai_localities = [
            "T. Nagar", "Adyar", "Velachery", "Anna Nagar", "Mylapore", "Guindy",
            "Tambaram", "Perungudi", "Kodambakkam", "Nungambakkam", "Kilpauk","Chrompet"
        ]
        street = self.generator.street_name()
        locality = self.random_element(chennai_localities)
        return f"{street}, {locality}, Chennai, Tamil Nadu, India - {self.generator.postcode()}"

fake = Faker('en_IN')
fake.add_provider(ChennaiAddressProvider)

# List of cuisine types
cuisine_types = [
    "South Indian", "North Indian", "Chettinad", "Andhra", "Kerala", "Biryani", "Seafood",
    "Chinese", "Thai", "Japanese", "Korean", "Italian", "Mexican", "French", "Mediterranean",
    "Continental", "BBQ", "Fast Food", "Street Food", "Cafe", "Bakery", "Desserts", "Juice Bar"
]

# Prefix and suffix lists for restaurant names
prefixes = ["Spicy", "Royal", "Tandoori", "Grand", "Golden", "Classic", "Chennai", "Madras", "Authentic", "Savor", "Flavors of", "Delicious"]
suffixes = ["Kitchen", "Bistro", "Diner", "Cafe", "Grill", "Lounge", "Eatery", "Corner", "Spot", "Point", "House", "Hut"]

# Generate 200 unique restaurant names
restaurants = []
while len(restaurants) < 200:
    name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
    cuisine = random.choice(cuisine_types)
    restaurant_entry = f"\"{name} ({cuisine})\""
    
    if restaurant_entry not in restaurants:
        restaurants.append(restaurant_entry)


# Create Restaurant table and insert data
RestaurantTable = []
for _ in range(1, 200):
    RestaurantTable.append((
        restaurants[_-1],
        random.choice(["North Indian", "South Indian", "Chinese", "Italian", "Continental"]),
        fake.chennai_address(),
        fake.name(),
        random.randint(0, 120),
        fake.unique.phone_number(),
        random.uniform(0, 5),
        random.randint(0, 3000),
        random.choice([True, False])      
    ))
    db_obj.insert_Restaurants(RestaurantTable[-1])

    print(RestaurantTable[-1])


#Inserts order details data into the database
# Initialize db config
config = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "user": "2B9qSGSxQso7gBp.root",
    "port": 4000,
    "password": "nLUDS0fz3HRQatbm",
    "database": "SAMPLEZOM"
}

db_obj = ZomatoClass(**config)

# function for creating Chennai Address
from faker import Faker
from faker.providers import BaseProvider
from datetime import datetime, timedelta

fake = Faker()
fake = Faker('en_IN')

#fake_time = fake.date_time_between(start_date="today 06:00:00", end_date="today 21:00:00").time()
fake_time = fake.time(pattern="%H:%M:%S")

# Get the current date
current_date = datetime.today()


# Create oreder table and insert data
orderTable = []
for _ in range(1000, 1500):
    # Generate a fake order datetime within the last 2 years
    order_datetime = fake.date_time_between(start_date="-2y", end_date="now")

    # Set delivery datetime (30 minutes later)
    delivery_datetime = order_datetime + timedelta(minutes=85)  # Delivery 30 minutes after order time

    # Define possible statuses
    statuses = ['Pending','Delivered','Cancelled']
    # Set delivery status (assuming Pending until delivered or canceled)
    random_status = random.choice(statuses)  

    orderTable.append((
            random.randint(0, 500),
            random.randint(0, 199),
            order_datetime,
            delivery_datetime,
            random_status,
            round(random.uniform(1, 5000), 2),
            fake.random_element(["Credit Card", "Cash", "UPI"]),
            round(random.uniform(1, 50), 2),
            round(random.uniform(1, 5), 2)
        ))
       
    db_obj.insert_order(orderTable[-1])

df = pd.DataFrame(orderTable)
df