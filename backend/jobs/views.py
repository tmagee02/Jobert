from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from django.utils import timezone

from .models import Job


def jobs(request):
    offset = int(request.GET.get('offset', 0))
    jobCount = int(request.GET.get('jobCount', 20))
    thirtyDays = timezone.now() - timedelta(days=30) #CHANGE
    totalJobs = Job.objects.filter(date_scraped__gte=thirtyDays).count() 
    recentJobs = Job.objects.filter(date_scraped__gte=thirtyDays).order_by('-pk')[offset : offset + jobCount] 
    jobList = []
    for job in recentJobs:
        jobDetails = {
            #Probably should add dates or requirements or salary or something
            'JobId' : job.pk,
            'JobUrl' : job.job_url,
            'Company' : job.company.company_name,
            'Title' : job.title,
            'MinExperience' : job.min_experience,
            'MaxExperience' : job.max_experience,
            'MinSalary' : job.min_salary,
            'MaxSalary' : job.max_salary,
            'DateScraped' : job.date_scraped,
        }
        jobList.append(jobDetails)

    return JsonResponse({'jobList': jobList, 'totalJobs': totalJobs}, safe=False)

def jobInfo(request, jobId):
    #need: Company Logo?, Company name, title, locations, minExperience, max experience, date posted, date scraped, job desc
    job = get_object_or_404(Job, pk=jobId)
    jobInfo = {
        'Company' : job.company.company_name,
        'JobUrl' : job.job_url,
        'Title' : job.title,
        #'Locations' : job.locations
        'MinExperience' : job.min_experience,
        'MaxExperience' : job.max_experience,
        # 'DatePosted' : job.date_posted,
        'DateScraped' : job.date_scraped,
        'JobDesc' : job.job_desc,
        'MinSalary' : job.min_salary,
        'MaxSalary' : job.max_salary
    }

    return JsonResponse(jobInfo)