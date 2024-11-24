from flask import Flask, request, jsonify
import uuid
from datetime import datetime
import re
import math

app = Flask(__name__)

# Dictionary to store receipts and their corresponding points in memory
receipts = {}

# Function to calculate points for a receipt based on specific rules
def calculate_points(receipt):
    points = 0

    # One point for each alphanumeric character in the retailer's name
    retailer_name = receipt.get('retailer', '')
    alphanumeric_chars = re.findall(r'[A-Za-z0-9]', retailer_name)
    points += len(alphanumeric_chars)

    # 50 points if the total is a round dollar amount with no cents
    try:
        total = float(receipt.get('total', '0'))
        if total.is_integer():
            points += 50
    except ValueError:
        total = 0

    # 25 points if the total is a multiple of 0.25
    if (total * 100) % 25 == 0:
        points += 25

    # 5 points for every two items on the receipt
    items = receipt.get('items', [])
    points += (len(items) // 2) * 5

    # 0.2 * price (rounded up) for items with description length multiple of 3
    for item in items:
        description = item.get('shortDescription', '').strip()
        if len(description) % 3 == 0:
            try:
                price = float(item.get('price', '0'))
                bonus = math.ceil(price * 0.2)
                points += bonus
            except ValueError:
                continue

    # 6 points if the purchase date is an odd day
    purchase_date = receipt.get('purchaseDate', '')
    try:
        date_obj = datetime.strptime(purchase_date, '%Y-%m-%d')
        if date_obj.day % 2 == 1:
            points += 6
    except ValueError:
        pass

    # 10 points if purchase time is between 2:00 PM and 4:00 PM
    purchase_time = receipt.get('purchaseTime', '')
    try:
        time_obj = datetime.strptime(purchase_time, '%H:%M')
        if 14 <= time_obj.hour < 16:
            points += 10
    except ValueError:
        pass

    return points

# This route processes a receipt, calculates its points, and returns a unique ID for tracking
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.get_json()
    if not receipt:
        return jsonify({'error': 'Invalid JSON'}), 400

    # Validating required fields, if they are provided in the request
    required_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    for field in required_fields:
        if field not in receipt:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Generating a unique receipt ID and calculate its points
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)

    # Store the receipt ID and associated points
    receipts[receipt_id] = points

    return jsonify({'id': receipt_id}), 200

# This route lets users fetch the points for a given receipt ID
@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = receipts.get(receipt_id)
    if points is None:
        return jsonify({'error': 'Receipt ID not found'}), 404

    return jsonify({'points': points}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)