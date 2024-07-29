# users/decorators.py
from django.http import JsonResponse
from django.conf import settings
import jwt
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_user_by_token

User = get_user_model()

def jwt_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            try:
                token = token.replace('Bearer ', '')
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                print(f"JWT Payload: {payload}")  # Debugging: Print payload to check its structure
                user_id = payload.get('user_id')  # Use get() to avoid KeyError
                # user_id = get_user_by_token(token)
                
                if user_id:
                    request.user = User.objects.get(pk=user_id)
                else:
                    return JsonResponse({'error': 'User ID not found in token'}, status=401)
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist) as e:
                print(f"JWT Error: {str(e)}")  # Debugging: Print error message
                return JsonResponse({'error': 'Invalid token or user not found'}, status=401)
        else:
            return JsonResponse({'error': 'Token required'}, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
