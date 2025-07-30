from django.contrib import admin

# Register your models here.
from .models import Company, Job, Joblocation, Location

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Joblocation)
admin.site.register(Location)