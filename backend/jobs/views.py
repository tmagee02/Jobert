from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Job


def jobs(request):
    recentJobs = Job.objects.order_by('-date_scraped')[:30]
    jobList = []
    for job in recentJobs:
        jobDetails = {
            #Probably should add dates or requirements or salary or something
            'JobId' : job.pk,
            'JobUrl' : job.job_url,
            'Company' : job.company.company_name,
            'Title' : job.title
        }
        jobList.append(jobDetails)

    return JsonResponse(jobList, safe=False)

def jobInfo(request, jobId):
    #need: Company Logo?, Company name, title, locations, minExperience, max experience, date posted, date scraped, job desc
    job = get_object_or_404(Job, pk=jobId)
    jobInfo = {
        'Company' : job.company.company_name,
        'JobUrl' : job.job_url,
        'Title' : job.title,
        #'Locations' : job.locations
        # 'MinExperience' : job.min_experience,
        # 'MaxExperience' : job.max_experience,
        # 'DatePosted' : job.date_posted,
        'DateScraped' : job.date_scraped,
        'JobDesc' : job.job_desc
    }

    return JsonResponse(jobInfo)