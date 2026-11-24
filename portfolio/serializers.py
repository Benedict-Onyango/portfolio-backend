from rest_framework import serializers
from .models import ContactMessage, Skill, Project, ProjectImage, ProjectVideo


class ContactMessageSerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message", "website"]

    def validate_website(self, value):
        if value:
            raise serializers.ValidationError("Spam detected")
        return value

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'image_alt']


class ProjectVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVideo
        fields = ['id', 'video', 'caption']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model=Skill
        fields=['id','tag']

class ProjectSerializer(serializers.ModelSerializer):
    tag=SkillSerializer(many=True, read_only=True)
    project_images = ProjectImageSerializer(many=True, read_only=True)
    project_videos = ProjectVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'badge',
            'description',
            'tag',
            'github',
            'demo',
            'project_images',
            'project_videos',
        ]
