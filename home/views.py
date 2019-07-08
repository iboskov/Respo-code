
"""
This is the views.py file where we will direct html and send objects from backend to the html code from templates
login function atm is just an example of how it should be written.
'html\login' is the location of the html file.
"""

from django.shortcuts import render
from home.API import *


# Create your views here.
from django.http import HttpResponse


def index(request):
    user = "admin"
    return render(request, 'html/index.html', {"user": user})


def login(request):
    title = "Login"
    return render(request, 'html/login.html', {"title": title})

# region admin_views


def upload(request):
    user = "admin"
    main_pick = "upload"
    return render(request, 'html/admin/upload.html', {"main_pick": main_pick, "user": user})


def employees(request):
    user = "admin"
    main_pick = "employees"
    employees = getEmployees()
    return render(request, 'html/admin/employees.html', {"main_pick": main_pick, "user": user,"employees":employees})


def competencies(request):
    user = "admin"
    main_pick = 'competencies'
    competency = getCompetencies()
    competency_type = getCompetencies_type()
    return render(request, 'html/admin/competencies.html',
                  {"main_pick": main_pick, "user": user, "competency": competency, "competency_type": competency_type})


def options(request):
    user = "admin"
    main_pick = 'options'
    return render(request, 'html/admin/options.html', {"main_pick": main_pick, "user": user})


def history(request):
    user = "admin"
    main_pick = "history"
    return render(request, 'html/admin/history.html', {"main_pick": main_pick, "user": user})


def trainings(request):
    user = "admin"
    main_pick = "trainings"
    competency = getCompetencies()
    trainings = getTrainings()
    return render(request, 'html/admin/trainings.html', {"main_pick": main_pick, "user": user,"competency":competency,"trainings":trainings})

def analytics(request):
    user = "admin"
    main_pick = "analytics"
    return render(request, 'html/admin/analytics.html', {"main_pick": main_pick, "user": user})


def status(request):
    user = "admin"
    main_pick = "status"
    return render(request, 'html/admin/status.html', {"main_pick": main_pick, "user": user})
# endregion

# region user_views


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


def user_competencies(request):
    user = "user"
    main_pick = "user_competencies"
    return render(request, 'html/user/competencies.html', {"main_pick": main_pick, "user": user})


def user_options(request):
    user = "user"
    main_pick = "user_options"
    return render(request, 'html/user/user_options.html', {"main_pick": main_pick, "user": user})


def user_trainings(request):
    user = "user"
    main_pick = "user_trainings"
    return render(request, 'html/user/trainings.html', {"main_pick": main_pick, "user": user})

# endregion

#API
#TODO SEND CONFIRMATION
def employeeAdd(request):
    user = "admin"
    main_pick = "employees"
    if addEmployee(request):
        employees = getEmployees()
        return render(request, 'html/admin/employees.html', {"main_pick": main_pick, "user": user,"employees":employees})
    else:
        employees = getEmployees()
        return render(request, 'html/admin/employees.html', {"main_pick": main_pick, "user": user,"employees":employees})

def competencyAdd(request):
    user = "admin"
    main_pick = 'competencies'
    if addCompetencies(request):
        competency = getCompetencies()
        competency_type = getCompetencies_type()
        return render(request, 'html/admin/competencies.html', {"main_pick": main_pick, "user": user, "competency":competency,"competency_type":competency_type})
    else:
        competency = getCompetencies()
        competency_type = getCompetencies_type()
        return render(request, 'html/admin/competencies.html', {"main_pick": main_pick, "user": user, "competency":competency,"competency_type":competency_type})

def trainingsAdd(request):
    user = "admin"
    main_pick = "trainings"
    competency = getCompetencies()
    if addTrainings(request):
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {"main_pick": main_pick, "user": user, "competency": competency,"trainings":trainings})
    else:
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {"main_pick": main_pick, "user": user, "competency": competency,"trainings":trainings})