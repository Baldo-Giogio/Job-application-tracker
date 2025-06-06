import streamlit as st
import sqlite3
from datetime import date

def init_db():
    conn = sqlite3.connect("Job_apps.db")
    cur = conn.cursor()
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,                           
            role TEXT,
            status TEXT,
            date_applied DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()      

    return conn

def add_application(conn, company, role, status, date_applied):
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO applications (company, role, status, date_applied)
                VALUES(?,?,?,?)
                """, (company, role, status, date_applied) 
    )

    conn.commit()

def get_applications(conn, st_filter = None, search_word = None):
    cur = conn.cursor()
    query = "SELECT * FROM applications WHERE 1=1"
    params = []

    if st_filter and st_filter != "All":
        query+= " AND status = ?"
        params.append(status_filter)

    if search_word:
        query+= """
                AND (
                company LIKE ? OR
                role LIKE ? OR
                notes LIKE ?
                )"""
        search_word_param = f"%{search_word}%"
        params.extend([search_word_param] * 3)
    
    query+= " ORDER BY date_applied ASC"
    cur.execute(query, params)
    return cur.fetchall()

def remove_application(conn, id):
    cur = conn.cursor()
    cur.execute("DELETE FROM applications WHERE id = ?", (id,))
    conn.commit()

def edit_application(conn, company, role, status, date_applied):
    cur = conn.cursor()
    cur.execute("UPDATE applications SET company = ?, role = ?, status = ?, date_applied = ?", (company, role, status, date_applied))
    conn.commit()
        

st.set_page_config(page_title="Job Application Tracker", layout="centered")
st.title("📋 Job Application Tracker")

conn = init_db()

# Sidebar form for input
with st.sidebar.form("new_app_form"):
    st.subheader("➕ Add New Application")
    company = st.text_input("Company")
    role = st.text_input("Role")
    date_applied = st.date_input("Date Applied", value=date.today())
    status = st.selectbox("Status", ["Applied", "Interviewing", "Offer", "Rejected"])
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Submit")

    if submitted and company and role:
        add_application(conn, company, role, date_applied.isoformat(), status)
        st.success(f"Added application for **{role} at {company}**")

# Filter section
st.subheader("📄 View Applications")
col1, col2 = st.columns([2, 3])
with col1:
    status_filter = st.selectbox("Filter by Status", 
                                 options = ["All", "Applied", "Interviewing", "Offer", "Rejected"],
                                 index = 0,
                                 key = "status_filter"
                                )
with col2:
    search = st.text_input("Search (company, role)", value="")

apps = get_applications(conn, status_filter, search)

if apps:
    for app in apps:
        with st.expander(f"{app[1]} – {app[2]}", expanded=False):
            st.markdown(f"- **Status:** {app[3]}")
            st.markdown(f"- **Date:** {app[4]}")
            st.caption(f"📅 Created: {app[5]}")

            if f"edit_mode_{app[0]}"not in st.session_state:
                st.session_state[f"edit_mode_{app[0]}"] = False

            col3,col4 = st.columns([1, 1])
            with col3:
                if st.button(f"Edit", key = f"edit_{app[0]}"):
                    st.session_state[f"edit_mode_{app[0]}"] =True
            with col4:
                if st.button(f"Delete", key = f"del_{app[0]}"):
                    remove_application(conn, app[0])
                    st.success("Application Deleted")

            if st.session_state[f"edit_mode_{app[0]}"]:
                st.markdown("**Edit Application**")
                with st.form(f"edit_form_{app[0]}"):
                    new_company = st.text_input("Company", app[1])
                    new_role = st.text_input("Role", app[2])
                    new_status = st.selectbox("Status", ["Applied", "Interviewing", "Offer", "Rejected"], index=["Applied", "Interviewing", "Offer", "Rejected"].index(app[3]))
                    new_date = st.date_input("Date Applied", value=date.fromisoformat(app[4]))
                    submitted = st.form_submit_button("Update")

                    if submitted:
                        edit_application(conn, new_company, new_role, new_date.isoformat(), new_status)
                        st.success("Application updated.")
                        st.session_state[f"edit_mode_{app[0]}"] = False              
else:
    st.info("No applications found.")

# Stats
st.subheader("📊 Summary")
st.write(f"Total applications: **{len(apps)}**")