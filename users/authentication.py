# users/authentication.py
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, timezone

User = get_user_model()

def generate_token(user):
    payload = {
        'user_id': user.pk,  # Ensure this key matches what you're looking for
        'exp': datetime.now(timezone.utc) + timedelta(days=7),  # Use timezone-aware datetime
        'iat': datetime.now(timezone.utc),  # Use timezone-aware datetime
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
