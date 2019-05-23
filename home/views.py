
"""
This is the views.py file where we will direct html and send objects from backend to the html code from templates
login function atm is just an example of how it should be written.
'html\login' is the location of the html file.
"""

from django.shortcuts import render



# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request,'html/index.html')




def login(request):
    return render(request,'html/login.html')
