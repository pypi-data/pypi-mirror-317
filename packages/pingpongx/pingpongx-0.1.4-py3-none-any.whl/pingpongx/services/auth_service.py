import os
from passlib.context import CryptContext
from pingpongx.models import SignupRequest, LoginRequest
from pingpongx.services.firestore_service import db
import datetime
import jwt
from pingpongx.utils import validate_phone_number, validate_email, get_secret

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = get_secret("JWT_SECRET")
JWT_ALGORITHM = get_secret("JWT_ALGORITHM")


def generate_jwt(username: str):
    """Generate a JWT token with the username."""
    try:
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Token expires in 1 hour
            "iat": datetime.datetime.utcnow()
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    except Exception as e:
        print(e)
        return None


def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def register_user(username: str, password: str):
    """Register a new user."""
    try:
        username = username.strip().lower()
        if "@" in username:
            valid_username = validate_email(username)
        else:
            valid_username = validate_phone_number(username)

        if username == "" or valid_username is None:
            return {"message": "Invalid credentials", "success": False}
        user_ref = db.collection("users").document(username)
        if user_ref.get().exists:
            return {"message": "User already exists", "success": False}

        hashed_password = hash_password(password)
        user_ref.set({
            "username": username,
            "password": hashed_password,
            "created_at": datetime.datetime.utcnow().isoformat()
        })
        return {"message": "User registered successfully", "success": True}
    except Exception as e:
        return {"message": str(e), "success": False}


def login_user(username: str, password: str):
    """Login user by verifying credentials."""
    try:
        username = username.strip().lower()
        if "@" in username:
            valid_username = validate_email(username)
        else:
            valid_username = validate_phone_number(username)

        if username == "" or valid_username is None:
            return {"message": "Username can't be empty", "success": False}

        user_ref = db.collection("users").document(username)
        user_data = user_ref.get()
        if not user_data.exists:
            return {"message": "Invalid credentials", "success": False}

        user_data = user_data.to_dict()
        if not verify_password(password, user_data["password"]):
            return {"message": "Invalid credentials", "success": False}

        token = generate_jwt(username)
        if token:
            return {"message": "Login successful", "username": username, "token": token, "success": True}
        return {"message": "Login failed!", "success": False}
    except Exception as e:
        return {"message": str(e), "success": False}


def signup(request: SignupRequest):
    """Signup API."""
    return register_user(request.username, request.password)


def login(request: LoginRequest):
    """Login API."""
    return login_user(request.username, request.password)


def sender_record(sender: str, channel: str = None):
    try:
        if channel is None or channel not in ["email", "sms"]:
            return {"message": "Invalid channel", "success": False}

        doc_key = sender + "_" + channel
        user_ref = db.collection("sender_record").document(doc_key)
        user_data = user_ref.get()
        count = 1
        current_time = datetime.datetime.utcnow()

        if user_data.exists:
            user_data = user_data.to_dict()
            last_updated = user_data.get("last_updated", None)

            if last_updated:
                last_updated_time = datetime.datetime.fromisoformat(last_updated)
                time_difference = abs(current_time - last_updated_time)
                if time_difference.total_seconds() > 48 * 3600:  # 48 hours in seconds
                    count = 1  # Reset count if more than 48 hours
                else:
                    count = user_data["count"] + 1
            else:
                count = user_data["count"] + 1

            if channel == "email" and count < 5 or channel == "sms" and count < 3:
                user_ref.set({
                    "username": sender,
                    "channel": channel,
                    "count": count,
                    "last_updated": datetime.datetime.utcnow().isoformat() if count == 1 else last_updated
                })
                return {"message": "done", "success": True}
            else:
                return {"message": "unauthorized", "success": False}
        else:
            user_ref.set({
                "username": sender,
                "channel": channel,
                "count": count,
                "last_updated": datetime.datetime.utcnow().isoformat()
            })
            return {"message": "done", "success": True}

    except Exception as e:
        return {"message": str(e), "success": False}


def get_sender_record(sender: str, channel: str = None):
    try:
        if channel is None or channel not in ["email", "sms"]:
            return None

        current_time = datetime.datetime.utcnow()
        doc_key = sender + "_" + channel
        user_ref = db.collection("sender_record").document(doc_key)
        user_data = user_ref.get()
        if user_data.exists:
            user_data = user_data.to_dict()
            last_updated = user_data.get("last_updated", None)

            if last_updated:
                last_updated_time = datetime.datetime.fromisoformat(last_updated)
                time_difference = abs(current_time - last_updated_time)
                if time_difference.total_seconds() > 48 * 3600:  # 48 hours in seconds
                    count = 1   # Reset count if more than 48 hours
                else:
                    count = user_data["count"]
            else:
                count = user_data["count"]
            return count
        return 1

    except Exception as e:
        print("get_sender_record: ", e)
        return None

