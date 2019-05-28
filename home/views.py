
"""
This is the views.py file where we will direct html and send objects from backend to the html code from templates
login function atm is just an example of how it should be written.
'html\login' is the location of the html file.
"""

from django.shortcuts import render



# Create your views here.
from django.http import HttpResponse


def index(request):
    user = "admin"
    return render(request,'html/index.html',{"user": user})




def login(request):
    return render(request,'html/login.html')

def upload(request):
    user = "admin"
    main_pick = "upload"
    return render(request,'html/upload.html',{"main_pick":main_pick, "user":user})

def employee_add(request):
    picked = 'add'
    user = "admin"
    main_pick = "employee"
    return render(request,'html/employee.html',{"picked": picked,"main_pick": main_pick, "user":user})

def employee_employees(request):
    user = "admin"
    picked = 'employee'
    main_pick='employee'
    return render(request, 'html/employee.html', {"picked": picked, "main_pick": main_pick, "user":user})

def employee_history(request):
    picked = 'history'
    main_pick='employee'
    user = "admin"
    return render(request, 'html/employee.html', {"picked": picked, "main_pick": main_pick, "user":user})

def competence_add(request):
    user = "admin"
    picked = 'add'
    main_pick = 'competencies'
    return render(request, 'html/competencies.html', {"picked": picked, "main_pick": main_pick, "user":user})

def competence_competencies(request):
    user = "admin"
    picked = 'competence'
    main_pick = 'competencies'
    return render(request,'html/competencies.html', {"picked": picked, "main_pick": main_pick, "user":user})