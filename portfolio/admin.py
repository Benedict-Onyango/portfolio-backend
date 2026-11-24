from django.contrib import admin
from .models import  Skills,Projects,ProjectImage,ProjectVideo

# Register your models here.

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectVideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 1


@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline,ProjectVideoInline]

admin.register(Skills)
