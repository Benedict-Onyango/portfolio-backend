from typing import Any

from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False,allow_blank=True,write_only=True)

    class Meta:
        model=ContactMessage
        fields=["name","email","subject","message","website"]

    def validate_website(self,value):
        if value:
            raise serializers.ValidationError("Spam detected")
        return value

    def create(self,validated_data):
        validated_data.pop("website",None)
        return super().create(validated_data)