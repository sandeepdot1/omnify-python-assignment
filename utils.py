import re
from datetime import datetime
import pytz
from email.utils import parseaddr
from flask import jsonify
from db import get_db_connection


def format_datetime_for_display(utc_datetime_str, timezone_str='Asia/Kolkata'):
    """
    Convert UTC/IST datetime string to a formatted string in the given timezone.
    E.g., '2025-06-10 09:00 AM IST'
    """
    try:
        # Parse the datetime string (assuming it's stored as IST in DB)
        utc_dt = datetime.strptime(utc_datetime_str, "%Y-%m-%d %H:%M:%S")
        
        # Assume stored in IST
        ist = pytz.timezone("Asia/Kolkata")
        ist_dt = ist.localize(utc_dt)

        # Convert to target timezone
        target_tz = pytz.timezone(timezone_str)
        converted_dt = ist_dt.astimezone(target_tz)

        # Format with AM/PM and timezone info
        return converted_dt.strftime("%Y-%m-%d %I:%M %p %Z")
    except Exception as e:
        return utc_datetime_str  # Fallback to original if error

def validate_email(email):
    return '@' in parseaddr(email)[1]

def query_db(query, args=(), one=False):
    with get_db_connection() as conn:
        cur = conn.execute(query, args)
        result = cur.fetchall()
        cur.close()
    return (result[0] if result else None) if one else result

def modify_db(query, args=()):
    with get_db_connection() as conn:
        cur = conn.execute(query, args)
        conn.commit()
        cur.close()

def error_response(message, code=400):
    return jsonify({"error": message}), code
