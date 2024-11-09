import random
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
# Fix local CORS errors
CORS(app)

# Load sqlite database
DATABASE = './database.db'

# Home route that returns a welcome message for the MopTag API
@app.route('/')
def home():
    return jsonify(message="MopTag API")

# TEST: get all from db
@app.route('/api/tags/all', methods=['GET'])
def all_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM TAGS'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(data=result)

# Set resettable tag
@app.route('/api/tags/resettable', methods=['POST'])
def set_resettable():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    data = request.get_json()
    mac_address = data.get('mac_address')
    resettable = data.get('resettable')
    print("dioboia"+str(resettable))
    cursor.execute('UPDATE TAGS SET resettable = ? WHERE mac_address = ?;',(resettable, mac_address))
    return jsonify(message="Set tag "+mac_address+" to resettable: "+ str(resettable))


@app.route('/api/mops/all', methods=['GET'])
def all_mops():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM MOPS'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

@app.route('/api/history/all', methods=['GET'])
def all_location():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM HISTORY'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

@app.route('/api/insert/tag/', methods=['POST'])
def insert_db():
    data = request.get_json()
    mac_address = data.get('mac_address')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO TAGS (mac_address) VALUES (?)',
        (mac_address, )
    )
    conn.commit()
    conn.close()
    return jsonify(message="Inserted successfully")

@app.route('/api/insert/mop/', methods=['POST'])
def insert_mop():
    data = request.get_json()
    tag = data.get('tag')
    last_location = "laundry"
    last_seen_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO MOPS (tag, last_location, last_seen_datetime) VALUES (?, ?, ?)',
        (tag, last_location, last_seen_datetime)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Inserted successfully")

@app.route('/api/update/mop/is_replaced', methods=['POST'])
def update_mop_is_replaced():
    data = request.get_json()
    tag = data.get('tag')
    is_replaced = 1
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE MOPS SET is_replaced = ? WHERE tag = ? AND is_replaced = 0',
        (is_replaced, tag)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Updated successfully")

@app.route('/api/update/mop/in_use', methods=['POST'])
def update_mop_in_use():
    data = request.get_json()
    tag = data.get('tag')
    in_use = data.get('in_use')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE MOPS SET in_use = ? WHERE tag = ? AND is_replaced = 0',
        (in_use, tag)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Updated successfully")

@app.route('/api/update/mop/usage', methods=['POST'])
def update_mop_usage():
    data = request.get_json()
    tag = data.get('tag')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE MOPS SET usage = usage + 1 WHERE tag = ? AND is_replaced = 0',
        (tag, )
    )
    conn.commit()
    conn.close()
    return jsonify(message="Updated successfully")

@app.route('/api/update/mop/last_location', methods=['POST'])
def update_mop_last_location():
    data = request.get_json()
    tag = data.get('tag')
    last_location = data.get('last_location')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE MOPS SET last_location = ? WHERE tag = ? AND is_replaced = 0',
        (last_location, tag)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Updated successfully")

@app.route('/api/update/mop/last_seen_datetime', methods=['POST'])
def update_mop_last_seen_datetime():
    data = request.get_json()
    tag = data.get('tag')
    last_seen_datetime = data.get('last_seen_datetime')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE MOPS SET last_seen_datetime = ? WHERE tag = ? AND is_replaced = 0',
        (last_seen_datetime, tag)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Updated successfully")

@app.route('/api/insert/history/', methods=['POST'])
def insert_history():
    data = request.get_json()
    tag = data.get('tag')
    location = data.get('location')
    timestamp = data.get('timestamp')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO HISTORY (tag, location, timestamp) VALUES (?, ?, ?)',
        (tag, location, timestamp)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Inserted successfully")

