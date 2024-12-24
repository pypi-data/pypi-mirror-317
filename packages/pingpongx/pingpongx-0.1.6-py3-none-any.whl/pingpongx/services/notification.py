from fastapi import Request
from pingpongx.services.auth_middleware import require_auth
from pingpongx.services.auth_service import get_sender_record, sender_record
from pingpongx.services.kafka_consumer import consume_notifications
from pingpongx.services.redis_service import add_to_queue
from pingpongx.services.kafka_producer import send_event
from pingpongx.services.firestore_service import save_notification_log, get_user_preferences, update_user_preferences
from pingpongx.services.user_preferences import UserPreferences
from pingpongx.utils import generate_notification_id, get_secret
from pingpongx.utils import validate_phone_number, validate_email
import time
import os

MAILGUN_EMAIL = get_secret("MAILGUN_EMAIL")
MAILGUN_API_KEY = get_secret("MAILGUN_API_KEY")
MAILGUN_DOMAIN = get_secret("MAILGUN_DOMAIN")
TWILIO_ACCOUNT_SID = get_secret("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = get_secret("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = get_secret("TWILIO_PHONE_NUMBER")


class PingPong:
    """PingPong notification service."""

    def __init__(self, sender=None, receiver=None, message="", channels=None, mailgun_api_key=None, mailgun_domain=None, mailgun_email=None, twilio_account_sid=None, twilio_auth_token=None, twilio_phone_number=None, trail_account=False):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.channels = channels
        self.mailgun_api_key = mailgun_api_key
        self.mailgun_domain = mailgun_domain
        self.mailgun_email = mailgun_email
        self.twilio_account_sid = twilio_account_sid
        self.twilio_phone_number = twilio_phone_number
        self.twilio_auth_token = twilio_auth_token
        self.trail_account = trail_account

    async def send_notification(self):
        try:

            user_id = self.receiver
            username = self.sender
            message = self.message
            channel_list = self.channels
            trail_account = self.trail_account
            message_sent_for_channel = []
            email_api_key = None
            email_domain = None
            sample_email = None
            sms_auth_token = None
            sms_account_id = None
            sample_phone_number = None

            if not username or username.strip() == "":
                return {"success": False, "message": f"Please login and try again."}

            if user_id == "" or user_id is None or username is None or channel_list is None or message == "" or len(channel_list) < 1 or user_id.strip() == "" or message.strip() == "":
                return {"success": False, "message": f"Invalid user_id or message: {user_id} and {message}"}

            username = username.strip().lower()
            user_id = user_id.strip().lower()
            message = message.strip()

            if username == user_id:
                return {"success": False, "message": f"You can't send notification to yourself!"}

            for i in channel_list:
                if i not in ["email", "sms"]:
                    return {"success": False, "message": f"Invalid channel: {i}. Choose from ['email', 'sms']"}

                if i == "email" and validate_email(user_id) is False:
                    return {"success": False, "message": f"Invalid email address: {user_id} as user_id"}

                if i == "sms" and validate_phone_number(user_id) is False:
                    return {"success": False, "message": f"Invalid phone number: {user_id} as user_id"}

                if i == "email" and (self.mailgun_email is None or self.mailgun_domain is None or self.mailgun_email is None) and trail_account is False:
                    return {"success": False, "message": f"Invalid or missing Mailgun credentials."}

                if i == "sms" and (self.twilio_auth_token is None or self.twilio_phone_number is None or self.twilio_account_sid is None) and trail_account is False:
                    return {"success": False, "message": f"Invalid or missing Twilio credentials."}

            if trail_account is False:
                if "email" in channel_list:
                    email_api_key = self.mailgun_api_key
                    email_domain = self.mailgun_domain
                    sample_email = self.mailgun_email
                if "sms" in channel_list:
                    sms_auth_token = self.twilio_auth_token
                    sms_account_id = self.twilio_account_sid
                    sample_phone_number = self.twilio_phone_number
            else:
                if "email" in channel_list:
                    email_api_key = MAILGUN_API_KEY
                    email_domain = MAILGUN_DOMAIN
                    sample_email = MAILGUN_EMAIL
                if "sms" in channel_list:
                    sms_auth_token = TWILIO_AUTH_TOKEN
                    sms_account_id = TWILIO_ACCOUNT_SID
                    sample_phone_number = TWILIO_PHONE_NUMBER

            for channel in channel_list:
                if trail_account:
                    check_sender_record = get_sender_record(username, channel)
                    if check_sender_record is None:
                        return {"success": False, "message": f"Notification failed due to not getting trail account"}
                    if channel == "email" and check_sender_record > 2 or channel == "sms" and check_sender_record > 1:
                        return {"success": False, "message": f"Trail account subscription ended"}
                publish = await publish_notification(user_id=user_id, message=message, channel=channel, username=username)
                if publish.get("success") is True:
                    consume = await consume_notifications(receiver=user_id, sender=username, mailgun_api_key=email_api_key, mailgun_domain=email_domain, mailgun_email=sample_email, twilio_account_sid=sms_account_id, twilio_auth_token=sms_auth_token, twilio_phone_number=sample_phone_number)
                    if consume.get("success") is True:
                        message_sent_for_channel.append(channel)
                        sender_record(username, channel)

            if message_sent_for_channel and len(message_sent_for_channel) > 0:
                return {"success": True, "message": f"Notification sent to {user_id}."}
            return {"success": False, "message": f"Notification failed to {user_id}."}
        except Exception as e:
            return {"success": False, "message": f"Notification failed due to :{e}"}


@require_auth
async def notify(request: Request, data: dict = None, username: str = None):
    """api method to send notifications"""
    try:
        sender = username
        if data is None:
            return {"success": False, "message": f"Please login and try again with valid payload."}

        receiver = data.get("user_id", "")
        message = data.get("message", "")
        channel_list = data.get("channel", [])
        service = PingPong(sender=sender, receiver=receiver, message=message, channels=channel_list, trail_account=True)
        response = await service.send_notification()
        return response
    except Exception as e:
        return {"success": False, "message": f"Notification failed due to :{e}"}


async def publish_notification(user_id: str, message: str, channel: str, username: str):
    """Send a notification to a user via the specified channel."""

    try:
        user_preferences = await get_user_preferences(user_id)
        if not user_preferences:
            await update_user_preferences(user_id, {"email": True, "sms": True})

        preferences = user_preferences.get("preferences", {})
        if not preferences.get(channel, False):
            return {"success": False, "message": f"User {user_id} hasn't opted for {channel} notifications."}

        notification_data = {"user_id": user_id, "message": message, "channel": channel, "sent_by": username, "timestamp": time.time()}
        redis_status = await add_to_queue(user_id, notification_data)
        if redis_status:
            kafka_status = await send_event(user_id, f"Notification sent to {user_id} via {channel}")
            if kafka_status:
                await save_notification_log(user_id, {"id": generate_notification_id(), "message": message,"sent_by": username, "channel": channel})
                return {"success": True, "message": f"Notification queued successfully for channel: {channel}"}

        return {"success": False, "message": "Notification queued failed"}
    except Exception as e:
        return {"success": False, "message": f"Notification queued failed due to :{e}"}

