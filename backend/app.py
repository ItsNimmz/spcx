from flask import Flask, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import json
import os
from dotenv import load_dotenv

load_dotenv()

from . import main  # If both are in the same package # Import any Python logic you need to run
import database

app = Flask(__name__)
CORS(app)

# MySQL configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/api/launches/stats', methods=['GET'])
def get_launch_stats():
    try:
        cur = mysql.connection.cursor()
        
        # Get yearly success rates
        cur.execute("""
            SELECT launch_year as year, 
                   COUNT(*) as total_launches,
                   SUM(launch_success) as successful_launches,
                   ROUND(SUM(launch_success)/COUNT(*)*100, 1) as success_rate
            FROM launches
            GROUP BY launch_year
            ORDER BY launch_year
        """)
        yearly_stats = cur.fetchall()
    
        # Get rocket payload stats
        cur.execute("""
            SELECT rocket_name as rocket,
                   COUNT(*) as launch_count,
                   ROUND(AVG(payload_mass_kg), 1) as avg_payload,
                   ROUND(SUM(payload_mass_kg), 1) as total_payload
            FROM launches
            GROUP BY rocket_name
        """)
        rocket_stats = cur.fetchall()
        
        cur.close()
        
        return jsonify({
            'yearly_stats': yearly_stats,
            'rocket_stats': rocket_stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Path to the JSON file
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'launch_data.json')
@app.route('/api/launches/metrix', methods=['GET'])
def get_launch_metrix():
    
    # Check if the file exists
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r') as file:
            try:
                launch_data = json.load(file)  # Load JSON data from the file
                return jsonify(launch_data)  # Return the JSON data as the response
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid JSON format in file"}), 400
    else:
        return jsonify({"error": f"File {DATA_FILE_PATH} not found"}), 404

if __name__ == '__main__':
    main.run_initial_logic()  # Call the function from `main.py`
    database.create_table()
    app.run(debug=True, port=5000)