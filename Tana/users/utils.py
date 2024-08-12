import jwt
from datetime import datetime, timedelta

def generate_token(user_id, secret_key, expiration_minutes=30):
    expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    payload = {
        "user_id": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def validate_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

def hash_password(password):
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)
