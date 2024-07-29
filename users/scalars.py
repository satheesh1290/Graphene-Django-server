from graphene.types import Scalar
from graphene_django.converter import convert_django_field
from cloudinary.models import CloudinaryField

class CloudinaryImage(Scalar):
    @staticmethod
    def serialize(cloudinary_image):
        return cloudinary_image.url if cloudinary_image else None

@convert_django_field.register(CloudinaryField)
def convert_cloudinary_field(field, registry=None):
    return CloudinaryImage(description=field.help_text, required=not field.null)