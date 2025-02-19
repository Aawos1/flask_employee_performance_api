from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# Database connection parameters
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres.cutuhjamlftcpgeedykn",
    "password": "Z6vZyi1MHF2qGz12",
    "host": "aws-0-us-east-1.pooler.supabase.com",
    "port": "6543"
}

# Function to establish a connection to the database
def get_db_connection():
    conn = psycopg2.connect(**DB_PARAMS)
    return conn

# Endpoint to get all employee performance records
@app.route('/employee_performance', methods=['GET'])
def get_employee_performance():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM auth.employee_performance;")
    rows = cursor.fetchall()
    
    # Format the data as a list of dictionaries
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "employee_id": row[1],
            "performance_score": row[2],
            "evaluated_at": row[3],
        })
    
    conn.close()
    return jsonify(results)

# Endpoint to get a specific employee performance by ID
@app.route('/employee_performance/<employee_id>', methods=['GET'])
def get_employee_performance_by_id(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM auth.employee_performance WHERE employee_id = %s;", (employee_id,))
    row = cursor.fetchone()
    
    if row:
        result = {
            "id": row[0],
            "employee_id": row[1],
            "performance_score": row[2],
            "evaluated_at": row[3],
        }
        conn.close()
        return jsonify(result)
    else:
        conn.close()
        return jsonify({"error": "Employee not found"}), 404

# Endpoint to insert a new performance record
@app.route('/employee_performance', methods=['POST'])
def add_employee_performance():
    data = request.get_json()
    
    employee_id = data.get('employee_id')
    performance_score = data.get('performance_score')
    evaluated_at = data.get('evaluated_at')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO auth.employee_performance (employee_id, performance_score, evaluated_at)
        VALUES (%s, %s, %s);
    """, (employee_id, performance_score, evaluated_at))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Employee performance record added"}), 201

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
