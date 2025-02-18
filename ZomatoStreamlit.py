from PIL import Image
from Scripts.DBConnection import ZomatoClass
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Initialize DB Connection
db_obj = ZomatoClass(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    user="2B9qSGSxQso7gBp.root",
    password="nLUDS0fz3HRQatbm",
    port=4000,
    database="SAMPLEZOM"
)

def main():
    #Main function to run the Streamlit app.
        st.markdown(
        "<h1 style='text-align: center; color: #FF5733; font-size: 35px; '> Zomato Food Delivery Data Insights  </h1>", 
        unsafe_allow_html=True)       
        # Sidebar navigation
        menu = ["Home","View Restaurants","View Orders", "Add Order", "Update Order", "Delete Order", "View Queries"]
        choice = st.sidebar.selectbox("Menu", menu)

        # Home Page
        if choice == "Home":
            #st.markdown("<h2 style='text-align: center; color: black;'>✨ Zomato Food Delivery Data Insights ✨</h2>", unsafe_allow_html=True)
            # Load and display image
            image = Image.open("D:\Sample_Projects\ZomatoInsights\ZomatoInsights\Scripts\images\img.jpeg")  
            st.image(image, caption="Welcome!", use_container_width =True)
            st.markdown("<h3 style='text-align: center; color: lightblue;'>Let's Explore the Features! Select an option from the sidebar to get started!</h3>", unsafe_allow_html=True)
           
        # View Orders
        elif choice == "View Orders":
            st.subheader("All View Orders")
            df = db_obj.fetch_orders()
            st.dataframe(df)
        # View Restaurants
        elif choice == "View Restaurants":
            st.subheader("All View Restaurants")
            df = db_obj.fetch_restaurant()
            st.dataframe(df)
        # Add Order
        elif choice == "Add Order":
            st.subheader("Add New Order")
            id = st.text_input("Order ID")
            customer_name = st.text_input("Customer Name")
            customer_address = st.text_area("Customer Address")
            restaurant_name = st.text_input("Restaurant Name")
            food_item = st.text_input("Food Item")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            price = st.number_input("Price", min_value=0.0, step=0.1)
            total_price = quantity * price
            order_time = st.text_input("Order Time (YYYY-MM-DD HH:MM:SS)")
            delivery_time = st.text_input("Delivery Time (YYYY-MM-DD HH:MM:SS)")
            status = st.selectbox("Status", ["Delivered", "Pending", "Cancelled"])
            # Submit button
            if st.button("Submit Order"):
                order_data = (id, customer_name, customer_address, restaurant_name, food_item, quantity, price, total_price, order_time, delivery_time, status)
                db_obj.insert_order(order_data)
                st.success("Order inserted successfully!")
    # Run the main function
if __name__ == "__main__":
        main()
