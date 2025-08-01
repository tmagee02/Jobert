from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Job


def jobs(request):
    recentJobs = Job.objects.order_by('-date_scraped')[:20]
    output = '<br>'.join([f'| {job.min_experience} || {job.company.company_name} || {job.title} || {job.job_url} |' for job in recentJobs])
    return HttpResponse(output)

def jobInfo(request, jobId):
    job = get_object_or_404(Job, pk=jobId)
    info = []
    info.append('Company Logo')
    info.append(job.company.company_name)
    info.append(job.title)
    info.append('job.locations')
    info.append(f'job.min_experience -- job.max_experience')
    info.append('job.date_posted')
    info.append(str(job.date_scraped))
    info.append(job.job_desc)
    output = '<br>'.join(info)

    return HttpResponse(output)