import django_filters
from job.models import JobPost


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = JobPost
        fields = ['title', 'industry', 'job_type', 'city']
