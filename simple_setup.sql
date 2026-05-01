-- Medical Imaging Database Setup
DROP DATABASE IF EXISTS medical_imaging;
CREATE DATABASE medical_imaging;
\c medical_imaging;

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

CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, phone, address, city, state, zip_code) VALUES
('Jane', 'Smith', '1990-05-15', 'F', 'jane.smith@example.com', '555-0101', '456 Oak Ave', 'Springfield', 'IL', '62701'),
('John', 'Doe', '1985-03-20', 'M', 'john.doe@example.com', '555-0102', '123 Main St', 'Anytown', 'CA', '12345');

INSERT INTO doctors (full_name, specialization, phone, email) VALUES
('Dr. John Wilson', 'Radiology', '555-0201', 'john.wilson@medical.com'),
('Dr. Sarah Johnson', 'Cardiology', '555-0202', 'sarah.johnson@medical.com');

INSERT INTO studies (patient_id, doctor_id, study_type, study_date, description, status) VALUES
(1, 1, 'CT', '2024-01-15', 'Chest CT scan', 'completed'),
(2, 2, 'MRI', '2024-01-20', 'Brain MRI', 'completed');

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
SELECT 'Database setup completed' as status;
