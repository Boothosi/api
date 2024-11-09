import random
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# Fix local CORS errors
CORS(app)

# Load sqlite database
DATABASE = './database.db'

# Generator for some mock tags for the mops
def generate_mac_address():
    return ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))

def generate_mock_mop_tags(num_tags):
    tags = []
    for i in range(num_tags):
        tag = {
            "id": i + 1,
            "mac_address": generate_mac_address(),
            "last_turn": random.choice(["Morning", "Afternoon", "Night"]),
            "last_location": random.choice(["Critical Care Unit", "Emergency Room", "Operating Room"]),
            "usage": random.randint(0, 100),
            "in_use": random.choice([True, False]),
            "is_missing": random.choice([True, False])
        }
        tags.append(tag)
    return tags

# List of mop tags
# Each mop has a tag, and its usage decreases with each laundry cycle
# When a mop's lifetime ends, its tag usage is reset
# A tag with usage 0 indicates a mop change
mock_mops_tags = generate_mock_mop_tags(10)

# Home route that returns a welcome message for the MopTag API
@app.route('/')
def home():
    return jsonify(message="MopTag API")

# TEST: get all from db
@app.route('/db')
def all_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM MOCKAROO_DATA'
    )
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# Get the data of all mops
@app.route('/api/mops/all', methods=['GET'])
def get_all_tags():
    return jsonify(mock_mops_tags)

# Get the usage for every mop
@app.route('/api/mops/usage/all', methods=['GET'])
def get_tags_usage():
    usage = list(map(lambda tag: {
        "id": tag["id"],
        "mac_address": tag["mac_address"],
        "usage": tag["usage"]
    }, mock_mops_tags))
    return jsonify(usage)

# Get the usage status of tag's mop
@app.route('/api/mops/usage/greater_than/<int:count>', methods=['GET'])
def get_tags_by_usage_greater_than(count):
    filtered_tags = list(filter(lambda tag: tag["usage"] > count, mock_mops_tags))
    return jsonify(filtered_tags)

# Get all mops that are in the laundry
@app.route('/api/mops/in_laundry', methods=['GET'])
def get_tags_in_laundry():
    mops_in_laundry = list(filter(lambda tag: not tag["in_use"], mock_mops_tags))
    return jsonify(mops_in_laundry)

# Get all tags that are currently in use
@app.route('/api/mops/in_use', methods=['GET'])
def get_tags_in_use():
    mops_in_use = list(filter(lambda tag: tag["in_use"], mock_mops_tags))
    return jsonify(mops_in_use)

# Get all tags that are missing
# Missing iff in_use == False && the work turn is over
@app.route('/api/mops/missing', methods=['GET'])
def get_missing_tags():
    missing_tags = list(filter(lambda tag: tag["is_missing"], mock_mops_tags))
    return jsonify(missing_tags)

# Get the last known location of the missing mops
@app.route('/api/mops/missing/last_location', methods=['GET'])
def get_missing_tags_location():
    missing_tags_location = list(map(lambda tag: {
        "id": tag["id"],
        "mac_address": tag["mac_address"],
        "last_location": tag["last_location"]
    }, filter(lambda tag: tag["is_missing"], mock_mops_tags))
    )
    return jsonify(missing_tags_location)

# Get the last known time of the missing mops
@app.route('/api/mops/missing/last_time_used', methods=['GET'])
def get_missing_tags_time():
    missing_tags_time = list(map(lambda tag: {
        "id": tag["id"],
        "mac_address": tag["mac_address"],
        "last_turn": tag["last_turn"]
    }, filter(lambda tag: tag["is_missing"], mock_mops_tags))
    )
    return jsonify(missing_tags_time)

# Get the usage of the missing mops
@app.route('/api/mops/missing/usage', methods=['GET'])
def get_missing_tags_usage():
    missing_tags_usage = list(map(lambda tag: {
        "id": tag["id"],
        "mac_address": tag["mac_address"],
        "usage": tag["usage"]
    }, filter(lambda tag: tag["is_missing"], mock_mops_tags))
    )
    return jsonify(missing_tags_usage)

# Change the mop (reset the tag usage), identify the mop by mac_address
@app.route('/api/mops/change/<string:mac_address>', methods=['POST'])
def change_mop(mac_address):
    for tag in mock_mops_tags:
        if tag["mac_address"] == mac_address:
            tag["usage"] = 0
            tag["in_use"] = False
            return jsonify(tag)
    return jsonify(message="Tag not found")

# Notify about a mop location, storing in database
# Notify about a mop location, storing in database
@app.route('/api/mops/location', methods=['POST'])
def notify_mop_location():
    # Get data from the POST request (expecting JSON with mac_address and location)
    data = request.get_json()
    
    mac_address = data.get('mac_address')
    location = data.get('location')

    if not mac_address or not location:
        return jsonify(message="Mac address and location are required"), 400
    
    # Store the mop location in the SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Insert the location data into the mop_locations table
    cursor.execute('''
        INSERT INTO MOCKAROO_DATA (mac_address, last_location)
        VALUES (?, ?)
    ''', (mac_address, location))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    return jsonify(message="Mop location notified successfully", mac_address=mac_address, location=location)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
