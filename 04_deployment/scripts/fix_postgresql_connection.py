#!/usr/bin/env python3
"""
PostgreSQL Database Connection Fix
Create medical database and tables
"""

import psycopg2
import sys
from psycopg2 import sql

def create_medical_db():
    """Create medical_db database if it doesn't exist"""
    try:
        # Connect to PostgreSQL default database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create medical_db if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'medical_db'")
        if not cursor.fetchone():
            cursor.execute(sql.SQL("CREATE DATABASE medical_db"))
            print("Created medical_db database")
        else:
            print("medical_db database already exists")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating medical_db: {e}")
        return False

def create_tables():
    """Create necessary tables in medical_db"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            database="medical_db"
        )
        cursor = conn.cursor()
        
        # Create doctors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                specialization VARCHAR(255),
                phone VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create patients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(50),
                date_of_birth DATE,
                gender VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create studies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS studies (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES patients(id),
                doctor_id INTEGER REFERENCES doctors(id),
                study_type VARCHAR(255),
                description TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create images table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                study_id INTEGER REFERENCES studies(id),
                image_type VARCHAR(255),
                image_url VARCHAR(500),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("Created/verified database tables")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            database="medical_db"
        )
        cursor = conn.cursor()
        
        # Insert sample doctors
        doctors_data = [
            ("Dr. John Smith", "john.smith@medical.com", "Cardiology", "555-0101"),
            ("Dr. Sarah Johnson", "sarah.johnson@medical.com", "Radiology", "555-0102"),
            ("Dr. Michael Brown", "michael.brown@medical.com", "Neurology", "555-0103")
        ]
        
        for doctor in doctors_data:
            cursor.execute("""
                INSERT INTO doctors (name, email, specialization, phone)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, doctor)
        
        # Insert sample patients
        patients_data = [
            ("Alice Wilson", "alice.wilson@email.com", "555-0201", "1985-03-15", "Female"),
            ("Bob Davis", "bob.davis@email.com", "555-0202", "1990-07-22", "Male"),
            ("Carol Martinez", "carol.martinez@email.com", "555-0203", "1978-11-30", "Female")
        ]
        
        for patient in patients_data:
            cursor.execute("""
                INSERT INTO patients (name, email, phone, date_of_birth, gender)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, patient)
        
        conn.commit()
        conn.close()
        print("Inserted sample data")
        return True
        
    except Exception as e:
        print(f"Error inserting sample data: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL Database Setup")
    print("=" * 40)
    
    if create_medical_db():
        if create_tables():
            if insert_sample_data():
                print("\nPostgreSQL setup completed successfully")
            else:
                print("\nDatabase created but sample data insertion failed")
        else:
            print("\nDatabase created but table creation failed")
    else:
        print("\nDatabase creation failed")