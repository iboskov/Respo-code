
"""
This is where all the paths are going to be written. Format is as below
path('/test' views.<name_of_view>, name='<name>'
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]