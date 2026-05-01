#!/usr/bin/env python3
"""
Database Bridge for PostgreSQL 18
Handles database queries from Node.js backend
"""

import sys
import json
import psycopg2
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No SQL query provided"}))
        return
    
    sql_query = sys.argv[1]
    params = []
    
    if len(sys.argv) > 2:
        try:
            params = json.loads(sys.argv[2])
        except:
            params = []
    
    # Database configuration
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'medical_imaging',
        'user': 'postgres',
        'password': 'Sibo25Mana'
    }
    
    try:
        # Connect to PostgreSQL 18
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Execute query
        cursor.execute(sql_query, params)
        
        # Handle different query types
        if sql_query.strip().upper().startswith('SELECT'):
            # For SELECT queries, return rows
            rows = cursor.fetchall()
            
            # Get column names
            column_names = [desc[0] for desc in cursor.description]
            
            # Convert rows to dictionaries
            result_rows = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    # Handle datetime objects
                    if isinstance(value, datetime):
                        row_dict[column_names[i]] = value.isoformat()
                    else:
                        row_dict[column_names[i]] = value
                result_rows.append(row_dict)
            
            result = {
                'rows': result_rows,
                'rowCount': len(result_rows)
            }
        else:
            # For INSERT, UPDATE, DELETE queries
            result = {
                'rows': [],
                'rowCount': cursor.rowcount
            }
        
        cursor.close()
        conn.close()
        
        # Return JSON result
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            'error': str(e),
            'rows': [],
            'rowCount': 0
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
