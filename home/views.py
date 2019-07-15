
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
from home.Analytics import *
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
import numpy as np
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
    employees = getEmployees()
    return render(request, 'html/admin/analytics.html', {"main_pick": main_pick, "user": user,"employees":employees})


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


def analyticsCompute(request):
    listOfEmployees = request.POST.getlist('employeesSelect',None)
    postRequest = request.POST.copy()
    algorithemSelect1 = postRequest.get('algo1',None)
    algorithemSelect2 = postRequest.get('algo2', None)
    algorithemSelect3 = postRequest.get('algo3', None)
    algorithemSelect4 = postRequest.get('algo4', None)
    print(algorithemSelect1)
    print(listOfEmployees)
    numberOfEmployees = len(listOfEmployees)
    print(numberOfEmployees)
    view = 'pessimistic'
    #start the calculation
    ALG1 = {}
    ALG2 = {}
    ALG3 = {}
    ALG4 = {}
    for i in listOfEmployees:
        devide = i.split(" ")
        gottenEmployee = getEmployeeeByNameAndSurname(devide[0],devide[1])[0]
        findAllOfHisCompetence = getAllEmployeeCompetence(gottenEmployee.id_employee)
        getAllCompetenceRelevance = getAllCompetenceRelevanceForWorkplace(gottenEmployee.id_workplace.id_workplace)
        print(getAllCompetenceRelevance)
        lengthOfRelevance = len(getAllCompetenceRelevance)
        print(lengthOfRelevance)
        tableOfRelevance = np.zeros(shape=(lengthOfRelevance,1))
        tableOfScores = np.zeros(shape=(lengthOfRelevance,1))
        tableOfImportance = np.zeros(shape=(lengthOfRelevance,1))
        iterator = 0
        idsOfRelevance = np.zeros(shape=(lengthOfRelevance,1))
        tableOfResults = {}
        for i in getAllCompetenceRelevance:
            value = 0
            relevance = 0
            for j in findAllOfHisCompetence:
                if i.id_competence.id_competence == j.id_competence.id_competence:
                    value = j.level
                    relevance = i.minimum_required
                    name = i.id_competence.slo_name
                    importance = i.competence_weight
                    id = i.id_competence_relevance
            if len(name) == 0:
                value = 0
                relevance = i.minimum_required
                name = i.id_competence.slo_name
                importance = i.competence_weight
                id = i.id_competence_relevance
            tableOfRelevance[iterator][0] = int(relevance)
            tableOfScores[iterator][0] = int(value)
            tableOfImportance[iterator][0] = int(importance)
            idsOfRelevance[iterator][0] = id
            iterator = iterator+1

        print(tableOfRelevance)
        print(tableOfScores)
        #Now the analysis

        alg1 = 0
        alg2 = 0
        alg3 = 0
        alg4 = 0
        print(tableOfImportance)
        if algorithemSelect1 == 'on':
            alg1 = maximal_absolute_lack(0,tableOfScores,tableOfRelevance,view)
        if algorithemSelect2 == 'on':
            alg2 = maximal_relative_lack(0,tableOfScores,tableOfRelevance,view)
        if algorithemSelect3 == 'on':
            alg3 = most_important_competence_that_lack(0,tableOfScores,tableOfRelevance,view)
        if algorithemSelect4 == 'on':
            alg4 = improve_comp_by_formula(0,tableOfScores,tableOfRelevance,tableOfImportance,view)
        tableOfContentAlg1 = []
        tableOfContentAlg2 = []
        tableOfContentAlg3 = []
        tableOfContentAlg4 = []
        if alg1 != 0 and alg1 is not None:
            ids = alg1[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            tableOfContentAlg1.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg1.append(alg1[2])
            ALG1[devide[0] + " " + devide[1]] = tableOfContentAlg1
        if alg2 != 0 and alg2 is not None:
            ids = alg2[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            tableOfContentAlg2.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg2.append(alg2[2])
            ALG2[devide[0] + " " + devide[1]] = tableOfContentAlg2
        if alg3 != 0 and alg3 is not None:
            ids = alg3[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            tableOfContentAlg3.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg3.append(alg3[2])
            ALG3[devide[0] + " " + devide[1]] = tableOfContentAlg3
        if alg4 != 0 and alg4 is not None:
            ids = alg4[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            tableOfContentAlg4.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg4.append(alg4[2])
            ALG4[devide[0] + " " + devide[1]] = tableOfContentAlg4

    # TIME TO RENDER

    user = "admin"
    main_pick = "analytics"
    employees = getEmployees()
    return render(request, 'html/admin/analytics.html', {"main_pick": main_pick, "user": user, "employees": employees,"ALG1":ALG1,"ALG2":ALG2,"ALG3":ALG3,"ALG4":ALG4})


