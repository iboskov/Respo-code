
"""
This is where all the paths are going to be written. Format is as below
path('/test' views.<name_of_view>, name='<name>'
the login url pattern is an example of how it works. The views.login tells url which function to use in the views.py
file.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('upload', views.upload, name='upload'),
    path("employees", views.employees, name="employees"),
    path('competencies', views.competencies, name='competencies'),
    path('options', views.options, name='options'),
    path('history', views.history, name='history'),
    path('trainings', views.trainings, name='trainings'),
    path('analytics', views.analytics, name='analytics'),
    path('status', views.status, name='status'),
    #API
    path('employees/add', views.employeeAdd, name="add"),
    path('competencies/add', views.competencyAdd, name="competencyAdd"),
    path('trainings/add', views.trainingsAdd, name="trainingsAdd"),
    path('user_history', views.user_history_recent, name='user_history'),
    path('user_history/timeline', views.user_history_timeline, name='user_history/timeline'),
    path('user_competencies', views.user_competencies, name='user_competencies'),
    path('user_options', views.user_options, name='user_options'),
    path('user_trainings', views.user_trainings, name='user_trainings'),
    url('', views.index, name='index'),


]