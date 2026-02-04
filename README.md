# Attendance Management System

This Flask app manages attendance while pulling course offerings and registrations from a separate course registration database.

## Features
- Load course list from the **course registration** database.
- Fetch enrolled students for the selected course.
- Record attendance into the **attendance** database.
- Optional sample data mode for local UI preview.

## Setup

### 1) Create databases and tables
Run the SQL file in MySQL:

```sql
SOURCE schema.sql;
```

### 2) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Configure environment variables

```bash
export REGISTRATION_DB_HOST=localhost
export REGISTRATION_DB_USER=root
export REGISTRATION_DB_PASSWORD=yourpassword
export REGISTRATION_DB_NAME=course_registration

export ATTENDANCE_DB_HOST=localhost
export ATTENDANCE_DB_USER=root
export ATTENDANCE_DB_PASSWORD=yourpassword
export ATTENDANCE_DB_NAME=attendance
```

### 4) Run the app

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

### Optional: sample data mode

If you want to preview the UI without connecting to MySQL, enable sample data mode:

```bash
export USE_SAMPLE_DATA=true
python app.py
```
