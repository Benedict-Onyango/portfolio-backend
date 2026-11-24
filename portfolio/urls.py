from django.urls import path,include
from .views import ContactApiView,ProjectsViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register(r'projects',ProjectsViewSet,basename='projects')

urlpatterns = [
    path('contact/', ContactApiView.as_view(), name='api-contact'),
    path('',include(router.urls)),
]

