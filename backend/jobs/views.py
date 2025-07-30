from django.shortcuts import render
from django.http import HttpResponse

from .models import Job


def jobs(request):
    recentJobs = Job.objects.order_by('-date_scraped')[:100]
    output = '<br>'.join([f'| {job.min_experience} || {job.company.company_name} || {job.title} || {job.job_url} |' for job in recentJobs])
    return HttpResponse(output)