# Get the usage for every mop
@app.route('/api/mops/usage/all', methods=['GET'])
def get_mops_usage():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, usage FROM MOPS'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get the usage of mops that are currently in use
@app.route('/api/mops/usage/in_use', methods=['GET'])
def get_mops_usage_in_use():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, usage FROM MOPS WHERE in_use = 1'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get the number of mops that are not in use and are not missing group by date in history
@app.route('/api/history/storage', methods=['GET'])
def get_history_storage():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT timestamp, COUNT(DISTINCT tag) as count FROM HISTORY WHERE location = "laundry" GROUP BY DATE(timestamp)'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get the usage of mops that are missing
@app.route('/api/mops/usage/missing', methods=['GET'])
def get_mops_usage_missing():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, usage FROM MOPS WHERE is_missing = 1 AND in_use = 0'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get the last known location of the missing mops
@app.route('/api/mops/missing/last_location', methods=['GET'])
def get_missing_mops_location():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, last_location FROM MOPS WHERE is_missing = 1 AND in_use = 0'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get the last known time of the missing mops
@app.route('/api/mops/missing/last_seen_datetime', methods=['GET'])
def get_missing_mops_time():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, last_seen_datetime FROM MOPS WHERE is_missing = 1 AND in_use = 0'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get the usage status of tag's mop
@app.route('/api/mops/usage/<string:tag>', methods=['GET'])
def get_mop_usage(tag):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT usage FROM MOPS WHERE tag = ?',
        (tag, )
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchone()
    result = dict(zip(columns, data))
    conn.close()
    return jsonify(result)


# Get all mops that are in the laundry
@app.route('/api/mops/laundry', methods=['GET'])
def get_mops_laundry():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM MOPS WHERE last_location = "laundry"'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get all tags that are currently in use
@app.route('/api/tags/in_use', methods=['GET'])
def get_tags_in_use():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM TAGS WHERE in_use = 1'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# Get all tags that are missing
@app.route('/api/tags/missing', methods=['GET'])
def get_missing_tags():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM TAGS WHERE is_missing = 1'
    )
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    conn.close()
    return jsonify(result)

# 

# Change the mop (reset the tag usage), identify the mop by mac_address
@app.route('/api/mops/change', methods=['POST'])
def change_mop():
    data = request.get_json()
    tag = data.get('tag')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE MOPS SET is_replaced = 1, in_use = 0 WHERE tag = ?',
        (tag, )
    )
    last_location = "laundry"
    last_seen_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        'INSERT INTO MOPS (tag, last_location, last_seen_datetime) VALUES (?, ?, ?)',
        (tag, last_location, last_seen_datetime)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Mop usage reset successfully")

# Insert a new location and then update the mop's if needed
@app.route('/api/history/notify', methods=['POST'])
def notify_location():
    data = request.get_json()
    tag = data.get('tag')
    location = data.get('location')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Select the last histories of the current day and order them from the most recent one
    current_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(
        'SELECT * FROM HISTORY WHERE tag = ? AND DATE(timestamp) = ? ORDER BY timestamp DESC',
        (tag, current_date)
    )
    history_entries = cursor.fetchall()

    if history_entries:
        last_entry = history_entries[0]
        last_location = last_entry[2]  # Assuming location is the third column

        # Check if the last entry location is the same as the new location
        if last_location == location:
            # Update the timestamp of the last entry
            cursor.execute(
                'UPDATE HISTORY SET timestamp = ? WHERE id = ?',
                (timestamp, last_entry[0])
            )
            # Also update mop
            cursor.execute(
                'UPDATE MOPS SET last_seen_datetime = ? WHERE tag = ? AND is_replaced = 0',
                (timestamp, tag)
            )
        elif last_location == "laundry" and any(entry[2] != "laundry" for entry in history_entries[1:]):
            # Update the in_use status of the mop to 0 and increment the usage by 1
            cursor.execute(
                'UPDATE MOPS SET in_use = 0, usage = usage + 1 WHERE tag = ?',
                (tag, )
            )
        else:
            # Insert a new entry
            cursor.execute(
                'INSERT INTO HISTORY (tag, location, timestamp) VALUES (?, ?, ?)',
                (tag, location, timestamp)
            )
            # Also update the mop in use
            cursor.execute(
                'UPDATE MOPS SET in_use = 1 WHERE tag = ? AND is_replaced = 0',
                (tag, )
            )
    else:
        # If no history entries exist, insert a new entry
        cursor.execute(
            'INSERT INTO HISTORY (tag, location, timestamp) VALUES (?, ?, ?)',
            (tag, location, timestamp)
        )

    conn.commit()
    conn.close()
    return jsonify(message="Location notified and updated everything successfully")

    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
