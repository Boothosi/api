from flask import Flask, jsonify
import random


app = Flask(__name__)

def generate_mac_address():
    return ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))

def generate_mock_tags(num_tags):
    tags = []
    for i in range(num_tags):
        tag = {
            "id": i + 1,
            "mac_address": generate_mac_address(),
            "wash_count": random.randint(0, 100),
            "is_out": random.choice([True, False]),
            "is_missing": random.choice([True, False])
        }
        tags.append(tag)
    return tags

mock_tags = generate_mock_tags(10)

@app.route('/')
def home():
    return jsonify(message="MopTag API")

@app.route('/api/tags/all', methods=['GET'])
def get_all_tags():
    return jsonify(mock_tags)

@app.route('/api/tags/wash_count/greater_than/<int:count>', methods=['GET'])
def get_tags_by_wash_count_greater_than(count):
    filtered_tags = list(filter(lambda tag: tag["wash_count"] > count, mock_tags))
    return jsonify(filtered_tags)

@app.route('/api/tags/is_out', methods=['GET'])
def get_tags_is_out():
    out_tags = list(filter(lambda tag: tag["is_out"], mock_tags))
    # return jsonify([tag for tag in mock_tags if tag["is_out"]])
    return jsonify(out_tags)

if __name__ == '__main__':
    app.run(debug=True)