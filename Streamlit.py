import streamlit as st
import pandas as pd
import os
from datetime import date, datetime

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Siemens H2R Portal", page_icon="⚡", layout="wide")

# ==========================================
# SESSION STATE
# ==========================================
for key, val in {
    "requirements": [],
    "processes": {
        "H2R-GM-01": {
            "title": "Global Mobility Intake",
            "owner": "GM Team", "version": "2.1", "status": "Active",
            "steps": ["Employee request received", "Manager approval", "HR review",
                      "Visa processing", "Relocation support", "Assignment start"]
        },
        "H2R-COMP-04": {
            "title": "Share Program Allocation",
            "owner": "Equity Team", "version": "1.3", "status": "Active",
            "steps": ["Eligibility check", "Grant calculation", "Board approval",
                      "System entry", "Employee notification", "Vesting tracking"]
        },
        "H2R-DATA-02": {
            "title": "ETL Data Pipeline",
            "owner": "Data Team", "version": "3.0", "status": "Active",
            "steps": ["Data extraction", "Validation", "Transformation",
                      "Quality check", "Load to warehouse", "Report generation"]
        },
    }
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ==========================================
# THEME VARIABLES (Dark Mode — permanent)
# ==========================================
bg           = "#1F2937"
sidebar_bg   = "#111827"
text_color   = "#F3F4F6"
card_bg      = "#374151"
input_bg     = "#2D3748"
input_border = "#4B5563"
input_text   = "#F3F4F6"
label_color  = "#D1D5DB"
border_color = "#4B5563"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * {{ font-family: 'Inter', sans-serif !important; }}

    /* ── Backgrounds ── */
    [data-testid="stAppViewContainer"], .main {{ background-color: {bg} !important; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {border_color}; }}

    /* ── Global text ── */
    body, p, div, span, h1, h2, h3, h4, h5, h6,
    [data-testid="stMarkdownContainer"] p {{ color: {text_color} !important; }}
    label, .stSelectbox label, .stTextInput label,
    .stNumberInput label, .stDateInput label,
    .stTextArea label, [data-testid="stWidgetLabel"] {{
        color: {label_color} !important; font-weight: 500 !important;
    }}

    /* ── Text inputs ── */
    input[type="text"], input[type="number"], input[type="date"],
    textarea, .stTextInput input, .stNumberInput input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: #6B7280 !important;
    }}

    /* ── Selectbox ── */
    div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 8px !important;
        color: {input_text} !important;
    }}
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {{ color: {input_text} !important; }}
    [role="listbox"] {{
        background-color: {input_bg} !important;
        border: 1px solid {input_border} !important;
    }}
    [role="option"] {{ color: {input_text} !important; }}
    [role="option"]:hover {{ background-color: #374151 !important; }}

    /* ── Date input ── */
    [data-testid="stDateInput"] input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 8px !important;
    }}

    /* ── Number input ── */
    [data-testid="stNumberInput"] input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stNumberInput"] button {{
        background-color: {input_bg} !important;
        border: 1px solid {input_border} !important;
        color: {input_text} !important;
    }}

    /* ── Text area ── */
    textarea {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 8px !important;
    }}

    /* ── Form container ── */
    div[data-testid="stForm"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 14px !important;
        padding: 24px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.25) !important;
    }}

    /* ── Metric cards ── */
    div[data-testid="metric-container"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-left: 4px solid #009999 !important;
        border-radius: 10px !important;
        padding: 14px !important;
    }}

    /* ── Buttons ── */
    div.stButton > button {{
        width: 100% !important;
        background: linear-gradient(135deg, #009999, #00BEDC) !important;
        color: white !important; border-radius: 8px !important;
        padding: 10px !important; font-weight: 600 !important;
        border: none !important; transition: all 0.3s !important;
        box-shadow: 0 4px 12px rgba(0,153,153,0.25) !important;
    }}
    div.stButton > button:hover {{ transform: scale(1.02) !important; opacity: 0.92 !important; }}
    div.stButton > button span {{ color: white !important; font-weight: 600 !important; }}

    /* ── Radio (sidebar nav) ── */
    div[data-testid="stRadio"] label {{ color: {label_color} !important; }}

    /* ── Requirement cards ── */
    .req-card {{
        background: {card_bg};
        border-radius: 10px; padding: 14px 18px; margin: 8px 0;
        border-left: 4px solid #009999;
        border: 1px solid {border_color};
        border-left: 4px solid #009999;
    }}

    /* ── Process step boxes ── */
    .step-box {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px; padding: 10px 16px; margin: 5px 0;
        display: flex; align-items: center; gap: 12px;
    }}

    /* ── Divider ── */
    hr {{ border-color: {border_color} !important; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    try:
        st.image(r"C:\Users\abdul\OneDrive\Desktop\Siemens\siemens_logo.png", width=160)
    except Exception:
        st.markdown("## ⚡ Siemens")

    st.markdown(f"<h3 style='color:{text_color}'>Navigation</h3>", unsafe_allow_html=True)


    active_module = st.radio("Module", [
        "📝 Assignment Intake",
        "📊 Expatriate Database",
        "🔧 Requirements Tracker",
        "📄 ISO Documentation",
    ])
    st.markdown("---")
    st.caption("👤 **H2R Process Admin**")
    st.caption("🌍 Production | Erlangen HQ")

file_path = r"C:\Users\abdul\OneDrive\Desktop\Siemens\Global_Mobility_Data.xlsx"

# ==========================================
# MODULE 1: ASSIGNMENT INTAKE
# ==========================================
if active_module == "📝 Assignment Intake":
    st.title("🌍 Global Mobility Intake")
    st.markdown("*Submit and register new international assignment requests, including employee details, visa status, compensation, and equity data.*")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Assignments", "142", "+3")
    c2.metric("Budget YTD", "€1.2M", "-5%")
    c3.metric("Pending Visas", "8", "-2")
    c4.metric("Visa Success", "97%", "↑")
    st.markdown("---")

    v1, v2, v3 = st.columns(3)
    v1.success("✅ Visa Approved: 134")
    v2.warning("⏳ Visa Processing: 6")
    v3.error("❌ Visa Rejected: 2")
    st.markdown("---")

    with st.form("intake_form"):
        st.markdown("#### 👤 1. Employee Information")
        a1, a2, a3 = st.columns(3)
        emp_id     = a1.text_input("SAP ID", placeholder="e.g. 9012345")
        department = a2.selectbox("Company Division", [
            "Digital Industries", "Smart Infrastructure", "Mobility", "Healthineers"
        ])
        cost_center = a3.text_input("Cost Center", placeholder="e.g. CC-4421")

        st.markdown("---")
        st.markdown("#### ✈️ 2. Assignment Details")
        b1, b2, b3 = st.columns(3)
        country    = b1.selectbox("Destination Country", [
            "Germany", "USA", "UK", "China", "India", "Brazil", "Singapore", "France", "Netherlands"
        ])
        start_date = b2.date_input("Start Date", date.today())
        end_date   = b3.date_input("End Date")

        st.markdown("---")
        st.markdown("#### 💼 3. Assignment Type & Visa")
        e1, e2, e3 = st.columns(3)
        assignment_type = e1.selectbox("Assignment Type", [
            "Long-Term (>12 months)", "Short-Term (3–12 months)", "Commuter", "Business Trip"
        ])
        visa_type = e2.selectbox("Visa / Permit Type", [
            "Work Permit", "EU Blue Card", "Intracompany Transfer", "Business Visa", "Not Required"
        ])
        visa_status = e3.selectbox("Visa Status", [
            "✅ Approved", "⏳ In Processing", "📋 Not Started", "❌ Rejected"
        ])

        st.markdown("---")
        st.markdown("#### 💰 4. Compensation & Equity")
        d1, d2, d3 = st.columns(3)
        salary    = d1.number_input("Base Salary (EUR)", min_value=0, step=1000)
        relocation = d2.number_input("Relocation Allowance (EUR)", min_value=0, step=500)
        shares    = d3.number_input("Equity Shares (Units)", min_value=0, step=50)

        st.markdown("---")
        st.markdown("#### 📝 5. Notes")
        notes = st.text_area("Internal Notes / Remarks", placeholder="Any additional information for the HR team...", height=80)

        total = salary + relocation
        st.info(f"💡 **Estimated Total Cost:** € {total:,.0f}  |  **Equity Shares:** {shares} units  |  **Duration:** {(end_date - start_date).days} days")

        if total > 150000:
            st.warning("⚠️ Total cost exceeds €150,000 — will be flagged for senior approval.")

        submitted = st.form_submit_button("🚀 Submit to Database")

    if submitted:
        if not emp_id:
            st.error("❌ SAP ID is required.")
        elif end_date <= start_date:
            st.error("❌ End Date must be after Start Date.")
        else:
            new_row = pd.DataFrame({
                "Employee_ID":           [emp_id],
                "Department":            [department],
                "Cost_Center":           [cost_center],
                "Country":               [country],
                "Assignment_Type":       [assignment_type],
                "Visa_Type":             [visa_type],
                "Visa_Status":           [visa_status],
                "Start_Date":            [start_date],
                "End_Date":              [end_date],
                "Duration_Days":         [(end_date - start_date).days],
                "Salary_EUR":            [salary],
                "Relocation_EUR":        [relocation],
                "Total_Cost_EUR":        [total],
                "Equity_Shares":         [shares],
                "Notes":                 [notes],
                "Submitted_At":          [datetime.now().strftime("%Y-%m-%d %H:%M")],
                "Needs_Senior_Approval": [total > 150000],
            })
            try:
                if os.path.exists(file_path):
                    df_ex = pd.read_excel(file_path)
                    pd.concat([df_ex, new_row], ignore_index=True).to_excel(file_path, index=False)
                else:
                    new_row.to_excel(file_path, index=False)
                st.success(f"✅ Record for **{emp_id}** successfully saved to database!")
                st.balloons()
            except PermissionError:
                st.error("⚠️ File is open in Excel — please close it and try again.")

# ==========================================
# MODULE 2: EXPATRIATE DATABASE
# ==========================================
elif active_module == "📊 Expatriate Database":
    st.title("📊 Central Expatriate Database")
    st.markdown("*Browse, filter, and export all submitted expatriate assignment records stored in the master database.*")
    st.markdown("---")

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)

        f1, f2, f3 = st.columns(3)
        countries = ["All"] + sorted(df["Country"].dropna().unique().tolist()) if "Country" in df.columns else ["All"]
        depts     = ["All"] + sorted(df["Department"].dropna().unique().tolist()) if "Department" in df.columns else ["All"]
        sel_country = f1.selectbox("Filter: Country", countries)
        sel_dept    = f2.selectbox("Filter: Division", depts)
        search_id   = f3.text_input("Search SAP ID", placeholder="e.g. 9012345")

        filtered = df.copy()
        if sel_country != "All":
            filtered = filtered[filtered["Country"] == sel_country]
        if sel_dept != "All":
            filtered = filtered[filtered["Department"] == sel_dept]
        if search_id:
            filtered = filtered[filtered["Employee_ID"].astype(str).str.contains(search_id)]

        st.markdown(f"**{len(filtered)} record(s) found**")
        st.dataframe(filtered, use_container_width=True, height=420)

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Export CSV", data=csv, file_name="expatriate_export.csv", mime="text/csv")
    else:
        st.info("📭 No data yet. Submit an assignment in the Intake module first.")

# ==========================================
# MODULE 3: REQUIREMENTS TRACKER
# ==========================================
elif active_module == "🔧 Requirements Tracker":
    st.title("🔧 Digitalization Requirements Tracker")
    st.markdown("*Log, prioritize, and monitor technical and process requirements for ongoing digitalization initiatives within the H2R function.*")
    st.markdown("---")

    with st.expander("➕ Add New Requirement", expanded=True):
        with st.form("req_form"):
            r1, r2 = st.columns(2)
            req_id   = r1.text_input("Requirement ID", placeholder="e.g. REQ-2026-007")
            req_area = r2.selectbox("Business Area", [
                "Global Mobility", "Equity Programs", "Data Pipeline", "Reporting", "Compliance", "Visa Processing"
            ])
            req_title = st.text_input("Title", placeholder="Short, clear description")
            req_desc  = st.text_area("Detailed Description",
                                     placeholder="Describe the business need, expected outcome, and affected stakeholders...",
                                     height=100)
            r3, r4, r5 = st.columns(3)
            priority = r3.selectbox("Priority", ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"])
            status   = r4.selectbox("Status", [
                "📋 Backlog", "🔄 In Analysis", "✅ Approved", "🚧 In Development", "🎯 Done"
            ])
            owner    = r5.text_input("Owner / Team", placeholder="e.g. GM Process Team")

            add_req = st.form_submit_button("➕ Add Requirement")

        if add_req:
            if not req_title:
                st.error("❌ Title is required.")
            else:
                st.session_state.requirements.append({
                    "ID":          req_id,
                    "Area":        req_area,
                    "Title":       req_title,
                    "Description": req_desc,
                    "Priority":    priority,
                    "Status":      status,
                    "Owner":       owner,
                    "Created":     datetime.now().strftime("%Y-%m-%d"),
                })
                st.success(f"✅ Requirement **{req_id}** added!")

    st.markdown("---")

    total_reqs = len(st.session_state.requirements)
    if total_reqs > 0:
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total", total_reqs)
        s2.metric("In Development", sum(1 for r in st.session_state.requirements if "Development" in r["Status"]))
        s3.metric("Done", sum(1 for r in st.session_state.requirements if "Done" in r["Status"]))
        s4.metric("Critical", sum(1 for r in st.session_state.requirements if "Critical" in r["Priority"]))
        st.markdown("---")

    st.markdown(f"### 📋 Backlog ({total_reqs} items)")

    if st.session_state.requirements:
        filter_status = st.selectbox("Filter by Status", [
            "All", "📋 Backlog", "🔄 In Analysis", "✅ Approved", "🚧 In Development", "🎯 Done"
        ])
        reqs = st.session_state.requirements
        if filter_status != "All":
            reqs = [r for r in reqs if r["Status"] == filter_status]

        for req in reqs:
            st.markdown(f"""
            <div class="req-card">
                <strong style="font-size:1.05em">{req['ID']} — {req['Title']}</strong><br>
                <small>📁 {req['Area']} &nbsp;|&nbsp; {req['Priority']} &nbsp;|&nbsp; {req['Status']} &nbsp;|&nbsp; 👤 {req['Owner']} &nbsp;|&nbsp; 📅 {req['Created']}</small><br><br>
                <span style="font-size:0.9em; opacity:0.85;">{req['Description'][:200]}{'...' if len(req['Description']) > 200 else ''}</span>
            </div>
            """, unsafe_allow_html=True)

        req_df = pd.DataFrame(st.session_state.requirements)
        st.download_button("📥 Export Requirements CSV",
                           req_df.to_csv(index=False).encode(),
                           "requirements.csv", "text/csv")
    else:
        st.info("No requirements yet. Add your first one above.")

# ==========================================
# MODULE 4: ISO DOCUMENTATION
# ==========================================
elif active_module == "📄 ISO Documentation":
    st.title("📄 ISO 9001:2015 Process Documentation")
    st.markdown("*View, edit, and maintain ISO 9001:2015-compliant H2R process manuals, including step-by-step workflows and the official document library.*")
    st.markdown("---")
    st.success("✅ ISO 9001:2015 Compliant | Last Audit: Q4 2025 | Next Review: Q2 2026")
    st.markdown("---")

    proc_key = st.selectbox(
        "Select Process Manual",
        list(st.session_state.processes.keys()),
        format_func=lambda k: f"[{k}] {st.session_state.processes[k]['title']}"
    )
    proc = st.session_state.processes[proc_key]

    col_info, col_meta = st.columns([3, 1])
    with col_info:
        st.markdown(f"### [{proc_key}] {proc['title']}")
        st.markdown(f"**Process Owner:** {proc['owner']} &nbsp;|&nbsp; **Version:** v{proc['version']} &nbsp;|&nbsp; **Status:** {proc['status']}")

    with col_meta:
        new_status = st.selectbox("Update Status", ["Active", "Under Review", "Deprecated"],
                                  index=["Active", "Under Review", "Deprecated"].index(proc["status"]))
        if st.button("💾 Save Status"):
            st.session_state.processes[proc_key]["status"] = new_status
            st.success("Status updated!")
            st.rerun()

    st.markdown("---")
    st.markdown("#### 🔄 Process Flow")
    steps = proc["steps"]
    for i, step in enumerate(steps):
        is_last = i == len(steps) - 1
        st.markdown(f"""
        <div class="step-box">
            <span style="font-size:1.1em; font-weight:700; color:#009999; min-width:28px;">{i+1}</span>
            <span style="flex:1">{step}</span>
            <span>{"🏁" if is_last else "→"}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ✏️ Edit Process Steps")
    with st.form(f"edit_{proc_key}"):
        new_steps_raw = st.text_area("Steps (one per line)", value="\n".join(steps), height=180)
        if st.form_submit_button("💾 Update Process"):
            new_steps = [s.strip() for s in new_steps_raw.split("\n") if s.strip()]
            st.session_state.processes[proc_key]["steps"]   = new_steps
            st.session_state.processes[proc_key]["version"] = f"{float(proc['version']) + 0.1:.1f}"
            st.success(f"✅ Updated to v{st.session_state.processes[proc_key]['version']}")
            st.rerun()

    st.markdown("---")
    st.markdown("#### 📂 Document Library")
    manual_data = {
        "Document ID": ["H2R-GM-01", "H2R-COMP-04", "H2R-DATA-02", "H2R-VISA-03", "H2R-EQ-05"],
        "Title":       ["Global Mobility Intake", "Share Program Allocation Rules",
                        "Python ETL Pipeline Standards", "Visa Processing Workflow", "Equity Eligibility Framework"],
        "Version":     ["2.1", "1.3", "3.0", "1.8", "2.0"],
        "Status":      ["Active", "Active", "Active", "Active", "Under Review"],
        "Owner":       ["GM Team", "Equity Team", "Data Team", "Legal Team", "Compensation Team"],
        "Last Updated":["2025-11-01", "2025-09-15", "2025-12-03", "2025-10-22", "2026-01-10"],
    }
    st.dataframe(pd.DataFrame(manual_data), use_container_width=True)
    st.download_button("📥 Export Document Index",
                       pd.DataFrame(manual_data).to_csv(index=False).encode(),
                       "iso_docs.csv", "text/csv")