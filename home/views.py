
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
    return render(request, 'html/index.html', {"user": user})


def login(request):
    title = "Login"
    return render(request, 'html/login.html', {"title": title})


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
    main_pick = 'employee'
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


def options(request):
    user = "admin"
    main_pick = 'options'
    return render(request, 'html/options.html', {"main_pick": main_pick, "user":user})


def history(request):
    user = "admin"
    main_pick = "history"
    return render(request, 'html/history.html', {"main_pick": main_pick, "user": user})


def trainings(request):
    user = "admin"
    picked = "add"
    main_pick = "trainings"
    return render(request, 'html/trainings.html', {"picked": picked, "main_pick": main_pick, "user": user})


def trainings_training(request):
    user = "admin"
    picked = "trainings"
    main_pick = "trainings"
    return render(request, 'html/trainings.html', {"picked": picked, "main_pick": main_pick, "user": user})


def status(request):
    user = "admin"
    main_pick = "status"
    return render(request, 'html/status.html', {"main_pick": main_pick, "user": user})


# user views
def user_history_recent(request):
    user = "user"
    main_pick = "user_history"
    picked = "recent"
    return render(request, 'html/user/history.html', {"main_pick": main_pick, "user": user, "picked": picked})


def user_history_timeline(request):
    user = "user"
    main_pick = "user_history"
    picked = "timeline"
    return render(request, 'html/user/history.html', {"main_pick": main_pick, "user": user, "picked": picked})


def competencies(request):
    user = "user"
    main_pick = "competencies"
    return render(request, 'html/user/competencies.html', {"main_pick": main_pick, "user": user})


def user_options(request):
    user = "user"
    main_pick = "user_options"
    return render(request, 'html/user/user_options.html', {"main_pick": main_pick, "user": user})


def seminars(request):
    user = "user"
    main_pick = "seminars"
    return render(request, 'html/user/seminars.html', {"main_pick": main_pick, "user": user})

