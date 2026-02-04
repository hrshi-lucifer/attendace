CREATE DATABASE IF NOT EXISTS course_registration;
CREATE DATABASE IF NOT EXISTS attendance;

USE course_registration;

CREATE TABLE IF NOT EXISTS courses (
  course_code VARCHAR(10) PRIMARY KEY,
  course_title VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS course_registrations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL,
  course_code VARCHAR(10) NOT NULL,
  CONSTRAINT fk_course_registrations_course
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
);

USE attendance;

CREATE TABLE IF NOT EXISTS students (
  student_id VARCHAR(20) PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL,
  course_code VARCHAR(10) NOT NULL,
  attendance_date DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  CONSTRAINT fk_attendance_student
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
