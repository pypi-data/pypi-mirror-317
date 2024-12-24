from google.cloud import firestore, secretmanager
import json
import requests
import os
import uuid
import re

ONESIGNAL_APP_ID = os.getenv('ONESIGNAL_APP_ID', "")
PROJECT_ID = os.getenv('PROJECT_ID', "424159745652")
ENV = os.environ.get("ENV", "prod")
ENV_VALS = {}

try:
    print("Attempting to load environment variables")
    client = secretmanager.SecretManagerServiceClient()
    secret_name_path = f"projects/{PROJECT_ID}/secrets/ENV_FILE/versions/latest"
    response = client.access_secret_version(name=secret_name_path)
    secret_data = response.payload.data.decode('UTF-8')
    secret_json = json.loads(secret_data)
    if secret_json and len(secret_json) > 0:
        ENV_VALS = secret_json
        print("Loaded environment variables")
    else:
        print("No environment variables loaded")
except Exception as e:
    print(f"ERROR while getting secret: {e}")


def generate_device_token():
    try:
        url = "https://onesignal.com/api/v1/players"

        payload = {
            "device_type": 5,
            "language": "en",
            "timezone": "-28800",
            "game_version": "1.1.1",
            "device_model": "iPhone5,1",
            "device_os": "15.1.1",
            "session_count": 600,
            "tags": {
                "first_name": "Jon",
                "last_name": "Smith",
                "level": "99",
                "amount_spent": "6000",
                "account_type": "VIP"
            },
            "amount_spent": "100.99",
            "playtime": 600,
            "notification_types": 1,
            "lat": 37.563,
            "long": 122.3255,
            "country": "US",
            "timezone_id": "Asia/Kolkata",
            "app_id": ONESIGNAL_APP_ID
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(e)


def generate_notification_id():
    return str(uuid.uuid4())


def validate_email(email):
    """Validates an email address using a regular expression."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def validate_phone_number(phone_number):
    """Validates a phone number."""
    phone_regex = r"^\+(?:[0-9] ?){6,14}[0-9]$"
    return re.match(phone_regex, phone_number) is not None


def sanitize_topic_name(topic_name):
    # Replace "@" with "-" to make the topic name valid
    sanitized_topic_name = topic_name.replace('@', '-')
    return sanitized_topic_name


def get_db_via_firebase_credentials():
    try:
        if ENV == "dev":
            return firestore.Client.from_service_account_json("firebase_credentials.json")
        elif ENV == "gcp":
            client = secretmanager.SecretManagerServiceClient()
            secret_name_path = f"projects/{PROJECT_ID}/secrets/ENV_FILE/versions/latest"
            response = client.access_secret_version(name=secret_name_path)
            secret_data = response.payload.data.decode('UTF-8')
            secret_json = json.loads(secret_data)
            return secret_json
        else:
            client = firestore.Client()
            return client
    except Exception as e:
        print(f"Error getting firebase credentials: {e}")
        return None


def get_env_secret(secret_name, version="latest"):
    client = secretmanager.SecretManagerServiceClient()
    secret_name_path = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/{version}"
    response = client.access_secret_version(name=secret_name_path)
    return response.payload.data.decode('UTF-8')


def get_secret(key):
    try:
        return ENV_VALS.get(key)
    except Exception as e:
        print(f"Error getting ENV_FILE secrets: {e}")
        return None

