import re
from datetime import datetime

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def is_strong_password(password):
    # At least 8 characters, one uppercase, one lowercase, one number, and one special character
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

def is_valid_mobile(mobile):
    # Indian mobile numbers (10 digits)
    pattern = r"^[6-9]\d{9}$"
    return bool(re.match(pattern, mobile))

def is_18(dob):
    today = datetime.today()
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age >= 18
