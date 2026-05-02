import pandas as pd
from datetime import datetime

# 1. Veriyi Oku (Streamlit'in ürettiği veya senin elindeki CSV'yi okuyalım)
df = pd.read_csv(r"C:\Users\abdul\OneDrive\Desktop\Global_Mobility_Data.csv")

# 2. Tarihleri formata çevir
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df['End_Date'] = pd.to_datetime(df['End_Date'])

# 3. YENİ: VERİ KALİTESİ KONTROLÜ (Data Quality Check)
# Hata Kuralları: Bitiş tarihi başlangıçtan önce olamaz VEYA Maaş 0 olamaz.
error_condition = (df['End_Date'] <= df['Start_Date']) | (df['Salary_EUR'] <= 0)

# Veriyi ikiye ayır (Temizler ve Hatalılar)
df_errors = df[error_condition].copy()
df_clean = df[~error_condition].copy()

# 4. Sadece TEMİZ veri üzerinde hesaplamalar yap
df_clean['Duration_Months'] = ((df_clean['End_Date'] - df_clean['Start_Date']).dt.days / 30).round()
df_clean['Calculated_Category'] = df_clean['Duration_Months'].apply(lambda x: 'Long-Term' if x > 12 else 'Short-Term')
df_clean['Total_Cost_EUR'] = df_clean['Salary_EUR'] + df_clean['Bonus_EUR']

# 5. Dosyaları Dışa Aktar (İki farklı dosya)
df_clean.to_excel(r"C:\Users\abdul\OneDrive\Desktop\Cleaned_Mobility_Data.xlsx", index=False)

if not df_errors.empty:
    df_errors.to_excel(r"C:\Users\abdul\OneDrive\Desktop\Review_Needed_Errors.xlsx", index=False)
    print(f"⚠️ Warning: Found {len(df_errors)} erroneous records. Exported to Review_Needed_Errors.xlsx")

print("✅ Pipeline executed: Data processed, verified, and exported successfully!")