-- Medical Database Setup
-- Create database and tables for medical imaging system

-- Drop existing database if exists
DROP DATABASE IF EXISTS medical_db;

-- Create new database
CREATE DATABASE medical_db;

-- Connect to medical_db database
\c medical_db;

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create studies table
CREATE TABLE IF NOT EXISTS studies (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    doctor_id INTEGER REFERENCES doctors(id),
    study_type VARCHAR(50),
    study_date DATE,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create images table
CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    study_id INTEGER REFERENCES studies(id),
    image_type VARCHAR(50),
    file_path TEXT,
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, phone, address, city, state, zip_code) VALUES
('Jane', 'Smith', '1990-05-15', 'F', 'jane.smith@example.com', '555-0101', '456 Oak Ave', 'Springfield', 'IL', '62701'),
('John', 'Doe', '1985-03-20', 'M', 'john.doe@example.com', '555-0102', '123 Main St', 'Anytown', 'CA', '12345'),
('Alice', 'Johnson', '1988-08-12', 'F', 'alice.johnson@example.com', '555-0103', '789 Pine St', 'Riverside', 'CA', '92501');

INSERT INTO doctors (full_name, specialization, phone, email) VALUES
('Dr. John Wilson', 'Radiology', '555-0201', 'john.wilson@medical.com'),
('Dr. Sarah Johnson', 'Cardiology', '555-0202', 'sarah.johnson@medical.com'),
('Dr. Michael Brown', 'Neurology', '555-0203', 'michael.brown@medical.com'),
('Dr. Emily Davis', 'Orthopedics', '555-0204', 'emily.davis@medical.com'),
('Dr. Robert Miller', 'Pediatrics', '555-0205', 'robert.miller@medical.com');

INSERT INTO studies (patient_id, doctor_id, study_type, study_date, description, status) VALUES
(1, 1, 'CT', '2024-01-15', 'Chest CT scan', 'completed'),
(2, 2, 'MRI', '2024-01-20', 'Brain MRI', 'completed'),
(3, 3, 'X-Ray', '2024-01-25', 'Chest X-ray', 'completed'),
(1, 4, 'Ultrasound', '2024-02-01', 'Abdominal ultrasound', 'in_progress'),
(2, 5, 'CT', '2024-02-05', 'Sinus CT scan', 'pending');

-- Grant permissions to postgres user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Show setup completion
SELECT 'Medical database setup completed' as status,
       'medical_db' as database_name,
       (SELECT COUNT(*) FROM patients) as patient_count,
       (SELECT COUNT(*) FROM doctors) as doctor_count,
       (SELECT COUNT(*) FROM studies) as study_count;
