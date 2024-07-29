# utils.py
from django.conf import settings
import stream_chat
from .config import STREAM_API_KEY, STREAM_API_SECRET

def generate_stream_token(user_id):
    client = stream_chat.StreamChat(
        api_key=STREAM_API_KEY,
        api_secret=STREAM_API_SECRET
    )
    token = client.create_token(str(user_id))
    return token