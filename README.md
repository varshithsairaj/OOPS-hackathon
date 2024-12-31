# **DISU: Data Insights and Strategic Unit**

## **Overview**  
DISU (Data Insights and Strategic Unit) is a robust platform designed to streamline the operations of the Department of Posts (DoP). This system enhances data-driven decision-making, operational efficiency, and customer satisfaction by combining data processing, analytics, and visualization.  

Developed during a hackathon, DISU addresses challenges in handling, analyzing, and visualizing large-scale data securely.

---

## **Features**  

### **Real-Time Dashboard**  
The platform provides a real-time, interactive dashboard that displays IoT device data and post office records, making it easier to track operations and performance.

### **Role-Based Access Control (RBAC)**  
Secure access is enforced through role-based access, ensuring only authorized personnel can manage or view data.

### **Feedback Management**  
Collects customer feedback with ratings and comments to evaluate service quality and improve customer experience.

### **Delivery Management**  
Tracks delivery records with real-time updates, including statuses like "In Transit," "Delivered," and "Pending."

### **Complaint Management**  
Handles customer complaints efficiently by tracking their status and ensuring timely resolutions.

### **Data Analytics**  
Provides advanced analytics, including visual graphs and annual reports, to help make informed strategic decisions.

---

## **Technologies Used**  

### **Frontend**  
- **Streamlit**: For an interactive, user-friendly web interface.

### **Backend**  
- **Python**: Backend logic and database interactions.  
- **SQLite**: Lightweight, efficient database to store and manage records.  

---

## **Project Structure**
```plaintext
📁 OOPS-Hackathon/
├── 📄 dashboard.py          # Main Streamlit app file
├── 📄 post_office.db        # SQLite database file
├── 📄 requirements.txt      # Python dependencies
├── 📄 LICENSE               # License for the project
└── 📄 README.md             # Project documentation
