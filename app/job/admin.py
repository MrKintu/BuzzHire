from django.contrib import admin
from .models import JobPost, Job_Industry, ApplyJob


admin.site.register(JobPost)
admin.site.register(ApplyJob)
admin.site.register(Job_Industry)
