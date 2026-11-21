from django.urls import path
from .views import ContactApiView

urlpatterns = [
    path('contact/', ContactApiView.as_view(), name='api-contact'),
]