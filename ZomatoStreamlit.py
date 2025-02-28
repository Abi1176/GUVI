from PIL import Image
from Scripts.DBConnection import ZomatoClass
import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import matplotlib.pyplot as plt

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
        "<h1 style='text-align: left; color: #FF5733; font-size: 35px; '> Zomato Food Delivery Data Insights  </h1>", 
        unsafe_allow_html=True) 
        # Sidebar
        st.sidebar.title("Menu")
        
        # Top-Level Navigation
        section = st.sidebar.radio("Select Section:", ["Home","CRUD Operations", "Data Insights"])

         # Display Image Only on Home Page
        if section == "Home":
            image = Image.open("D:/Sample_Projects/ZomatoInsights/ZomatoInsights/Scripts/images/img.jpeg")

            # Resize the image (width=400, height=300)
            image_resized = image.resize((400, 300))
            st.image(image_resized, caption="Welcome!", use_container_width=True)
            st.markdown("<h3 style='text-align: center; color: lightblue;'>Let's Explore the Features! Select an option from the sidebar to get started!</h3>", unsafe_allow_html=True)


        if section == "CRUD Operations":
            st.sidebar.subheader("CRUD Operations") 
            menu = ["View Customers", "Add Customer", "Delete Customer", "Update Customer","View Orders","View Restaurants"]
            choice = st.sidebar.selectbox("Select Action", menu)

            # View Customers
            if choice == "View Customers":
                st.subheader("View All Customers")
                try:
                    df = db_obj.get_all_customers()
                    st.dataframe(df)
                except Error as e:
                    print(f"Error fetching customers: {e}")
            # View Orders
            elif choice == "View Orders":
                st.subheader("View All Orders")
                try:
                    df = db_obj.fetch_orders()
                    st.dataframe(df)
                except Error as e:
                    print(f"Error fetching orders: {e}")
            # View Restaurants
            elif choice == "View Restaurants":
                st.subheader("All View Restaurants")
                try:
                    df = db_obj.get_all_active_restaurants()
                    st.dataframe(df)
                except Error as e:
                    print(f"Error fetching restaurants: {e}")
                
            # Add Customer  
            elif choice == "Add Customer":
                st.subheader("Add Customer")
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                address = st.text_input("Location")
                ispremium = st.checkbox("Premium Customer")
                if ispremium:
                    ispremium=1
                else:
                    ispremium=0
                preferedcuisine = st.selectbox("Prefered Cuisine",["North Indian", "South Indian", "Chinese", "Italian", "Continental"])

                if st.button("Add"):
                    try:
                        db_obj.insert_customers(name, email, phone, address, pd.Timestamp.now(), ispremium, preferedcuisine)
                        st.success("Customer Added!")
                    except Error as e:
                        print(f"Error adding customer: {e}")

            # Delete Customer 
            elif choice == "Delete Customer":
                st.subheader("Delete Customer")
                id = st.text_input("Customer ID")

                #name= st.selectbox("Select Customer", db_obj.get_all_customers()["name"])
                #id=st.selectbox("Select Customer", db_obj.get_all_customers()["id"])
                if st.button("Delete"):
                    try:
                        db_obj.delete_customers(id)
                        st.success("Customer Deleted!")
                    except Error as e:
                        print(f"Error deleting customer: {e}")

            # Update Customer
            elif choice == "Update Customer":
                st.subheader("Update Customer")
                #st.selectbox("Select Customer", db_obj.get_all_customers()["name"])
                # df=db_obj.get_all_customers()
                #id = df[df["name"]==st.selectbox("Select Customer", db_obj.get_all_customers()["name"])]["id"].values[0]   
                customer_id = st.text_input("Customer ID")
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                location = st.text_input("Location")
                ispremium = st.checkbox("Premium Customer")
                if ispremium:
                    ispremium=1
                else:
                    ispremium=0
                preferedcuisine = st.selectbox("Prefered Cuisine",["North Indian", "South Indian", "Chinese", "Italian", "Continental"])
                if st.button("Update"):
                    try:
                        db_obj.update_customers(name, email, phone, location,ispremium, preferedcuisine, customer_id)
                        st.success("Customer Updated!")
                    except Error as e:
                        print(f"Error updating customer: {e}")  

        elif section == "Data Insights":
            st.sidebar.subheader("Data Insights")
            insights_menu = ["Top Customers","New Customers", "Delivery Performance by Person", "Delivery Performance by Vehicle Type","Most Ordered Food", "Revenue Trends", "Premium Members","Top Restaurants","Monthly Orders","Peak Orders Per Month","Peak Orders Per Day","Peak Orders Per Hour",
                             "Daily Orders","Hourly Orders","Common Cuisine","Common Delivery Person","Common Location","Most popular restaurant"]
            
            insights_choice = st.sidebar.selectbox("Select Insight", insights_menu)

            if insights_choice == "Top Customers":
                st.subheader("Top 5 Customers by Orders")
                #query = "SELECT name, total_orders FROM tbl_customers ORDER BY total_orders DESC LIMIT 5"
                df = db_obj.get_top_customers()
                st.dataframe(df)

                # #plot the bar chart
                # fig, ax = plt.subplots()
                # ax.barh(df["name"], df["total_orders"], color="green")
                # ax.set_xlabel("Total Orders")
                # ax.set_ylabel("Customer Name")
                # ax.set_title("Top 5 Customers by Orders")
                # st.pyplot(fig)
                                
            elif insights_choice == "Most Ordered Food":
                st.subheader("Most Ordered Food Items")    
                df = db_obj.get_common_cuisine()
                st.dataframe(df)

                #plot the bar chart
                fig, ax = plt.subplots()
                ax.barh(df["cuisine_type"], df["count"], color="green")
                ax.set_xlabel("Total Orders")
                ax.set_ylabel("Food Name")
                ax.set_title("Most Ordered Food Items")
                st.pyplot(fig)

           # Revenue Trends
            elif insights_choice == "Revenue Trends":
                st.subheader("Monthly Revenue Trends")
                df = db_obj.get_revenue_trend()
                st.line_chart(df.set_index("month"))

            # Premium Members vs Regular Customers
            elif insights_choice == "Premium Members":
                st.subheader("Premium Members vs Regular Customers")
                df = db_obj.get_premium_members()
                st.bar_chart(df.set_index("is_premium"))    

            elif insights_choice == "Top Restaurants":
                # Top 5 Restaurants - Bar Chart
                st.subheader(" Top 5 Earning Restaurants")
                df_top_restaurants = db_obj.get_top_restaurants()
                fig, ax = plt.subplots()
                ax.barh(df_top_restaurants["name"], df_top_restaurants["total_revenue"], color="green")
                ax.set_xlabel("Revenue")
                ax.set_ylabel("Restaurant Name")
                ax.set_title("Top 5 Restaurants by Revenue")
                st.pyplot(fig)   

            # New Customers
            elif insights_choice == "New Customers":
                st.subheader("New Customers This Month")                        
                new_customers = db_obj.get_new_customers().iloc[0,0]
                st.metric(label="New Customers This Month",value=new_customers)

            # #order per month - line chart
            elif insights_choice == "Monthly Orders":
                st.subheader("Monthly Orders")
                order_per_month = db_obj.get_monthly_order_trend()
                st.line_chart(order_per_month.set_index("month"))
            
            #peek orders per month - barchart
            elif insights_choice == "Peak Orders Per Month":
                st.subheader("Peak Orders Per Month")
                peak_orders_per_month = db_obj.get_peak_orders_per_month()    
                st.line_chart(peak_orders_per_month.set_index("month"))

            #peak order per day - line chart
            elif insights_choice == "Peak Orders Per Day":
                st.subheader("Peak Orders Per Day")
                peak_orders_per_day = db_obj.get_peak_orders_per_day()    
                st.line_chart(peak_orders_per_day.set_index("day"))
                
            

            elif insights_choice == "Peak Orders Per Hour":
                #peek orders per hour - barchart
                st.subheader("Peak Orders Per Hour")
                peak_orders_per_hour = db_obj.get_peak_hours()
                st.bar_chart(peak_orders_per_hour.set_index("hour"))

            elif insights_choice == "Daily Orders":
                st.subheader("Daily Orders")
                order_per_day = db_obj.get_daily_orders()
                st.line_chart(order_per_day.set_index("day"))

            elif insights_choice == "Hourly Orders":    
                st.subheader("Hourly Orders")
                order_per_hour = db_obj.get_hourly_order_trend()
                st.line_chart(order_per_hour.set_index("hour"))
              
            elif insights_choice == "Common Cuisine":
                st.subheader("Common Cuisine")
                common_cuisine = db_obj.get_common_cuisine()
                st.dataframe(common_cuisine)
                fig, ax = plt.subplots()
                ax.barh(common_cuisine["cuisine_type"], common_cuisine["count"], color="green")     
                ax.set_xlabel("Total Orders")
                ax.set_ylabel("Food Name")
                ax.set_title("Common Cuisine")
                st.pyplot(fig)

            elif insights_choice == "Common Delivery Person":
                st.subheader("Common Delivery Person")
                common_delivery_person = db_obj.get_common_delivery_person()
                st.dataframe(common_delivery_person)
                # fig, ax = plt.subplots()
                # ax.barh(common_delivery_person["name"], common_delivery_person["total_deliveries"], color="green")     
                # ax.set_xlabel("Total Deliveries")
                # ax.set_ylabel("Delivery Person")
                # ax.set_title("Common Delivery Person")
                # st.pyplot(fig)

            elif insights_choice == "Delivery Performance by Vehicle Type":
                st.subheader("Delivery Performance")
                # Fetch data
                delivery_performance = db_obj.get_delivery_performance()

                # Check if data exists
                if not delivery_performance.empty:
                    st.dataframe(delivery_performance)

                    # Create Matplotlib figure
                    fig, ax = plt.subplots(figsize=(8, 5))  # Set size for better visibility
                    ax.barh(delivery_performance["vehicle_type"], delivery_performance["avg_delay"], color="green")

                    # Set labels and title
                    ax.set_xlabel("Average Delivery Delay (Minutes)")
                    ax.set_ylabel("Vehicle Type")
                    ax.set_title("Delivery Performance by Vehicle Type")

                    # Show the plot in Streamlit
                    st.pyplot(fig)
                else:
                    st.warning("No delivery performance data available.")

            #Delivery Performance by Person
            elif insights_choice == "Delivery Performance by Person":      
                st.subheader("Delivery Performance by Person")
                delivery_performance_person = db_obj.get_delivery_performance_person()
                st.dataframe(delivery_performance_person)
                fig, ax = plt.subplots()
                ax.barh(delivery_performance_person["name"], delivery_performance_person["avg_delay"], color="green")     
                ax.set_xlabel("Average Delivery Delay (Minutes)")
                ax.set_ylabel("Delivery Person")
                ax.set_title("Delivery Performance by Person")
                st.pyplot(fig)  

            elif insights_choice == "Common Location":
                st.subheader("Common Location")
                common_location = db_obj.get_common_location()
                st.dataframe(common_location)
                fig, ax = plt.subplots()
                ax.barh(common_location["location"], common_location["count"], color="green")     
                ax.set_xlabel("Total Orders")
                ax.set_ylabel("Location")
                ax.set_title("Common Location")
                st.pyplot(fig) 

            elif insights_choice =="Most popular restaurant":           
                st.subheader("Most popular restaurant")
                popular_restaurant = db_obj.get_popular_restaurant()
                st.dataframe(popular_restaurant)
                fig, ax = plt.subplots()
                ax.barh(popular_restaurant["name"], popular_restaurant["total_orders"], color="green")     
                ax.set_xlabel("Total Orders")
                ax.set_ylabel("Restaurant Name")
                ax.set_title("Most popular restaurant")
                st.pyplot(fig)



    # Run the main function
if __name__ == "__main__":
        main()
