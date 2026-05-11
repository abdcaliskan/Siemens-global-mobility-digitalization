# 🌍 End-to-End Digitalization of Global Mobility & H2R Processes

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458.svg)
![Power BI](https://img.shields.io/badge/Power_BI-Analytics-F2C811.svg)

## 📌 Project Overview
This project serves as a proof-of-concept (PoC) for digitalizing and automating **Global Mobility and Hire-to-Retire (H2R)** processes within a Global Business Services (GBS) environment. It demonstrates how to transition from a manual, error-prone spreadsheet-based workflow to an automated, structured, and visually interactive data pipeline.

---

## 🎯 Business Problem (As-Is)
* **Manual Entry:** HR professionals rely on unstructured emails and manual Excel data entry.
* **Data Quality Issues:** High risk of human error at the source (e.g., negative salaries, inverted assignment dates).
* **Time-Consuming:** Manual calculation of assignment durations and consolidation of global costs.
* **Lack of Visibility:** Static reporting makes it difficult for decision-makers to track global assignment budgets and equity programs in real-time.

---

## 🚀 The Solution (To-Be Workflow)
This project introduces a **3-tier closed-loop architecture** to solve these operational inefficiencies:

1. **Data Input (Frontend UI):** A **Streamlit** web application replaces manual Excel entry. It features *Smart Validation* (e.g., >€150k budget alerts) to ensure compliance before data is even recorded.
2. **Process Automation & Quality Control (Backend ETL):** A Python script (`pandas`) extracts the raw data, validates quality, calculates exact assignment durations, and categorizes them. Crucially, it isolates erroneous entries into an **Exception Handling Loop** for HR review rather than failing the pipeline.
3. **Business Intelligence (Analytics):** A **Power BI** dashboard connected to the cleaned data provides real-time geographic distribution, operating company cost breakdowns, and a dynamic DAX-powered `"What-If"` parameter to simulate future budget increases.

### 🔄 System Architecture & Data Pipeline
```mermaid
graph TD
    %% AŞAMA 1: DATA ENTRY (FRONTEND)
    User((HR Admin)) -->|Inputs/Corrects Data| UI[Streamlit Web Portal: Form Validation]
    
    %% AŞAMA 2: RAW STORAGE
    UI -->|Appends Record| MasterDB[(Master Database: Raw Data)]
    
    %% AŞAMA 3: ETL PIPELINE (BACKEND)
    MasterDB -->|Extract| ETL{Python ETL Pipeline: Quality Check}
    
    %% AŞAMA 4: ROUTING & CLEAN STORAGE
    ETL -->|If Fails Quality| ErrorDB[(Error Logs: Review Needed)]
    ETL -->|If Passes & Cleaned| CleanDB[(Cleaned DB: Analytics Ready)]

    %% AŞAMA 4.5: EXCEPTION HANDLING LOOP
    ErrorDB -.->|Reviews & Fixes Data| User

    %% AŞAMA 5: ANALYTICS (POWER BI)
    CleanDB -->|Direct Query| PBI[Power BI Gateway: Data Modeling]
    PBI -->|Interactive Visuals| Dash((Executive Dashboard: What-If Scenarios))

    %% Renk ve Stil Atamaları
    classDef frontend fill:#009999,stroke:#fff,stroke-width:2px,color:#fff;
    classDef database fill:#1F2937,stroke:#009999,stroke-width:2px,color:#fff;
    classDef backend fill:#D97706,stroke:#fff,stroke-width:2px,color:#fff;
    classDef powerbi fill:#F59E0B,stroke:#fff,stroke-width:2px,color:#fff;
    classDef errorloop fill:#B91C1C,stroke:#fff,stroke-width:2px,color:#fff;

    class UI frontend;
    class MasterDB,CleanDB database;
    class ErrorDB errorloop;
    class ETL backend;
    class PBI,Dash powerbi;