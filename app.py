import streamlit as st
import pandas as pd
import os

# Uygulama Başlığı
st.set_page_config(page_title="H2R Process Portal", page_icon="🌍")
st.title("🌍 Global Mobility - New Assignment Form")
st.write("Please fill out the details below to initiate a new global assignment. Data is saved directly to the central database.")

# Veri Giriş Formu
with st.form("assignment_form"):
    col1, col2 = st.columns(2)
    with col1:
        emp_id = st.text_input("Employee ID (e.g., EMP011)")
        country = st.selectbox("Destination Country", ["Germany", "USA", "UK", "China", "India", "France", "Brazil"])
        start_date = st.date_input("Start Date")
    with col2:
        assign_type = st.selectbox("Assignment Type", ["Short-Term", "Long-Term", "Commuter"])
        salary = st.number_input("Base Salary (EUR)", min_value=0, step=1000)
        bonus = st.number_input("Expected Bonus (EUR)", min_value=0, step=500)
        end_date = st.date_input("End Date")

    submitted = st.form_submit_button("Submit Assignment Request")

# Kaydetme Mantığı
if submitted:
    new_data = pd.DataFrame({
        "Employee_ID": [emp_id], "Country": [country], "Assignment_Type": [assign_type],
        "Salary_EUR": [salary], "Bonus_EUR": [bonus], 
        "Start_Date": [start_date], "End_Date": [end_date], "Status": ["Active"]
    })
    
    file_path = r"C:\Users\abdul\OneDrive\Desktop\Global_Mobility_Data.csv"
    
    # Dosya varsa üstüne ekle, yoksa yeni oluştur
    if os.path.exists(file_path):
        new_data.to_csv(file_path, mode='a', header=False, index=False)
    else:
        new_data.to_csv(file_path, index=False)
        
    st.success(f"✅ Success! Assignment for {emp_id} has been securely saved.")