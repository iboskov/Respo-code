
"""
This is the views.py file where we will direct html and send objects from backend to the html code from templates
login function atm is just an example of how it should be written.
'html\login' is the location of the html file.
"""
from django.core.files import File
import pandas as pd
from pandas import ExcelFile
from django.shortcuts import render, redirect
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
    alert = {"show": "none", "type": "success", "message": "Excel's have been successfully uploaded!"}
    return render(request, 'html/admin/upload.html', {"main_pick": main_pick, "user": user, "alert": alert})


def employees(request):
    user = "admin"
    main_pick = "employees"
    employees = getEmployees()
    workplaces = getWorkplaces()
    competence_types = getCompetenceTypes()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/employees.html', {"main_pick": main_pick, "user": user, "employees": employees, "workplaces": workplaces, "competence_types": competence_types, "alert": alert})


def competencies(request):
    user = "admin"
    main_pick = 'competencies'
    competency = getCompetencies()
    competency_type = getAllCompetencies_type()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/competencies.html',
                  {"main_pick": main_pick, "user": user, "competency": competency, "competency_type": competency_type, "alert": alert})


def workplaces(request):
    user = "admin"
    main_pick = 'workplaces'
    competency = getCompetencies()
    workplaces = getWorkplaces()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/workplaces.html', {"main_pick": main_pick, "user": user,'competency':competency,'workplaces':workplaces, "alert": alert})


def options(request):
    user = "admin"
    main_pick = 'options'
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/options.html', {"main_pick": main_pick, "user": user, "alert": alert})


def history(request):
    user = "admin"
    main_pick = "history"
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/history.html', {"main_pick": main_pick, "user": user, "alert": alert})


def trainings(request):
    user = "admin"
    main_pick = "trainings"
    competency = getCompetencies()
    trainings = getTrainings()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/trainings.html', {"main_pick": main_pick, "user": user,"competency":competency,"trainings":trainings, "alert": alert})

def analytics(request):
    user = "admin"
    main_pick = "analytics"
    employees = getEmployees()
    competency = getCompetencies()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/analytics.html', {"main_pick": main_pick, "user": user,"employees":employees,"competency":competency, "alert": alert})


def status(request):
    user = "admin"
    main_pick = "status"
    train = {}
    employees = getEmployees()
    allTrainings = getTrainings()
    for i in allTrainings:
        participants = getParticipationByEducation(i.id_education)
        tableOfContent = {}
        tableOfContent["desc"] = i.desc
        for j in participants:
            tableOfContent[j.id_employee.first_name+" "+j.id_employee.last_name] = j.status

        train[i.name] = tableOfContent
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/status.html', {"main_pick": main_pick, "user": user,"train":train,"employees":employees, "alert": alert})
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
    workplaces = getWorkplaces()
    competence_types = getCompetenceTypes()
    if addEmployee(request):
        employees = getEmployees()
        alert = {"show": "inline", "type": "success", "message": "Employee successfully added"}
        return render(request, 'html/admin/employees.html', {"main_pick": main_pick, "user": user, "employees": employees, "workplaces": workplaces, "competence_types": competence_types, "alert": alert})
    else:
        employees = getEmployees()
        alert = {"show": "inline", "type": "danger", "message": "Employee already exists, username and email must be unique!"}
        return render(request, 'html/admin/employees.html', {"main_pick": main_pick, "user": user, "employees": employees, "workplaces": workplaces, "competence_types": competence_types,"alert":alert})

def employeeEdit(request):
    user = "admin"
    main_pick = "employees"
    workplaces = getWorkplaces()
    competence_types = getCompetenceTypes()
    if editEmployee(request):
        employees = getEmployees()
        alert = {"show": "inline", "type": "success", "message": "Employee successfully changed"}
        return render(request, 'html/admin/employees.html',{"main_pick": main_pick, "user": user, "employees": employees, "workplaces": workplaces,"competence_types": competence_types, "alert": alert})
    else:
        employees = getEmployees()
        alert = {"show": "inline", "type": "danger", "message": "Employee was not edited, keep in mind you cannot change username and email at the same time."}
        return render(request, 'html/admin/employees.html',{"main_pick": main_pick, "user": user, "employees": employees, "workplaces": workplaces,"competence_types": competence_types, "alert": alert})

