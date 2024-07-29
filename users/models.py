# users/models.py
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # avatar = CloudinaryField('avatar', blank=True, null=True)
    # avatar = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def upload_avatar(self, file):
        result = cloudinary.uploader.upload(file)
        self.avatar = result['public_id']
        self.save()

    def delete_avatar(self):
        if self.avatar:
            cloudinary.uploader.destroy(self.avatar.public_id)
            self.avatar = None
            self.save()

# For testing model validation
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10mb


def file_validation(file):
    if not file:
        raise ValidationError("No file selected.")

    # For regular upload, we get UploadedFile instance, so we can validate it.
    # When using direct upload from the browser, here we get an instance of the CloudinaryResource
    # and file is already uploaded to Cloudinary.
    # Still can perform all kinds on validations and maybe delete file, approve moderation, perform analysis, etc.
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 10MB.")