import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
@app.route('/api/mops/is_missing', methods=['GET'])
def get_tags_is_missing():
    missing_tags = list(filter(lambda tag: tag["is_missing"], mock_mops_tags))
    return jsonify(missing_tags)

# Get the data of missing mops
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

if __name__ == '__main__':
    app.run(debug=True)