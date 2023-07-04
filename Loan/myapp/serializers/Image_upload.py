import re
from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        if isinstance(data, str):
            if "data:" in data and ";base64," in data:
                header, data = data.split(";base64,")

            # Add padding if necessary
            padding = len(data) % 4
            if padding != 0:
                data += "=" * (4 - padding)

            # Validate and return the base64 data as the field value
            return data

        return super().to_internal_value(data)
