import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
import numpy as np

# Inject custom CSS for transparency and styling
st.markdown(
    """
    <style>
    /* Make the sidebar background transparent */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
    }

    /* Custom styling for headers */
    .css-1d391kg {
        background-color: transparent !important;
        color: white !important;
    }

    /* Make subheaders transparent with white text */
    h2, h4 {
        background-color: rgba(0, 0, 0, 0.5);
        color: white !important;
        padding: 10px;
        border-radius: 10px;
    }

    /* Background customization */
    .stApp {
        background-image: url("https://wallpaperboat.com/wp-content/uploads/2019/10/website-background-texture-15.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Beautiful Header with transparent background
st.markdown("""
    <div style="background-color:rgba(0, 0, 0, 0.7);padding:10px;border-radius:10px;text-align:center">
        <h2 style="color:white;">Post Office Data Management Dashboard</h2>
        <h4 style="color:white;">Real-time Data Management and Visualization</h4>
    </div>
    <br>
""", unsafe_allow_html=True)

# Function to establish a database connection
def get_connection():
    conn = sqlite3.connect('post_office.db')
    return conn

    

    

def execute_read_query(query, params=()):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('post.db')
        c = conn.cursor()
        
        # Execute the query with optional parameters
        c.execute(query, params)
        
        # Fetch all results from the executed query
        result = c.fetchall()
        
        # Close the database connection
        conn.close()
        
        return result
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

# Function to execute queries
def execute_query(query, params=()):
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

    
 # Function to fetch data from the database
# Function to fetch data from the database with error handling
def fetch_data(query):
    conn = sqlite3.connect("post_office.db")
    c = conn.cursor()
    try:
        c.execute(query)
        rows = c.fetchall()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        rows = []
    finally:
        conn.close()
    return rows
# Function to load data from SQLite database
def load_data(table_name):
    conn = sqlite3.connect('post_office.db')  # Ensure this path is correct
    query = f"SELECT * FROM {table_name}"
    print(f"Executing query: {query}")  # Debugging statement
    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error occurred while fetching data from {table_name}: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        conn.close()

    return df

    

# Function to display customer details
def display_customers():
    st.subheader("Customers")
    df = load_data('customers')
    st.dataframe(df)

# Function to add a new customer
def add_customer():
    st.subheader("Add New Customer")
    with st.form("customer_form"):
        name = st.text_input("Name")
        address = st.text_area("Address")
        contact_number = st.text_input("Contact Number")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add Customer")
        if submitted:
            if name and address:
                query = '''
                    INSERT INTO customers (name, address, contact_number, email)
                    VALUES (?, ?, ?, ?)
                '''
                execute_query(query, (name, address, contact_number, email))
                st.success("Customer added successfully!")
            else:
                st.error("Name and Address are required fields.")

# Function to update an existing customer
def update_customer():
    st.subheader("Update Customer")
    df = load_data('customers')
    customer_ids = df['customer_id'].tolist()
    selected_id = st.selectbox("Select Customer ID to Update", customer_ids)
    customer = df[df['customer_id'] == selected_id].iloc[0]
    
    with st.form("update_form"):
        name = st.text_input("Name", value=customer['name'])
        address = st.text_area("Address", value=customer['address'])
        contact_number = st.text_input("Contact Number", value=customer['contact_number'])
        email = st.text_input("Email", value=customer['email'])
        submitted = st.form_submit_button("Update Customer")
        if submitted:
            if name and address:
                query = '''
                    UPDATE customers
                    SET name = ?, address = ?, contact_number = ?, email = ?
                    WHERE customer_id = ?
                '''
                execute_query(query, (name, address, contact_number, email, selected_id))
                st.success("Customer updated successfully!")
            else:
                st.error("Name and Address are required fields.")

# Function to delete a customer
def delete_customer():
    st.subheader("Delete Customer")
    df = load_data('customers')
    customer_ids = df['customer_id'].tolist()
    selected_id = st.selectbox("Select Customer ID to Delete", customer_ids)
    if st.button("Delete Customer"):
        query = '''
            DELETE FROM customers
            WHERE customer_id = ?
        '''
        execute_query(query, (selected_id,))
        st.success("Customer deleted successfully!")

# Function to display services
def display_services():
    st.subheader("Services")
    df = load_data('services')
    st.dataframe(df)

# Function to add a new service
def add_service():
    st.subheader("Add New Service")
    with st.form("service_form"):
        service_name = st.text_input("Service Name")
        service_type = st.selectbox("Service Type", ["Mail Services", "Financial Services", "Philately", "Counter Services"])
        submitted = st.form_submit_button("Add Service")
        if submitted:
            if service_name and service_type:
                query = '''
                    INSERT INTO services (service_name, service_type)
                    VALUES (?, ?)
                '''
                execute_query(query, (service_name, service_type))
                st.success("Service added successfully!")
            else:
                st.error("Service Name and Service Type are required fields.")

# Function to update an existing service
def update_service():
    st.subheader("Update Service")
    df = load_data('services')
    service_ids = df['service_id'].tolist()
    selected_id = st.selectbox("Select Service ID to Update", service_ids)
    service = df[df['service_id'] == selected_id].iloc[0]
    
    with st.form("update_service_form"):
        service_name = st.text_input("Service Name", value=service['service_name'])
        service_type = st.selectbox("Service Type", ["Mail Services", "Financial Services", "Philately", "Counter Services"], index=["Mail Services", "Financial Services", "Philately", "Counter Services"].index(service['service_type']))
        submitted = st.form_submit_button("Update Service")
        if submitted:
            if service_name and service_type:
                query = '''
                    UPDATE services
                    SET service_name = ?, service_type = ?
                    WHERE service_id = ?
                '''
                execute_query(query, (service_name, service_type, selected_id))
                st.success("Service updated successfully!")
            else:
                st.error("Service Name and Service Type are required fields.")

# Function to delete a service
def delete_service():
    st.subheader("Delete Service")
    df = load_data('services')
    service_ids = df['service_id'].tolist()
    selected_id = st.selectbox("Select Service ID to Delete", service_ids)
    if st.button("Delete Service"):
        query = '''
            DELETE FROM services
            WHERE service_id = ?
        '''
        execute_query(query, (selected_id,))
        st.success("Service deleted successfully!")

# Function to add a new delivery record
def add_delivery():
    st.subheader("Add New Delivery Record")
    with st.form("delivery_form"):
        delivery_id = st.text_input("Delivery ID")
        customer_id = st.text_input("Customer ID")
        delivery_status = st.selectbox("Delivery Status", ["Pending", "In Transit", "Delivered", "Failed"])
        estimated_delivery = st.date_input("Estimated Delivery Date")
        
        submitted = st.form_submit_button("Add Delivery Record")

        if submitted:
            if delivery_id and customer_id:
                query = '''
                    INSERT INTO delivery (delivery_id, customer_id, delivery_status, estimated_delivery)
                    VALUES (?, ?, ?, ?)
                '''
                try:
                    execute_query(query, (delivery_id, customer_id, delivery_status, str(estimated_delivery)))
                    st.success("Delivery record added successfully!")
                    st.write("Please refresh the page to view updated data.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Delivery ID and Customer ID are required fields.")

# Function to display delivery records
def display_deliveries():
    query = '''
        SELECT * FROM delivery
    '''
    try:
        records = execute_read_query(query)
        if records:
            st.write("Delivery Records:")
            for row in records:
                st.write(f"Delivery ID: {row[0]}, Customer ID: {row[1]}, Status: {row[2]}, Estimated Delivery: {row[3]}")
        else:
            st.write("No delivery records found.")
    except Exception as e:
        st.error(f"An error occurred while fetching delivery records: {e}")

# Delivery Management Menu
def delivery_menu():
    st.subheader("Delivery Management")
    
    action = st.selectbox("Select Action", ["View All Deliveries", "Add New Delivery"])

    if action == "View All Deliveries":
        display_deliveries()
    elif action == "Add New Delivery":
        add_delivery()
        



# Function to add an employee
def add_employee():
    st.subheader("Add Employee Information")
    employee_id = st.text_input("Employee ID")
    name = st.text_input("Name")
    position = st.text_input("Position")
    contact_number = st.text_input("Contact Number")
    email = st.text_input("Email")
    
    if st.button("Add Employee"):
        query = """
        INSERT INTO employees (employee_id, name, position, contact_number, email) 
        VALUES (?, ?, ?, ?, ?)
        """
        execute_query(query, (employee_id, name, position, contact_number, email))
        st.success("Employee added successfully")

# Function to fetch all employee data
def fetch_all_employees():
    query = "SELECT employee_id, name, position, contact_number, email FROM employees"
    return fetch_data(query)

# Function to display employee data
def display_employees():
    st.subheader("All Employees")
    employees = fetch_all_employees()
    if employees:
        df = pd.DataFrame(employees, columns=["Employee ID", "Name", "Position", "Contact Number", "Email"])
        st.table(df)
    else:
        st.write("No employee data available.")


# Function to display complaints
def display_complaints():
    st.subheader("Complaints")
    df = load_data('complaints')
    st.dataframe(df)

# Function to add complaint details
def add_complaint():
    st.subheader("Add Complaint")
    with st.form("complaint_form"):
        complaint_id = st.text_input("Complaint ID")
        customer_id = st.text_input("Customer ID")
        description = st.text_area("Description")
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])  # Example statuses
        created_at = st.date_input("Created At")

        submitted = st.form_submit_button("Add Complaint")

        if submitted:
            if complaint_id and customer_id and description and status and created_at:
                query = '''
                    INSERT INTO complaints (complaint_id, customer_id, description, status, created_at)
                    VALUES (?, ?, ?, ?, ?)
                '''
                st.write(f"Executing query: {query}")
                st.write(f"With parameters: {complaint_id}, {customer_id}, {description}, {status}, {created_at}")
                
                execute_query(query, (complaint_id, customer_id, description, status, created_at))
                st.success("Complaint added successfully!")
            else:
                st.error("All fields are required.")

# Example execute_query function
def execute_query(query, params):
    try:
        conn = sqlite3.connect('post_office.db')  # Adjust your database connection
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()

# Function to display feedback
def display_feedback():
    st.subheader("Feedback")
    df = load_data('feedback')
    st.dataframe(df)

# Feedback Management Functions
def feedback_menu():
    st.subheader("Feedback Management")
    action = st.selectbox("Select Action", ["View All Feedback", "Add Feedback"])
    if action == "View All Feedback":
        display_feedback()
    elif action == "Add Feedback":
        add_feedback()

def add_feedback():
    st.subheader("Add New Feedback")
    with st.form("feedback_form"):
        feedback_id = st.text_input("Feedback ID")
        customer_id = st.text_input("Customer ID")
        rating = st.slider("Rating", min_value=1, max_value=5)
        comments = st.text_area("Comments")
        created_at = st.date_input("Date Created")
        submitted = st.form_submit_button("Add Feedback")

        if submitted:
            if feedback_id and customer_id:
                query = '''
                    INSERT INTO feedback (feedback_id, customer_id, rating, comments, created_at)
                    VALUES (?, ?, ?, ?, ?)
                '''
                try:
                    # Execute the query with the provided parameters
                    execute_query(query, (feedback_id, customer_id, rating, comments, str(created_at)))
                    st.success("Feedback added successfully!")
                    st.experimental_rerun()  # Force page refresh to display updated data
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Feedback ID and Customer ID are required fields.")



def add_office_performance():
    st.subheader("Add New Office Performance Record")
    with st.form("performance_form"):
        performance_id = st.text_input("Performance ID")
        month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", 
                                       "July", "August", "September", "October", "November", "December"])
        year = st.number_input("Year", min_value=2000, max_value=2100, step=1)
        total_customers = st.number_input("Total Customers", min_value=0, step=1)
        total_services = st.number_input("Total Services", min_value=0, step=1)
        total_complaints = st.number_input("Total Complaints", min_value=0, step=1)
        total_feedbacks = st.number_input("Total Feedbacks", min_value=0, step=1)
        
        submitted = st.form_submit_button("Add Performance Record")

        if submitted:
            if performance_id and month and year:
                query = '''
                    INSERT INTO office_performance (performance_id, month, year, total_customers, total_services, total_complaints, total_feedbacks)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
                try:
                    execute_query(query, (performance_id, month, year, total_customers, total_services, total_complaints, total_feedbacks))
                    st.success("Performance record added successfully!")
                    # Manual refresh logic (no need for experimental_rerun)
                    st.write("Please refresh the page to view updated data.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Performance ID, Month, and Year are required fields.")

# Function to display office performance records
def display_office_performance():
    query = '''
        SELECT * FROM office_performance
    '''
    try:
        records = execute_read_query(query)
        if records:
            st.write("Office Performance Records:")
            for row in records:
                st.write(f"Performance ID: {row[0]}, Month: {row[1]}, Year: {row[2]}, Total Customers: {row[3]}, Total Services: {row[4]}, Total Complaints: {row[5]}, Total Feedbacks: {row[6]}")
        else:
            st.write("No performance records found.")
    except Exception as e:
        st.error(f"An error occurred while fetching performance records: {e}")

# Office Performance Menu
def office_performance_menu():
    st.subheader("Office Performance Management")
    
    action = st.selectbox("Select Action", ["View Office Performance", "Add Office Performance"])

    if action == "View Office Performance":
        display_office_performance()
    elif action == "Add Office Performance":
        add_office_performance()

    


# Function to display interactive maps
def display_map():
    st.subheader("Customer Locations")
    df = load_data('customers')

    if not df.empty:
        # Generate random latitudes and longitudes for testing
        np.random.seed(0)  # For reproducibility
        df['latitude'] = np.random.uniform(low=12.0, high=15.0, size=len(df))
        df['longitude'] = np.random.uniform(low=75.0, high=80.0, size=len(df))

        customer_map = folium.Map(location=[13.0, 77.0], zoom_start=6)

        for i, row in df.iterrows():
            folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(customer_map)

        st_folium(customer_map, width=700, height=500)


       


# Main function
def main():
    st.title("Post Office Management Dashboard")
    
    menu = ["Home", "Customers", "Services","Delivery Management", "Employees", "Complaints", "Feedback", "Office Performance", "Map"]
    choice = st.sidebar.selectbox("Menu", menu)

    

    if choice == "Home":
        st.subheader("Welcome to the Post Office Management Dashboard")
        st.write("Use the sidebar to navigate through different sections.")
    elif choice == "Customers":
        display_customers()
        add_customer()
        update_customer()
        delete_customer()
    elif choice == "Services":
        display_services()
        add_service()
        update_service()
        delete_service()
    elif choice == "Delivery Management":
        display_deliveries()
        add_delivery()
    elif choice == "Employees":
        display_employees()
        add_employee()
    elif choice == "Complaints":
        display_complaints()
        add_complaint()
    elif choice == "Feedback":
        display_feedback()
        add_feedback()
    elif choice == "Office Performance":
        display_office_performance()
        add_office_performance()
    elif choice == "Map":
        display_map()

if __name__ == "__main__":
    main()