def competencyAdd(request):
    user = "admin"
    main_pick = 'competencies'
    if addCompetencies(request):
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "success", "message": "Competency successfully added"}
        return render(request, 'html/admin/competencies.html', {"main_pick": main_pick, "user": user, "competency":competency,"competency_type":competency_type,"alert":alert})
    else:
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "danger", "message": "Competency already exists, Hoegen id and Slovenian name need to be unique!"}
        return render(request, 'html/admin/competencies.html', {"main_pick": main_pick, "user": user, "competency":competency,"competency_type":competency_type,"alert":alert})

def competenciesEdit(request):
    user = "admin"
    main_pick = 'competencies'
    if editCompetenceByRequest(request):
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "success", "message": "Competency successfully changed!"}
        return render(request, 'html/admin/competencies.html',
                      {"main_pick": main_pick, "user": user, "competency": competency,
                       "competency_type": competency_type, "alert": alert})
    else:
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "danger", "message": "Competency with that hoegen id already exists!"}
        return render(request, 'html/admin/competencies.html',
                      {"main_pick": main_pick, "user": user, "competency": competency,
                       "competency_type": competency_type, "alert": alert})

def competencies_type_edit(request):
    user = "admin"
    main_pick = 'competencies'
    if editCompetenceType(request):
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "success", "message": "Competency type successfully changed"}
        return render(request, 'html/admin/competencies.html', {"main_pick": main_pick, "user": user, "competency":competency,"competency_type":competency_type,"alert":alert})
    else:
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "danger", "message": "Competency type name already exists!"}
        return render(request, 'html/admin/competencies.html', {"main_pick": main_pick, "user": user, "competency":competency,"competency_type":competency_type,"alert":alert})

def trainingsAdd(request):
    user = "admin"
    main_pick = "trainings"
    competency = getCompetencies()
    if addTrainings(request):
        alert = {"show": "inline", "type": "success", "message": "Training successfully added"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {"main_pick": main_pick, "user": user, "competency": competency,"trainings":trainings,"alert":alert})
    else:
        alert = {"show": "inline", "type": "danger", "message": "Training with that name already exists!"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {"main_pick": main_pick, "user": user, "competency": competency, "trainings": trainings,
                       "alert": alert})

def workplaceAdd(request):
    user = "admin"
    main_pick = "workplaces"
    if addWorkplace(request):
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "success", "message": "Workplace successfully added"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {"main_pick": main_pick, "user": user, 'competency': competency,'workplaces':workplaces,'alert':alert})
    else:
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "danger", "message": "Workplace with that name already exists!"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {"main_pick": main_pick, "user": user, 'competency': competency,'workplaces':workplaces, 'alert': alert})

def workplaceEdit(request):
    user = "admin"
    main_pick = "workplaces"
    if editWorkplace(request):
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "success", "message": "Workplace successfully changed"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {"main_pick": main_pick, "user": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})
    else:
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "danger", "message": "Workplace with that name already exists!"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {"main_pick": main_pick, "user": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})

def addExtraRelevanceToWorkplace(request):
    user = "admin"
    main_pick = "workplaces"
    if addExtraCompetenceRelevance(request):
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "success", "message": "Successfully added more competencies to workplace"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {"main_pick": main_pick, "user": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})
    else:
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "danger", "message": "One or more competencies already exists for that workplace!"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {"main_pick": main_pick, "user": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})

def editTraining(request):
    user = "admin"
    main_pick = "trainings"
    competency = getCompetencies()
    if editTrainings(request):
        alert = {"show": "inline", "type": "success", "message": "Training successfully changed!"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {"main_pick": main_pick, "user": user, "competency": competency, "trainings": trainings,
                       "alert": alert})
    else:
        alert = {"show": "inline", "type": "danger", "message": "Training with that name already exists!"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {"main_pick": main_pick, "user": user, "competency": competency, "trainings": trainings,"alert":alert})

