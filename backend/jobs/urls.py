from django.urls import path

from . import views

urlpatterns = [
        path('', views.jobs, name='jobs'),
        path('<int:jobId>/', views.jobInfo, name='jobInfo')
]