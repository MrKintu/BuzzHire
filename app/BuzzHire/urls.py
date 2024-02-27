"""
URL configuration for BuzzHire project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("accounts/", include("users.urls")),
    path("", include("dashboard.urls")),
    path("company/", include("company.urls")),
    path("resume/", include("resume.urls")),
    path("jobs/", include("job.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
