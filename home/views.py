
"""
This is the views.py file where we will direct html and send objects from backend to the html code from templates
login function atm is just an example of how it should be written.
'html\login' is the location of the html file.
"""
from django.core.files import File
import pandas as pd
from pandas import ExcelFile
from django.shortcuts import render
from home.API import *
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
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
    workplaces = getWorkplaces()
    competence_types = getCompetenceTypes()
    return render(request, 'html/admin/employees.html', {"main_pick": main_pick, "user": user,"employees":employees,"workplaces":workplaces,"competence_types":competence_types})


def competencies(request):
    user = "admin"
    main_pick = 'competencies'
    competency = getCompetencies()
    competency_type = getAllCompetencies_type()
    return render(request, 'html/admin/competencies.html',
                  {"main_pick": main_pick, "user": user, "competency": competency, "competency_type": competency_type})


def workplaces(request):
    user = "admin"
    main_pick = 'workplaces'
    competency = getCompetencies()
    return render(request, 'html/admin/workplaces.html', {"main_pick": main_pick, "user": user,'competency':competency})


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


def user_status(request):
    user = "user"
    main_pick = "user_status"
    return render(request, 'html/user/user_status.html', {"main_pick": main_pick, "user": user})


def user_trainings(request):
    user = "user"
    main_pick = "user_trainings"
    return render(request, 'html/user/trainings.html', {"main_pick": main_pick, "user": user})

# endregion

#***API***
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
        competency_type = getAllCompetencies_type()
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

def workplaceAdd(request):
    user = "admin"
    main_pick = "workplaces"
    if addWorkplace(request):
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {"main_pick": main_pick, "user": user, 'competency': competency})


###AJAX###
def findEmployees(request):
    user = request.GET.get('username',None)
    foundUsers = getEmployeesByName(user)
    html = render_to_string(
        template_name="html/admin/partial_table.html",
        context={"employees":foundUsers}
    )
    data_dict = {"html_from_view": html}
    return JsonResponse(data = data_dict,safe=False)

def findCompetenceType(request):
    value = request.GET.get('types',None)
    foundTypes = getCompetenceType(value)
    html = render_to_string(
        template_name="html/admin/partial_table_competence.html",
        context={"competence_types":foundTypes}
    )
    data_dict = {"html_from_view": html}
    return JsonResponse(data=data_dict, safe=False)

def findCompetencesByType(request):
    value = request.GET.get('types', None)
    id_employee = request.GET.get('employee',None)
    getCompetenceByRelevance = getCompetenceByEmployee(id_employee,value)
    new_list = []
    for i in getCompetenceByRelevance:
        new_list.append(i.id_competence.id_competence)
    getCompetencies = getCompetenciesByType(value,new_list)
    html = render_to_string(
        template_name="html/admin/partial_table_competence_values.html",
        context={"competences":getCompetencies,"competence_values":getCompetenceByRelevance}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

def findCompetencesByTwo(request):
    value = request.GET.get('value',None)
    type = request.GET.get('types', None)
    id_employee = request.GET.get('employee',None)
    getCompetenceByRelevance = getCompetenceByEmployeePart(id_employee, type,value)
    new_list = []
    for i in getCompetenceByRelevance:
        new_list.append(i.id_competence.id_competence)
    getCompetencies = getCompetenciesByTwo(value,type,new_list)

    html = render_to_string(
        template_name="html/admin/partial_table_competence_values.html",
        context={"competences":getCompetencies,"competence_values":getCompetenceByRelevance}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

def addCompetenciesToUser(request):
    value = request.GET
    employee = request.GET.get('employee',None)
    for i in value:
        if i == 'employee':
            continue
        id_of_competence = i.split('[')
        print(id_of_competence)
        true_id = id_of_competence[1].split(']')[0]
        print(true_id)
        saveEmployeeCompetence(true_id,employee,value[i])

    return JsonResponse(True,safe=False)

def uploadFile(request):
    file = File(request.GET.get('excel_competencies'))

    excel = pd.read_excel(file,sheetname='Temida-kompetence')
    print(excel.columns)
    return JsonResponse(True, safe=False)

def deleteEmployee(request):
    id_employee = request.GET.get('employee',None)
    if deleteEmployee(id_employee):
        return JsonResponse(True,safe=False)
    else:
        return JsonResponse(False, safe=False)