###AJAX###
def findEmployees(request):
    user = request.GET.get('username',None)
    foundUsers = getEmployeesByName(user)
    html = render_to_string(
        template_name="html/admin/partial_table_second.html",
        context={"employees":foundUsers}
    )
    data_dict = {"html_from_view": html}
    return JsonResponse(data = data_dict,safe=False)

def findCompetenceType(request):
    value = request.GET.get('types',None)
    foundTypes = getCompetenceType(value)
    html = render_to_string(
        template_name="html/admin/partial_table_competence_second.html",
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

def getCompetenciesByTypeOnRequest(request):
    type = request.GET.get('types', None)
    competences = getCompetenciesByOnlyType(type)
    html = render_to_string(
        template_name="html/admin/partial_table_competencies_byType.html",
        context={"competency":competences}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

def findWorkplaceRelevance(request):
    workplace_name = request.GET.get('name', None)
    print(workplace_name)
    competencesWithRelevance = findWorkplaceRelevanceAPI(workplace_name)
    html = render_to_string(
        template_name="html/admin/partial_table_workplaces_relevance.html",
        context={'competenceRelevance':competencesWithRelevance}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

def findTrainingCompetencies(request):
    training_name = request.GET.get('name', None)
    trainingInfo = getTrainingByName(training_name)
    html = render_to_string(
        template_name="html/admin/partial_table_trainings.html",
        context={'training_competence':trainingInfo}
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
        true_id = id_of_competence[1].split(']')[0]
        if value[i] == '':
            continue
        saveEmployeeCompetence(true_id,employee,value[i])

    return JsonResponse(True, safe=False)

def editCompetencyRelevanceForWorkplace(request):
    value = request.GET
    work = request.GET.get('workplace', None)
    for i in value:
        if i == 'workplace':
            continue
        nameOfCompetence = i.split('[')
        trueName = nameOfCompetence[1].split(']')[0]
        editCompetencyRelevance(trueName,work,value[i])

    return JsonResponse(True, safe=False)

def uploadFile(request):
    file = File(request.GET.get('excel_competencies'))

    excel = pd.read_excel(file,sheetname='Temida-kompetence')
    print(excel.columns)
    return JsonResponse(True, safe=False)

def deleteEmployee(request):
    id_employee = request.GET.get('employee', None)
    if deleteEmployeeById(id_employee):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

def deleteCompetenceType(request):
    name_type = request.GET.get('type', None)
    if deleteCompetenceTypeByName(name_type):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

def deleteCompetence(request):
    hoeg_id = request.GET.get('hoeg_id', None)
    if deleteSelectedCompetenceByHoegId(hoeg_id):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

def deleteWorkplaceAndRelevance(request):
    name = request.GET.get('name', None)
    if deleteSelectedWorkplace(name):
        return JsonResponse(True,safe=False)

    return JsonResponse(False,safe=False)

def deleteCompetence_relevance(request):
    id_relevance = request.GET.get('id_relevance', None)
    if deleteCompetenceRelevanceAPI(id_relevance):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

def deleteTrainings(request):
    id_education = request.GET.get('id_education', None)
    print(id_education)
    if deleteTrainingsById(id_education):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

def getEditEmployee(request):
    id_employee = request.GET.get('employee',None)
    employee = getEmployeeById(id_employee)
    dic_employee = employee.as_json()
    return JsonResponse(data=dic_employee,safe=False)

def getEditCompetenceType(request):
    name = request.GET.get('type', None)
    type = getCompetenceTypeStrict(name)
    dic_type = type.as_json()
    return JsonResponse(data=dic_type, safe=False)

def getEditCompetences(request):
    id = request.GET.get('id', None)
    editCompetence = getCompetenceByIdOnly(id)
    dic_editCompetence = editCompetence.as_json()
    return JsonResponse(data=dic_editCompetence, safe=False)

def getEditWorkplaces(request):
    name = request.GET.get('name', None)
    editWorkplace = findWorkplaceByName(name)
    dic_editWorkplace = editWorkplace.as_json()
    return JsonResponse(data=dic_editWorkplace, safe=False)

def getEditEducation(request):
    id = request.GET.get('id_education', None)
    by = request.GET.get('by', None)
    selectedEducation = 0
    print(by)
    if by != None:
        selectedEducation = getTrainingsByNameAPI(id)
    else:
        selectedEducation = getTrainingsById(id)
    newComp = selectedEducation.as_json()
    competences = selectedEducation.id_competence.all()
    newInformation = []
    for i in competences:
        newInformation.append(i.slo_name)
    print(newInformation)
    dataDic = {
        'education':newComp,
        'competences':newInformation
    }
    return JsonResponse(data=dataDic, safe=False)

def sendEmployee(request):
    information = request.GET.get('information')
    devide = information.split('|')
    trainingName = devide[0]
    employee_id = devide[1]
    if sendEmployeeOnEducation(trainingName,employee_id):
        return JsonResponse(True,safe=False)

    return JsonResponse(False,safe=False)



def analyticsCompute(request):
    listOfEmployees = request.POST.getlist('employeesSelect',None)
    postRequest = request.POST.copy()
    algorithemSelect1 = postRequest.get('algo1', None)
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
    #Go through all employees
    for i in listOfEmployees:
        devide = i.split(" ")
        gottenEmployee = getEmployeeeByNameAndSurname(devide[0],devide[1])[0] #find employee
        findAllOfHisCompetence = getAllEmployeeCompetence(gottenEmployee.id_employee) #find his competence
        getAllCompetenceRelevance = getAllCompetenceRelevanceForWorkplace(gottenEmployee.id_workplace.id_workplace) #get all work related relations
        print(getAllCompetenceRelevance)
        lengthOfRelevance = len(getAllCompetenceRelevance)
        print(lengthOfRelevance)
        #create tables for statistics
        tableOfRelevance = np.zeros(shape=(lengthOfRelevance,1))
        tableOfScores = np.zeros(shape=(lengthOfRelevance,1))
        tableOfImportance = np.zeros(shape=(lengthOfRelevance,1))
        iterator = 0
        idsOfRelevance = np.zeros(shape=(lengthOfRelevance,1))
        tableOfResults = {}
        name=""
        #Loop through all competence relevances
        for i in getAllCompetenceRelevance:
            value = 0
            relevance = 0
            #Loop through all of a employees competences
            for j in findAllOfHisCompetence:
                #find match and add
                if i.id_competence.id_competence == j.id_competence.id_competence:
                    #check if employee is going to participate in an existing training for this competence
                    if getParticipationByEmployee(gottenEmployee.id_employee,j.id_competence.id_competence):
                        value = 100
                    else:
                        value = j.level
                    relevance = i.minimum_required
                    name = i.id_competence.slo_name
                    importance = i.competence_weight
                    id = i.id_competence_relevance
            #If the employee doesn't have a competence for his workplace
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

        alg1 = None
        alg2 = None
        alg3 = None
        alg4 = None
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
        doesTrainingExist=False
        if alg1 != 0 and alg1 is not None:
            ids = alg1[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            theGottenCompetence = getCompetenceOnlyByNameAPI(competence_rele.id_competence.slo_name)
            possibleTraining = getTrainingByCompetenceAPI(theGottenCompetence.id_competence)
            if possibleTraining is not False:
                doesTrainingExist = True
                tableOfContentAlg1.append(possibleTraining.name)
            else:
                doesTrainingExist = False
                tableOfContentAlg1.append('No training at this time')
            tableOfContentAlg1.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg1.append(alg1[2])
            if doesTrainingExist:
                tableOfContentAlg1.append(possibleTraining.name+"|"+str(gottenEmployee.id_employee))
            else:
                tableOfContentAlg1.append('NO')
            ALG1[devide[0] + " " + devide[1]] = tableOfContentAlg1
        elif alg1 is not None:
            tableOfContentAlg1.append('/')
            tableOfContentAlg1.append('/')
            tableOfContentAlg1.append('All competencies satisfy requirment')
            tableOfContentAlg1.append('NO')
            ALG1[devide[0] + " " + devide[1]] = tableOfContentAlg1

        if alg2 != 0 and alg2 is not None:
            ids = alg2[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            theGottenCompetence = getCompetenceOnlyByNameAPI(competence_rele.id_competence.slo_name)
            possibleTraining = getTrainingByCompetenceAPI(theGottenCompetence.id_competence)
            if possibleTraining is not False:
                doesTrainingExist = True
                tableOfContentAlg2.append(possibleTraining.name)
            else:
                doesTrainingExist = False
                tableOfContentAlg2.append('No training at this time')
            tableOfContentAlg2.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg2.append(alg2[2])

            if doesTrainingExist:
                tableOfContentAlg2.append(possibleTraining.name+"|"+str(gottenEmployee.id_employee))
            else:
                tableOfContentAlg2.append('NO')
            ALG2[devide[0] + " " + devide[1]] = tableOfContentAlg2

        elif alg2 is not None:
            tableOfContentAlg2.append('/')
            tableOfContentAlg2.append('/')
            tableOfContentAlg2.append('All competencies satisfy requirment')
            tableOfContentAlg2.append('NO')
            ALG2[devide[0] + " " + devide[1]] = tableOfContentAlg2

        if alg3 != 0 and alg3 is not None:
            ids = alg3[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            theGottenCompetence = getCompetenceOnlyByNameAPI(competence_rele.id_competence.slo_name)
            possibleTraining = getTrainingByCompetenceAPI(theGottenCompetence.id_competence)
            if possibleTraining is not False:
                doesTrainingExist = True
                tableOfContentAlg3.append(possibleTraining.name)
            else:
                doesTrainingExist = False
                tableOfContentAlg3.append('No training at this time')
            tableOfContentAlg3.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg3.append(alg3[2])
            if doesTrainingExist:
                tableOfContentAlg3.append(possibleTraining.name+"|"+str(gottenEmployee.id_employee))
            else:
                tableOfContentAlg3.append('NO')
            ALG3[devide[0] + " " + devide[1]] = tableOfContentAlg3

        elif alg3 is not None:
            tableOfContentAlg3.append('/')
            tableOfContentAlg3.append('/')
            tableOfContentAlg3.append('All competencies satisfy requirment')
            tableOfContentAlg3.append('NO')
            ALG3[devide[0] + " " + devide[1]] = tableOfContentAlg3

        if alg4 != 0 and alg4 is not None:
            ids = alg4[3]
            competence_rele = getSpecificCompetenceOfRelevanceById(idsOfRelevance[int(ids)][0])[0]
            theGottenCompetence = getCompetenceOnlyByNameAPI(competence_rele.id_competence.slo_name)
            possibleTraining = getTrainingByCompetenceAPI(theGottenCompetence.id_competence)
            if possibleTraining is not False:
                doesTrainingExist = True
                tableOfContentAlg4.append(possibleTraining.name)
            else:
                doesTrainingExist = False
                tableOfContentAlg4.append('No training at this time')
            tableOfContentAlg4.append(competence_rele.id_competence.slo_name)
            tableOfContentAlg4.append(alg4[2])
            if doesTrainingExist:
                tableOfContentAlg4.append(possibleTraining.name+"|"+str(gottenEmployee.id_employee))
            else:
                tableOfContentAlg4.append('NO')
            ALG4[devide[0] + " " + devide[1]] = tableOfContentAlg4

        elif alg4 is not None:
            tableOfContentAlg4.append('/')
            tableOfContentAlg4.append('/')
            tableOfContentAlg4.append('All competencies satisfy requirment')
            tableOfContentAlg4.append('NO')
            ALG4[devide[0] + " " + devide[1]] = tableOfContentAlg4

    # TIME TO RENDER
    print(ALG1)
    print(ALG2)
    print(ALG3)
    print(ALG4)
    user = "admin"
    main_pick = "analytics"
    employees = getEmployees()
    competency = getCompetencies()
    return render(request, 'html/admin/analytics.html', {"main_pick": main_pick, "user": user, "employees": employees,"competency":competency,"ALG1":ALG1,"ALG2":ALG2,"ALG3":ALG3,"ALG4":ALG4})


