from django.urls import path,include
from .views import ContactApiView,ProjectsViewSet
from django.conf import settings
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register(r'projects',ProjectsViewSet,basename='projects')

urlpatterns = [
    path('contact/', ContactApiView.as_view(), name='api-contact'),
    path('',include(router.urls)),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)