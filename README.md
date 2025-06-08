# Simple Booking API

This is a Flask-based REST API that allows clients to:
- View available fitness classes
- Book a class
- Retrieve their bookings

The app includes timezone support and unit tests with a separate test database.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sandeepdot1/omnify-python-assignment.git
cd omnify-python-assignment
```

### 2. Create a Virtual Environment and Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Seed the database

```bash
python seed_data.py
```

### 4. Run the App

```bash
python app.py
```

### Running Tests

```bash
pytest test_app.py -v
```

---

## API Endpoints

#### 1. GET /classes
Returns a list of upcoming fitness classes.

Optional Query Parameters:
tz (string): Timezone for formatting scheduled times (default is Asia/Kolkata)

GET /classes?tz=America/New_York

curl
```
curl -X GET "http://localhost:5000/classes?tz=Asia/Kolkata" -H "Content-Type: application/json"
```

#### 2. POST /book
Books a slot in a fitness class.

```bash
POST /book
```

Request Body:
```bash
{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
```

curl
```bash
curl -X POST http://localhost:5000/book \
  -H "Content-Type: application/json" \
  -d '{
        "class_id": 1,
        "client_name": "Jane Doe",
        "client_email": "jane.doe@example.com"
      }'
```

#### 3. GET /bookings
Retrieves all bookings for a given client email.

Query Parameters:
client_email (required)
tz (optional): Format datetime in the requested timezone.

```bash
GET /bookings?client_email=john@example.com&tz=Europe/London
```

curl
```bash
curl -X GET "http://localhost:5000/bookings?client_email=jane.doe@example.com&tz=UTC" \
  -H "Content-Type: application/json"
```

### Timezone Suppport

This API supports the [IANA Time Zone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) format.

Common Timezones
| Timezone             | Description                     | Example Usage in API                                |
|----------------------|----------------------------------|------------------------------------------------------|
| Asia/Kolkata         | Indian Standard Time             | `tz=Asia/Kolkata`                          |
| UTC                  | Coordinated Universal Time       | `tz=UTC`                                   |
| America/New_York     | Eastern Time (US & Canada)       | `tz=America/New_York`                      |
| Europe/London        | Greenwich Mean Time              | `tz=Europe/London`                         |
| Asia/Tokyo           | Japan Standard Time              | `tz=Asia/Tokyo`                            |
| Australia/Sydney     | Australian Eastern Daylight Time | `tz=Australia/Sydney`                      |
| America/Los_Angeles  | Pacific Time (US & Canada)       | `tz=America/Los_Angeles`                   |
| Europe/Berlin        | Central European Time            | `tz=Europe/Berlin`                         |
| Asia/Dubai           | Gulf Standard Time               | `tz=Asia/Dubai`                            |

If tz is not provided or invalid, the server defaults to Asia/Kolkata.
