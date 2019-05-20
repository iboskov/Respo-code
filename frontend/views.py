from django.shortcuts import render


"""
This is the views.py file where we will direct html/css/javascript code from templates
"""


# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")