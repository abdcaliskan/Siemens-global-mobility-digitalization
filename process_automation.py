import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. DEFINE PIPELINE PATHS
# ==========================================
# Dosya yollarını Siemens klasörüne sabitledik (Streamlit ile aynı yer)
input_file = r"C:\Users\abdul\OneDrive\Desktop\Siemens\Global_Mobility_Data.xlsx"
clean_output = r"C:\Users\abdul\OneDrive\Desktop\Siemens\Cleaned_Mobility_Data.xlsx"
error_output = r"C:\Users\abdul\OneDrive\Desktop\Siemens\Review_Needed_Errors.xlsx"

print("[INFO] Initiating H2R Data Pipeline...")

# ==========================================
# 2. EXTRACT: READ MASTER DATABASE
# ==========================================
if not os.path.exists(input_file):
    print("[ERROR] Master database not found. Please submit data via the portal first.")
    exit()

# Streamlit artık Excel (.xlsx) ürettiği için read_excel kullanıyoruz
df = pd.read_excel(input_file)

# ==========================================
# 3. TRANSFORM: DATA TYPE CONVERSIONS
# ==========================================
# Gerçek Excel kolon isimleriyle hizalandı
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df['End_Date'] = pd.to_datetime(df['End_Date'])

# ==========================================
# 4. DATA QUALITY GATE (Validation Rules)
# ==========================================
# Kural 1: Bitiş tarihi başlangıçtan önce/aynı olamaz
# Kural 2: Maaş 0 veya daha küçük olamaz
error_condition = (df['End_Date'] <= df['Start_Date']) | (df['Salary_EUR'] <= 0)

# Veriyi ikiye ayır (Temizler ve Hatalılar)
df_errors = df[error_condition].copy()
df_clean = df[~error_condition].copy()

# ==========================================
# 5. DATA ENRICHMENT (For Power BI)
# ==========================================
if not df_clean.empty:
    # Görev süresini (Ay) hesapla
    df_clean['Duration_Months'] = ((df_clean['End_Date'] - df_clean['Start_Date']).dt.days / 30).round(1)
    
    # 12 aydan uzunsa Long-Term, kısaysa Short-Term etiketini otomatik yapıştır
    df_clean['Calculated_Type'] = df_clean['Duration_Months'].apply(lambda x: 'Long-Term' if x > 12 else 'Short-Term')
    
    # Relocation_Allowance_EUR NaN olabilir, 0 ile doldur
    df_clean['Relocation_Allowance_EUR'] = df_clean['Relocation_Allowance_EUR'].fillna(0)
    df_clean['Total_Cost_EUR'] = df_clean['Salary_EUR'] + df_clean['Relocation_Allowance_EUR']

# ==========================================
# 6. LOAD: EXPORT PIPELINE
# ==========================================
# Temizlenmiş ve zenginleştirilmiş veriyi Power BI için dışa aktar
df_clean.to_excel(clean_output, index=False)

# Hatalı kayıtlar varsa İK onayı için ayrı bir dosyaya çıkar
if not df_errors.empty:
    df_errors.to_excel(error_output, index=False)
    print(f"[WARNING] Data Quality Alert: {len(df_errors)} erroneous records flagged. Sent to Review_Needed_Errors.xlsx")

print(f"[SUCCESS] ETL Pipeline executed: {len(df_clean)} records cleaned, enriched, and exported to Power BI Gateway.")