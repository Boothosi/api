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
    return jsonify(result)

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
    is_replaced = 0
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
        'UPDATE MOPS SET in_use = ? WHERE tag = ?',
        (in_use, tag)
    )
    conn.commit()
    conn.close()
    return jsonify(message="Updated successfully")

@app.route('/api/update/mop/usage', methods=['POST'])
def update_mop_usage():
    data = request.get_json()
    tag = data.get('tag')
    usage = data.get('usage')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE MOPS SET usage = ? WHERE tag = ? AND is_replaced = 0',
        (usage, tag)
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

# # Get the usage for every mop
# @app.route('/api/mops/usage/all', methods=['GET'])
# def get_tags_usage():
#     usage = list(map(lambda tag: {
#         "id": tag["id"],
#         "mac_address": tag["mac_address"],
#         "usage": tag["usage"]
#     }, mock_mops_tags))
#     return jsonify(usage)

# # Get the usage status of tag's mop
# @app.route('/api/mops/usage/greater_than/<int:count>', methods=['GET'])
# def get_tags_by_usage_greater_than(count):
#     filtered_tags = list(filter(lambda tag: tag["usage"] > count, mock_mops_tags))
#     return jsonify(filtered_tags)

# # Get all mops that are in the laundry
# @app.route('/api/mops/in_laundry', methods=['GET'])
# def get_tags_in_laundry():
#     mops_in_laundry = list(filter(lambda tag: not tag["in_use"], mock_mops_tags))
#     return jsonify(mops_in_laundry)

# # Get all tags that are currently in use
# @app.route('/api/mops/in_use', methods=['GET'])
# def get_tags_in_use():
#     mops_in_use = list(filter(lambda tag: tag["in_use"], mock_mops_tags))
#     return jsonify(mops_in_use)

# # Get all tags that are missing
# # Missing iff in_use == False && the work turn is over
# @app.route('/api/mops/missing', methods=['GET'])
# def get_missing_tags():
#     missing_tags = list(filter(lambda tag: tag["is_missing"], mock_mops_tags))
#     return jsonify(missing_tags)

# # Get the last known location of the missing mops
# @app.route('/api/mops/missing/last_location', methods=['GET'])
# def get_missing_tags_location():
#     missing_tags_location = list(map(lambda tag: {
#         "id": tag["id"],
#         "mac_address": tag["mac_address"],
#         "last_location": tag["last_location"]
#     }, filter(lambda tag: tag["is_missing"], mock_mops_tags))
#     )
#     return jsonify(missing_tags_location)

# # Get the last known time of the missing mops
# @app.route('/api/mops/missing/last_time_used', methods=['GET'])
# def get_missing_tags_time():
#     missing_tags_time = list(map(lambda tag: {
#         "id": tag["id"],
#         "mac_address": tag["mac_address"],
#         "last_turn": tag["last_turn"]
#     }, filter(lambda tag: tag["is_missing"], mock_mops_tags))
#     )
#     return jsonify(missing_tags_time)

# # Get the usage of the missing mops
# @app.route('/api/mops/missing/usage', methods=['GET'])
# def get_missing_tags_usage():
#     missing_tags_usage = list(map(lambda tag: {
#         "id": tag["id"],
#         "mac_address": tag["mac_address"],
#         "usage": tag["usage"]
#     }, filter(lambda tag: tag["is_missing"], mock_mops_tags))
#     )
#     return jsonify(missing_tags_usage)

# # Change the mop (reset the tag usage), identify the mop by mac_address
# @app.route('/api/mops/change/<string:mac_address>', methods=['POST'])
# def change_mop(mac_address):
#     for tag in mock_mops_tags:
#         if tag["mac_address"] == mac_address:
#             tag["usage"] = 0
#             tag["in_use"] = False
#             return jsonify(tag)
#     return jsonify(message="Tag not found")

# @app.route('/api/mops/location', methods=['POST'])
# @app.route('/api/mops/location', methods=['POST'])
# def notify_mop_location():
#     # Get data from the POST request (expecting JSON with mac_address and location)
#     data = request.get_json()
    
#     mac_address = data.get('mac_address')
#     location = data.get('location')

#     if not mac_address or not location:
#         return jsonify(message="Mac address and location are required"), 400
    
#     # Get the current timestamp (this will be stored in the 'last_turn' field)
#     current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date for checking (no time part)

#     # Store the mop location and timestamp in the SQLite database
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     # Check if the mop has been in laundry, moved to another location, and returned to laundry
#     cursor.execute('''
#         SELECT * FROM MOCKAROO_DATA 
#         WHERE mac_address = ? AND DATE(last_turn) = ?
#         ORDER BY last_turn DESC
#     ''', (mac_address, current_date))
#     previous_entries = cursor.fetchall()

#     # Determine the status for 'in_use'
#     in_use_status = 'true'  # Default to in_use = true for any location
    
#     if previous_entries:
#         # Check if the mop has been in laundry, then moved elsewhere, and returned to laundry
#         for entry in previous_entries:
#             last_location = entry[3]  # last_location is at index 3
#             if last_location == 'laundry' and len(previous_entries) > 1:
#                 for i in range(1, len(previous_entries)):
#                     if previous_entries[i][3] != 'laundry':  # If it has been to another location
#                         # If the mop was in laundry, moved to another location, and then back to laundry
#                         in_use_status = 'false'
#                         break
#                 break
    
#     # Insert or update the mop's location in the database
#     cursor.execute('''
#         SELECT * FROM MOCKAROO_DATA 
#         WHERE mac_address = ? AND last_location = ? AND DATE(last_turn) = ?
#     ''', (mac_address, location, current_date))

#     existing_mop = cursor.fetchone()

#     if existing_mop:
#         # If the record exists, update the timestamp and in_use status
#         cursor.execute('''
#             UPDATE MOCKAROO_DATA
#             SET last_turn = ?, in_use = ?
#             WHERE mac_address = ? AND last_location = ? AND DATE(last_turn) = ?
#         ''', (current_timestamp, in_use_status, mac_address, location, current_date))
#         message = "Mop location timestamp updated successfully"
#     else:
#         # If no record exists, insert a new record with in_use status
#         cursor.execute('''
#             INSERT INTO MOCKAROO_DATA (mac_address, last_location, last_turn, in_use)
#             VALUES (?, ?, ?, ?)
#         ''', (mac_address, location, current_timestamp, in_use_status))
#         message = "Mop location and timestamp posted successfully"
    
#     # Commit changes and close the connection
#     conn.commit()
#     conn.close()
    
#     return jsonify(message=message, mac_address=mac_address, location=location, timestamp=current_timestamp)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
