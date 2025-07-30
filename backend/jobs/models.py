from django.db import models

class Company(models.Model):
    company_name = models.TextField()
    base_url = models.TextField(unique=True)
    search_path = models.TextField()
    search_query = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Company'



class Job(models.Model):
    job_url = models.TextField(unique=True)
    title = models.TextField()
    job_desc = models.TextField()
    min_experience = models.IntegerField(blank=True, null=True)
    max_experience = models.IntegerField(blank=True, null=True)
    date_scraped = models.DateTimeField(blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING)
    date_posted = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Job'


class Joblocation(models.Model):
    job = models.ForeignKey(Job, models.DO_NOTHING, db_column='job_id')
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location_id')

    class Meta:
        managed = False
        db_table = 'JobLocation'
        unique_together = (('job', 'location'),)


class Location(models.Model):
    location_name = models.TextField()
    is_remote = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Location'