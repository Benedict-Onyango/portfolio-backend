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
    model = ProjectVideo
    fields = ['id', 'video', 'caption']


class ProjectSerializer(serializers.ModelSerializer):
    project_images = ProjectImageSerializer(many=True, read_only=True)
    project_videos = ProjectVideoSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    uploaded_videos = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=True
    )

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
            'project_images', 'project_videos',
            'uploaded_images', 'uploaded_videos'
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        uploaded_videos = validated_data.pop('uploaded_videos', [])
        tags= validated_data.pop('tag',[])

        project=Project.objects.create(**validated_data)
        project.tag.set(tags)

        for img in uploaded_images:
            ProjectImage.objects.create(project=project,image=img,image_alt=f"image of {project.title}")

        for vid in uploaded_videos:
            ProjectVideo.objects.create(project=project,video=vid,caption=f"Overview of {project.title}")
        return project