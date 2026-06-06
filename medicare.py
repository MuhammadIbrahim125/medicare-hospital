import streamlit as st
import pandas as pd
from datetime import datetime, date
import uuid

# Page Configuration
st.set_page_config(
    page_title="MediCare Hospital",
    page_icon="🏥",
    layout="wide"

)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1E3A8A; font-weight: bold;}
    .sub-header {font-size: 1.5rem; color: #3B82F6;}
    .stButton>button {width: 100%;}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏥 MediCare Hospital Management System")
st.markdown("### Professional Hospital Management System")

# Initialize Session State
if 'patients' not in st.session_state:
    st.session_state.patients = pd.DataFrame(columns=[
        'Patient_ID', 'Name', 'Age', 'Gender', 'Phone', 'Address', 
        'Blood_Group', 'Registration_Date'
    ])

if 'doctors' not in st.session_state:
    st.session_state.doctors = pd.DataFrame(columns=[
        'Doctor_ID', 'Name', 'Specialization', 'Phone', 'Experience', 'Availability'
    ])

if 'appointments' not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=[
        'Appointment_ID', 'Patient_Name', 'Doctor_Name', 'Date', 'Time', 'Status'
    ])

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Main Menu",
    ["🏠 Dashboard", "👥 Patients", "👨‍⚕️ Doctors", "📅 Appointments", "📊 Reports"]
)

# ====================== DASHBOARD ======================
if menu == "🏠 Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", len(st.session_state.patients))
    with col2:
        st.metric("Total Doctors", len(st.session_state.doctors))
    with col3:
        st.metric("Today's Appointments", len(st.session_state.appointments))
    with col4:
        st.metric("Active Patients", len(st.session_state.patients))
    
    st.subheader("Recent Patients")
    if not st.session_state.patients.empty:
        st.dataframe(st.session_state.patients.tail(5), use_container_width=True)
    else:
        st.info("No patients registered yet.")

# ====================== PATIENTS ======================
elif menu == "👥 Patients":
    st.subheader("👥 Patient Management")
    
    tab1, tab2 = st.tabs(["Register New Patient", "View All Patients"])
    
    with tab1:
        with st.form("patient_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                age = st.number_input("Age", 1, 120, 25)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
            with col2:
                phone = st.text_input("Phone Number*")
                address = st.text_area("Address")
            
            submitted = st.form_submit_button("Register Patient")
            if submitted:
                if name and phone:
                    new_patient = pd.DataFrame([{
                        'Patient_ID': f"P{str(uuid.uuid4())[:6]}".upper(),
                        'Name': name,
                        'Age': age,
                        'Gender': gender,
                        'Phone': phone,
                        'Address': address,
                        'Blood_Group': blood_group,
                        'Registration_Date': date.today().strftime("%Y-%m-%d")
                    }])
                    st.session_state.patients = pd.concat([st.session_state.patients, new_patient], ignore_index=True)
                    st.success(f"Patient {name} registered successfully! ✅")
                else:
                    st.error("Name and Phone are required!")
    
    with tab2:
        if not st.session_state.patients.empty:
            st.dataframe(st.session_state.patients, use_container_width=True)
        else:
            st.warning("No patients found.")

# ====================== DOCTORS ======================
elif menu == "👨‍⚕️ Doctors":
    st.subheader("👨‍⚕️ Doctor Management")
    
    tab1, tab2 = st.tabs(["Add New Doctor", "View All Doctors"])
    
    with tab1:
        with st.form("doctor_form"):
            col1, col2 = st.columns(2)
            with col1:
                d_name = st.text_input("Doctor Name*")
                specialization = st.selectbox("Specialization", [
                    "Cardiologist", "Neurologist", "Orthopedic", "Pediatrician",
                    "General Physician", "Surgeon", "Gynecologist", "ENT"
                ])
                experience = st.number_input("Experience (Years)", 0, 50, 5)
            
            with col2:
                d_phone = st.text_input("Phone Number*")
                availability = st.selectbox("Availability", ["Available", "On Leave", "Busy"])
            
            if st.form_submit_button("Add Doctor"):
                if d_name and d_phone:
                    new_doctor = pd.DataFrame([{
                        'Doctor_ID': f"D{str(uuid.uuid4())[:6]}".upper(),
                        'Name': d_name,
                        'Specialization': specialization,
                        'Phone': d_phone,
                        'Experience': experience,
                        'Availability': availability
                    }])
                    st.session_state.doctors = pd.concat([st.session_state.doctors, new_doctor], ignore_index=True)
                    st.success("Doctor added successfully! ✅")
    
    with tab2:
        if not st.session_state.doctors.empty:
            st.dataframe(st.session_state.doctors, use_container_width=True)
        else:
            st.info("No doctors added yet.")

# ====================== APPOINTMENTS ======================
elif menu == "📅 Appointments":
    st.subheader("📅 Appointment Booking")
    
    if st.session_state.patients.empty or st.session_state.doctors.empty:
        st.warning("Please add patients and doctors first.")
    else:
        with st.form("appointment_form"):
            col1, col2 = st.columns(2)
            with col1:
                patient_list = st.session_state.patients['Name'].tolist()
                patient_name = st.selectbox("Select Patient", patient_list)
                
                doctor_list = st.session_state.doctors['Name'].tolist()
                doctor_name = st.selectbox("Select Doctor", doctor_list)
            
            with col2:
                app_date = st.date_input("Appointment Date", date.today())
                app_time = st.time_input("Appointment Time")
            
            if st.form_submit_button("Book Appointment"):
                new_appointment = pd.DataFrame([{
                    'Appointment_ID': f"A{str(uuid.uuid4())[:6]}".upper(),
                    'Patient_Name': patient_name,
                    'Doctor_Name': doctor_name,
                    'Date': app_date.strftime("%Y-%m-%d"),
                    'Time': str(app_time)[:5],
                    'Status': "Confirmed"
                }])
                st.session_state.appointments = pd.concat([st.session_state.appointments, new_appointment], ignore_index=True)
                st.success("Appointment booked successfully! ✅")

    st.subheader("All Appointments")
    if not st.session_state.appointments.empty:
        st.dataframe(st.session_state.appointments, use_container_width=True)
    else:
        st.info("No appointments yet.")

# ====================== REPORTS ======================
elif menu == "📊 Reports":
    st.subheader("📊 Hospital Reports")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Registered Patients", len(st.session_state.patients))
        st.metric("Total Doctors", len(st.session_state.doctors))
    
    with col2:
        st.metric("Total Appointments", len(st.session_state.appointments))
        if not st.session_state.appointments.empty:
            today_apps = len(st.session_state.appointments[st.session_state.appointments['Date'] == str(date.today())])
            st.metric("Today's Appointments", today_apps)

    st.subheader("Patient Distribution by Gender")
    if not st.session_state.patients.empty:
        gender_count = st.session_state.patients['Gender'].value_counts()
        st.bar_chart(gender_count)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("MediCare HMS v1.0\nMade with Streamlit")



