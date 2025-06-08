from flask import Flask, request, jsonify
import os
from utils import query_db, modify_db, error_response, validate_email, format_datetime_for_display
from db import init_db

app = Flask(__name__)

@app.route('/classes', methods=['GET'])
def get_classes():
    tz = request.args.get("tz", "Asia/Kolkata")
    classes = query_db("SELECT * FROM fitness_classes WHERE scheduled_at >= datetime('now')")
    result = []
    for c in classes:
        local_datetime = format_datetime_for_display(c['scheduled_at'], tz)
        result.append({
            "id": c['id'],
            "name": c['name'],
            "instructor": c['instructor'],
            "scheduled_at": local_datetime,
            "available_slots": c['available_slots']
        })
    return jsonify(result), 200

@app.route('/book', methods=['POST'])
def book_class():
    data = request.get_json()
    required_fields = ['class_id', 'client_name', 'client_email']
    if not all(field in data for field in required_fields):
        return error_response("Invalid request, Missing: class_id or client_name or client_email")

    if not validate_email(data['client_email']):
        return error_response("Invalid email address")

    class_info = query_db("SELECT * FROM fitness_classes WHERE id = ?", (data['class_id'],), one=True)
    if not class_info:
        return error_response("Class not found", 404)

    if class_info['available_slots'] <= 0:
        return error_response("No slots available")

    modify_db("INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)",
              (data['class_id'], data['client_name'], data['client_email']))
    modify_db("UPDATE fitness_classes SET available_slots = available_slots - 1 WHERE id = ?", (data['class_id'],))
    
    return jsonify({"message": "Booking successful"}), 200

@app.route('/bookings', methods=['GET'])
def get_bookings():
    email = request.args.get("client_email")
    tz = request.args.get("tz", "Asia/Kolkata")  # Default to IST

    if not email or not validate_email(email):
        return error_response("Invalid or missing email")

    bookings = query_db(
        "SELECT b.id, fc.name, fc.scheduled_at, fc.instructor FROM bookings b JOIN fitness_classes fc ON b.class_id = fc.id WHERE b.client_email = ?",
        (email,))
    
    return jsonify([
        {
            "booking_id": b['id'],
            "class_name": b['name'],
            "instructor": b['instructor'],
            "scheduled_at": format_datetime_for_display(b['scheduled_at'], tz)
        } for b in bookings
    ]), 200

if __name__ == '__main__':
    # Use default DB for app run
    os.environ.setdefault('DB_PATH', 'fitness_studio.db')
    init_db()
    app.run(debug=True)
