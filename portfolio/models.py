from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ———> {self.email}"

class Skill(models.Model):
    tag=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.tag}"

class Project(models.Model):
    title = models.CharField(max_length=100)
    badge = models.CharField(max_length=50)
    description = models.TextField()
    tag=models.ManyToManyField(Skill, related_name="used_skills", blank=True)
    github = models.URLField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_images")
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)
    image_alt=models.CharField(max_length=100)

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_videos")
    video = models.FileField(
        upload_to="project_videos/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'mov'])]
    )
    caption = models.CharField(max_length=100, blank=True)
