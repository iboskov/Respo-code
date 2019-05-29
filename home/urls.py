
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
    url('login', views.login, name='login'),
    url('upload', views.upload, name='upload'),
    path("employee", views.employee_add, name="employee"),
    path("employee/employees", views.employee_employees,name="employee/employees"),
    path('employee/history', views.employee_history,name='employee/history'),
    path('competence/add', views.competence_add, name='competence/add'),
    path('competence/competencies', views.competence_competencies, name='competencies'),
    path('options', views.options, name='options'),
    path('history', views.history, name='history'),
    path('trainings', views.trainings, name='trainings'),
    path('trainings/training', views.trainings_training, name='training'),
    path('status', views.status, name='status'),
    path('history', views.history, name='history'),
    path('competencies', views.history, name='competencies'),
    path('useroptions', views.history, name='useroptions'),
    path('seminars', views.history, name='seminars'),
    url('', views.index, name='index'),

]