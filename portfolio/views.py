from typing import Sequence

from rest_framework import (status,
                            views,
                            permissions,
                            throttling,
                            viewsets)
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Project
from .serializers import ContactMessageSerializer, ProjectSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class ContactRateThrottle(throttling.AnonRateThrottle):
    rate = "5/hour"  # limits each ip to 5 submissions per hour


class ContactApiView(views.APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ContactRateThrottle]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():
            contact = serializer.save()

            subject = (contact.subject or "New Message").replace("\n", " ").replace("\r", " ")

            email = EmailMessage(
                subject=f"Portfolio Inquiry:{subject}",
                body=f"From: {contact.name} ({contact.email}\n\n{contact.message})",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[contact.email]
            )

            try:
                email.send()
            except:
                import logging
                logging.getLogger(__name__).exception("Contact email failed to send")

            return Response(
                {"detail": "Message sent successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('tag', 'project_images', 'project_videos').all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
