# ------------------------------------------------------------
# Educational Database Lookup API - Nexxon Hackers Edition
# Developed by: Creator Shyamchand & Ayan
# Organization: CEO & Founder Of - Nexxon Hackers
# FOR EDUCATIONAL PURPOSES ONLY
# ------------------------------------------------------------

from flask import Flask, jsonify, request, render_template_string
import sqlite3
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

COPYRIGHT_STRING = "Creator Shyamchand & Ayan - CEO & Founder Of - Nexxon Hackers"

CSV_FILE = "data.csv"
DB_FILE = "data.db"

# ---------------- HTML TEMPLATE ----------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Database Lookup API - Nexxon Hackers</title>
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css" rel="stylesheet">
<style>
.gradient-bg { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); }
.glass-effect { backdrop-filter: blur(10px); background: rgba(255,255,255,0.85); }
.json-viewer { background: #1e1e1e; border-radius: 8px; padding: 16px; overflow-x: auto; font-family: monospace; font-size: 13px; max-height: 500px; }
.json-key { color: #9cdcfe; } .json-string { color: #ce9178; } .json-number { color: #b5cea8; }
</style>
</head>
<body class="bg-gradient-to-br from-indigo-50 via-white to-purple-50 min-h-screen">
<main class="pt-8 pb-12 px-4 max-w-5xl mx-auto">
    
    <header class="text-center py-8">
        <div class="inline-flex items-center justify-center w-20 h-20 gradient-bg rounded-3xl mb-6 shadow-xl">
            <i class="ri-database-2-line text-white ri-3x"></i>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Database Lookup API</h1>
        <p class="text-lg text-gray-600 mb-2">Educational Database Query System</p>
        <p class="text-sm text-gray-500">For Educational Purposes Only</p>
        <div class="mt-4 inline-flex gap-2">
            <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">⚠️ Educational Use Only</span>
            <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">No API Key</span>
        </div>
    </header>

    <!-- API Endpoints -->
    <section class="mb-8 bg-white rounded-3xl p-6 shadow-xl border border-indigo-100">
        <h2 class="text-xl font-bold text-gray-900 mb-4">📡 API Endpoints</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 border border-indigo-100">
                <h3 class="font-semibold text-gray-900 mb-2">🔍 Search by ID</h3>
                <code class="text-xs bg-gray-900 text-green-400 p-2 rounded block mb-2">/api/search/{id_number}</code>
                <p class="text-xs text-gray-600">Search database by ID number</p>
            </div>
            <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 border border-indigo-100">
                <h3 class="font-semibold text-gray-900 mb-2">📞 Search by Phone</h3>
                <code class="text-xs bg-gray-900 text-green-400 p-2 rounded block mb-2">/api/phone/{phone_number}</code>
                <p class="text-xs text-gray-600">Search database by phone number</p>
            </div>
        </div>
    </section>

    <!-- Sample Response -->
    <section class="mb-8 bg-gray-900 rounded-2xl p-6">
        <h2 class="text-xl font-bold text-white mb-4">📋 Sample Response</h2>
        <pre class="text-green-400 text-xs overflow-x-auto">{
  "success": true,
  "data": {
    "name": "Sample Name",
    "phone": "1234567890",
    "address": "Sample Address",
    "city": "Sample City",
    "state": "Sample State"
  },
  "checked_at": "2026-04-28 10:30:45 UTC",
  "api_info": {
    "developed_by": "Creator Shyamchand & Ayan",
    "organization": "CEO & Founder Of - Nexxon Hackers"
  }
}</pre>
    </section>

    <div class="text-center py-6">
        <div class="inline-block gradient-bg text-white px-8 py-4 rounded-2xl shadow-xl">
            <p class="font-bold text-lg">Developed by Creator Shyamchand & Ayan</p>
            <p class="text-sm opacity-95">CEO & Founder Of - Nexxon Hackers</p>
        </div>
        <p class="text-xs text-gray-500 mt-4">⚠️ This is an educational project. Do not use for illegal purposes.</p>
    </div>

</main>
</body>
</html>
'''

def create_db_from_csv():
    """Create SQLite DB from CSV file"""
    print("Creating database from CSV...")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS people (
            name TEXT,
            fathersName TEXT,
            phoneNumber TEXT,
            otherNumber TEXT,
            passportNumber TEXT,
            aadharNumber TEXT,
            age TEXT,
            gender TEXT,
            address TEXT,
            district TEXT,
            pincode TEXT,
            state TEXT,
            town TEXT
        )
    """)
    conn.commit()

    with open(CSV_FILE, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        rows = []
        for i, row in enumerate(reader, start=1):
            values = [row.get(h, "") for h in [
                "name", "fathersName", "phoneNumber", "otherNumber",
                "passportNumber", "aadharNumber", "age", "gender",
                "address", "district", "pincode", "state", "town"
            ]]
            rows.append(values)
            if len(rows) >= 1000:
                cur.executemany("INSERT INTO people VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
                conn.commit()
                rows.clear()
                print(f"Inserted {i} rows...")
        if rows:
            cur.executemany("INSERT INTO people VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
            conn.commit()

    conn.close()
    print("Database created successfully!")

def query_db(field, value):
    """Query database by field"""
    if not os.path.exists(DB_FILE):
        return None
    
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM people WHERE {field}=?", (value,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

# Initialize database
if not os.path.exists(DB_FILE):
    if os.path.exists(CSV_FILE):
        create_db_from_csv()
    else:
        print("Warning: data.csv not found. Database will be empty.")

# ---------------- API ROUTES ----------------
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/search/<query>")
def search_by_id(query):
    """Search by any ID number"""
    data = query_db("aadharNumber", query)
    
    if not data:
        data = query_db("passportNumber", query)
    
    if data:
        return jsonify({
            "success": True,
            "data": data,
            "checked_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "api_info": {
                "developed_by": "Creator Shyamchand & Ayan",
                "organization": "CEO & Founder Of - Nexxon Hackers"
            }
        })
    
    return jsonify({
        "success": False,
        "error": "Record not found",
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    }), 404

@app.route("/api/phone/<number>")
def search_by_phone(number):
    """Search by phone number"""
    data = query_db("phoneNumber", number)
    
    if not data:
        data = query_db("otherNumber", number)
    
    if data:
        return jsonify({
            "success": True,
            "data": data,
            "checked_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "api_info": {
                "developed_by": "Creator Shyamchand & Ayan",
                "organization": "CEO & Founder Of - Nexxon Hackers"
            }
        })
    
    return jsonify({
        "success": False,
        "error": "Record not found",
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    }), 404

@app.route("/api/health")
def health():
    """Health check"""
    db_exists = os.path.exists(DB_FILE)
    db_size = os.path.getsize(DB_FILE) if db_exists else 0
    
    return jsonify({
        "status": "healthy" if db_exists else "no_database",
        "database_size": f"{db_size / 1024:.2f} KB" if db_exists else "N/A",
        "timestamp": datetime.utcnow().isoformat(),
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "available_endpoints": ["/", "/api/search/{id}", "/api/phone/{number}", "/api/health"],
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    }), 404

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
