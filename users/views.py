from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import get_user_model
from .decorators import jwt_login_required
import cloudinary.uploader
import cloudinary.api
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()


# Endpoint to get CSRF token (for client-side usage)
@csrf_exempt
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


# File upload view with JWT authentication
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(jwt_login_required, name='dispatch')
class FileUploadView(View):
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']

            # Ensure that the uploaded file is an image
            if not uploaded_file.content_type.startswith('image/'):
                return JsonResponse({'error': 'Only image files are allowed'}, status=400)
            
            # # Save the uploaded file using Django’s default storage system
            # file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
            # file_url = default_storage.url(file_name)

            # Upload file to Cloudinary
            try:
                result = cloudinary.uploader.upload(uploaded_file,
                                                    folder="chatApp/",
                                                    public_id=f"{request.user.username}_avatar",
                                                    overwrite=True,
                                                    resource_type="image")
                avatar_url = result['secure_url'].rstrip('/')
            
                # Assign the URL directly to the user object
                user = request.user
                user.avatar = avatar_url  # Store it directly
                user.save()
                return JsonResponse({'avatarUrl': avatar_url}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        return JsonResponse({'error': 'No file uploaded'}, status=400)

# Test view for checking POST request
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(jwt_login_required, name='dispatch')
class TestView(View):
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        
        return HttpResponse("POST request received!")


