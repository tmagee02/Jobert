from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models.query import QuerySet
from django.db.models import Q, F
from .models import Job


def jobs(request):
    offset = int(request.GET.get('offset', 0))
    jobCount = int(request.GET.get('jobCount', 20))
    companies = request.GET.getlist('companies', [])
    salary = request.GET.get('salary', "")
    salary = None if salary == "" else int(salary)
    experience = request.GET.get('experience', '')
    if experience == '':
        experience = None
    else:
        experience = int(experience)
        if experience < 0:
            experience = None

    thirtyDays = timezone.now() - timedelta(days=60) 
    recentJobs = Job.objects.filter(date_scraped__gte=thirtyDays) 

    recentJobs = filterCompanies(recentJobs, companies)
    recentJobs = filterSalary(recentJobs, salary)
    recentJobs = filterExperience(recentJobs, experience)
    
    totalJobs =  recentJobs.count() 
    recentJobs = recentJobs.order_by('-pk')[offset : offset + jobCount]

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


def filterCompanies(jobs: QuerySet, companies: list[str]):
    if not companies:
        return jobs
    
    return jobs.filter(company__company_name__in=companies)


def filterSalary(jobs: QuerySet, salary: int):
    if salary == None:
        return jobs

    return jobs.filter(
        Q(max_salary__gte=salary) | Q(max_salary=-1) | Q(max_salary__isnull=True)
    )


def filterExperience(jobs: QuerySet, experience: int):
    if experience == None:
        return jobs
        
    return jobs.filter(
        Q(max_experience=-1) | Q(max_experience__isnull=True) |
        #range
        (Q(min_experience__lt=F('max_experience')) & Q(min_experience__lte=experience) & Q(max_experience__gte=experience)) |
        #min == max -> 3+
        (Q(min_experience=F('max_experience')) & Q(min_experience__lte=experience))
    ) 