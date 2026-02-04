from datetime import date
import os

from flask import Flask, redirect, render_template, request, url_for

from db import get_attendance_connection, get_registration_connection

app = Flask(__name__)

SAMPLE_COURSES = [
    {"course_code": "CSC101", "course_title": "Intro to Programming"},
    {"course_code": "MAT210", "course_title": "Discrete Mathematics"},
]
SAMPLE_ROSTERS = {
    "CSC101": [
        {"student_id": "S1001", "full_name": "Ada Lovelace"},
        {"student_id": "S1002", "full_name": "Alan Turing"},
    ],
    "MAT210": [
        {"student_id": "S2001", "full_name": "Katherine Johnson"},
        {"student_id": "S2002", "full_name": "George Boole"},
    ],
}


def _using_sample_data() -> bool:
    return os.environ.get("USE_SAMPLE_DATA", "").lower() == "true"


@app.route("/")
def index():
    if _using_sample_data():
        return render_template("index.html", courses=SAMPLE_COURSES)

    registration_conn = get_registration_connection()
    cursor = registration_conn.cursor(dictionary=True)
    cursor.execute("SELECT course_code, course_title FROM courses ORDER BY course_code")
    courses = cursor.fetchall()
    cursor.close()
    registration_conn.close()
    return render_template("index.html", courses=courses)


@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    course_code = request.values.get("course_code", "").strip().upper()
    if not course_code:
        return redirect(url_for("index"))

    if _using_sample_data():
        if request.method == "POST":
            return redirect(url_for("attendance", course_code=course_code))
        students = SAMPLE_ROSTERS.get(course_code, [])
        return render_template("attendance.html", course_code=course_code, students=students)

    if request.method == "POST" and "student_ids" in request.form:
        present_students = request.form.getlist("student_ids")
        attendance_conn = get_attendance_connection()
        cursor = attendance_conn.cursor()
        for student_id in present_students:
            cursor.execute(
                """
                INSERT INTO attendance_records (student_id, course_code, attendance_date, status)
                VALUES (%s, %s, %s, %s)
                """,
                (student_id, course_code, date.today(), "present"),
            )
        attendance_conn.commit()
        cursor.close()
        attendance_conn.close()
        return redirect(url_for("attendance", course_code=course_code))

    registration_conn = get_registration_connection()
    reg_cursor = registration_conn.cursor(dictionary=True)
    reg_cursor.execute(
        """
        SELECT student_id
        FROM course_registrations
        WHERE course_code = %s
        ORDER BY student_id
        """,
        (course_code,),
    )
    student_ids = [row["student_id"] for row in reg_cursor.fetchall()]
    reg_cursor.close()
    registration_conn.close()

    students = []
    if student_ids:
        attendance_conn = get_attendance_connection()
        attendance_cursor = attendance_conn.cursor(dictionary=True)
        placeholders = ", ".join(["%s"] * len(student_ids))
        attendance_cursor.execute(
            f"SELECT student_id, full_name FROM students WHERE student_id IN ({placeholders})",
            tuple(student_ids),
        )
        students = attendance_cursor.fetchall()
        attendance_cursor.close()
        attendance_conn.close()

    return render_template("attendance.html", course_code=course_code, students=students)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
