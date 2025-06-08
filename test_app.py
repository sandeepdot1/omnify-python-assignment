import pytest
import json
import os
from app import app, init_db
from db import get_db_connection

@pytest.fixture
def test_client():
    # Use a separate test DB
    os.environ['DB_PATH'] = 'test_fitness_studio.db'

    # Initialize fresh test DB before each test function
    init_db()

    # Optionally, clear data before each test 
    conn = get_db_connection()
    conn.execute("DELETE FROM bookings")
    conn.execute("DELETE FROM fitness_classes")
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client

    # Cleanup test DB file after tests (optional)
    # import os
    # if os.path.exists('test_fitness.db'):
    #     os.remove('test_fitness.db')

def test_get_classes(test_client):
    response = test_client.get('/classes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'name' in data[0]
        assert 'scheduled_at' in data[0]

def test_successful_booking(test_client):
    # Seed a class with available slots first
    conn = get_db_connection()
    conn.execute("INSERT INTO fitness_classes (name, instructor, scheduled_at, available_slots) VALUES (?, ?, datetime('now', '+1 day'), ?)",
                 ("Test Yoga", "Test Instructor", 2))
    conn.commit()
    conn.close()

    # Get class id of the inserted record
    conn = get_db_connection()
    cur = conn.execute("SELECT id FROM fitness_classes WHERE name = ?", ("Test Yoga",))
    class_id = cur.fetchone()['id']
    conn.close()

    payload = {
        "class_id": class_id,
        "client_name": "John Doe",
        "client_email": "john@example.com"
    }
    response = test_client.post('/book', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Booking successful"

def test_overbooking(test_client):
    # Insert a class with 1 slot
    conn = get_db_connection()
    conn.execute("INSERT INTO fitness_classes (name, instructor, scheduled_at, available_slots) VALUES (?, ?, datetime('now', '+1 day'), ?)",
                 ("Limited Class", "Instructor", 1))
    conn.commit()
    conn.close()

    # Fetch the class id
    conn = get_db_connection()
    cur = conn.execute("SELECT id FROM fitness_classes WHERE name = ?", ("Limited Class",))
    class_id = cur.fetchone()['id']
    conn.close()

    payload = {
        "class_id": class_id,
        "client_name": "Jane",
        "client_email": "jane@example.com"
    }

    # 1st booking should succeed
    resp1 = test_client.post('/book', json=payload)
    assert resp1.status_code == 200

    # 2nd booking should fail
    resp2 = test_client.post('/book', json=payload)
    assert resp2.status_code == 400
    data = resp2.get_json()
    assert "No slots available" in data['error']

def test_get_bookings(test_client):
    # Seed a class and book it
    conn = get_db_connection()
    conn.execute("INSERT INTO fitness_classes (name, instructor, scheduled_at, available_slots) VALUES (?, ?, datetime('now', '+1 day'), ?)",
                 ("Booked Class", "Instructor", 5))
    conn.commit()
    cur = conn.execute("SELECT id FROM fitness_classes WHERE name = ?", ("Booked Class",))
    class_id = cur.fetchone()['id']
    conn.close()

    payload = {
        "class_id": class_id,
        "client_name": "Alice",
        "client_email": "alice@example.com"
    }
    test_client.post('/book', json=payload)

    response = test_client.get('/bookings?client_email=alice@example.com')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['class_name'] == "Booked Class"

def test_invalid_booking_payload(test_client):
    payload = {
        "class_id": 1,
        "client_email": "not-an-email"
    }
    response = test_client.post('/book', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

