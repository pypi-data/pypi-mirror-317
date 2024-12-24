from pingpongx.services.notification import PingPong
from pingpongx.services.user_preferences import UserPreferences
from google.cloud import firestore, secretmanager
import json
import os
import tempfile

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


def get_db():
    try:
        db_client = secretmanager.SecretManagerServiceClient()
        db_secret_name_path = f"projects/{PROJECT_ID}/secrets/FIREBASE_CREDENTIALS/versions/latest"
        db_response = db_client.access_secret_version(name=db_secret_name_path)
        db_secret_data = db_response.payload.data.decode('UTF-8')
        db_secret_json = json.loads(db_secret_data)
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            json.dump(db_secret_json, temp_file, indent=4)
            temp_file_path = temp_file.name

        _db = firestore.Client.from_service_account_json(temp_file_path)
        return _db
    except Exception as e:
        print(f"Error getting DB: {e}")
        return None


db = get_db()
if db is None:
    print("No firestore DB found")
else:
    print("Firestore DB found")