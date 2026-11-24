from django.urls import path
from .views import ContactApiView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('contact/', ContactApiView.as_view(), name='api-contact'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)