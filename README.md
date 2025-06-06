# 📋 Job Application Tracker

A simple, interactive job application tracker built using **Streamlit** and **SQLite**. This app helps you organize, filter, edit, and track your job applications all in one place with a clean UI.

---

## 🚀 Features

- Add new job applications with:
  - Company name
  - Role
  - Application date
  - Status
  - Notes
- View all applications in an expandable list
- Search by keyword (company or role)
- Filter by application status
- Edit or delete existing applications
- Summary statistics

---

## 🛠️ Technologies Used

- **Python 3.9+**
- **Streamlit** – for the interactive frontend
- **SQLite** – lightweight database storage
- **Datetime** – for date handling

---

## 📦 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/job-application-tracker.git
   cd job-application-tracker
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run athe app**
   ```bash
   streamlit run app.py
   ```

## 📁 File Structure
``` bash
├── job_application_tracker.py              # Main Streamlit app
├── Job_apps.db                             # SQLite database (auto-created)
├── requirements.txt                        # Python dependencies
├── README.md                               # This file
```

## 📌 Notes

- The SQLite database will be created automatically on the first run.
- You can clear all data by deleting the Jobs_apps.db file

## 🧪 Example Usage
-Add job applications with details
-Search for a role like "backend"
-Filter only "Interviewing" status
-Update status after receiving an offer

## Author
Baldo Giogio Otu-Quayson
