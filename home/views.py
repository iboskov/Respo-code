
"""
This is the views.py file where we will direct html and send objects from backend to the html code from templates
login function atm is just an example of how it should be written.
'html\login' is the location of the html file.
"""
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import pandas as pd
from pandas import ExcelFile
from django.shortcuts import render, redirect
from home.API import *
from home.Analytics import *
from home.decorators import employee_required, HR_required
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
import numpy as np
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
from django.http import HttpResponse

@login_required
def index(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    return render(request, 'html/index.html', {'notifications':notifications,'number':nrOfNotifications})


#def login(request):
#    title = "Login"
#    return render(request, 'html/login.html', {"title": title})

# region admin_views

# additional functions
def authenticationOfUser(request):
    username = request.POST['usrName']
    password = request.POST['usrPass']
    user = findUser(username,password)
    print(user)
    if user is not None:
        login(request,user)
        notifications = getAllNotifications(user)
        nrOfNotifications = len(notifications)
        allTrainings = getTrainings()
        train = calculateForTrainings(allTrainings)
        usr = "admin"
        return render(request, 'html/index.html', {"usr": usr,'notifications':notifications,'number':nrOfNotifications})
    else:
        title = "Login"
        alert = {"show": "inline", "type": "danger", "message": "Wrong username or password."}
        return render(request, 'registration/login.html', {"title": title,'alert':alert})


#TODO create check for code and create admin user
@login_required
def logoutUser(request):
    logout(request)
    title = "Login"
    alert = {"show": "inline", "type": "success", "message": "You have successfully logged out."}
    return render(request, 'registration/login.html', {"title": title,"alert":alert})

def calculateForTrainings(allTrainings):
    train = {}
    for i in allTrainings:

        participant = {}
        tableOfContent = {}
        tableOfContent["desc"] = i.desc
        if now().date() < i.date_from:
            participant['status'] = 'Scheduled'
        elif now().date() >= i.date_from and now().date() <= i.date_to:
            participant['status'] = 'Ongoing'
        else:
            participant['status'] = 'Finished'

        participants = getParticipationByEducation(i.id_education,participant['status'])
        for j in participants:
            tableOfContent[j.id_employee.first_name + " " + j.id_employee.last_name] = j.status
        participant['participants'] = tableOfContent


        train[i.name] = participant
    return train
# end additional functions
@login_required
@HR_required
def upload(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    usr = "admin"
    main_pick = "upload"
    alert = {"show": "none", "type": "success", "message": "Excel's have been successfully uploaded!"}
    return render(request, 'html/admin/upload.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": usr, "alert": alert})
@login_required
@HR_required
def employees(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    usr = "admin"
    main_pick = "employees"
    employees = getEmployees()
    workplaces = getWorkplaces()
    competence_types = getCompetenceTypes()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/employees.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": usr, "employees": employees, "workplaces": workplaces, "competence_types": competence_types, "alert": alert})

@login_required
@HR_required
def competencies(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    usr = "admin"
    main_pick = 'competencies'
    competency = getCompetencies()
    competency_type = getAllCompetencies_type()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/competencies.html',
                  {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": usr, "competency": competency, "competency_type": competency_type, "alert": alert})

@login_required
@HR_required
def workplaces(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    usr = "admin"
    main_pick = 'workplaces'
    competency = getCompetencies()
    workplaces = getWorkplaces()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/workplaces.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": usr,'competency':competency,'workplaces':workplaces, "alert": alert})

@login_required
@HR_required
def options(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = 'options'
    employees = getEmployees()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/options.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user,"employees":employees, "alert": alert})

@login_required
@HR_required
def history(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "history"
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/history.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "alert": alert})

@login_required
@HR_required
def trainings(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "trainings"
    competency = getCompetencies()
    trainings = getTrainings()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/trainings.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user,"competency":competency,"trainings":trainings, "alert": alert})

@login_required
@HR_required
def analytics(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "analytics"
    employees = getEmployees()
    competency = getCompetencies()
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/analytics.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user,"employees":employees,"competency":competency, "alert": alert})

@login_required
@HR_required
def status(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "status"
    train = {}
    employees = getEmployees()
    allTrainings = getTrainings()
    competency = getCompetencies()
    train = calculateForTrainings(allTrainings)
    alert = {"show": "none", "type": "danger", "message": "There was a problem adding an employee!"}
    return render(request, 'html/admin/status.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick,"competency":competency, "usr": user,"train":train,"employees":employees, "alert": alert})
# endregion

# region user_views

@login_required
@employee_required
def user_history_recent(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    employe = getEmployeeeByNameAndSurname(user.first_name, user.last_name)[0]
    user_comp = getAllEmployeeCompetence(employe.id_employee)
    user = "user"
    main_pick = "user_history"
    picked = "recent"
    return render(request, 'html/user/history.html', {'competences':user_comp,'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "picked": picked})

@login_required
@employee_required
def user_history_timeline(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    employe = getEmployeeeByNameAndSurname(user.first_name, user.last_name)[0]
    user_comp = getAllEmployeeCompetence(employe.id_employee)
    user = "usr"
    main_pick = "user_history"
    picked = "timeline"
    return render(request, 'html/user/history.html', {'competences':user_comp,'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "picked": picked})

@login_required
@employee_required
def user_competencies(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = get_user(request)
    employe = getEmployeeeByNameAndSurname(user.first_name,user.last_name)[0]
    user_comp = getAllEmployeeCompetence(employe.id_employee)
    types = []

    for i in user_comp:
        exists = False
        for j in types:
            if j == i.id_competence_type.name:
                exists = True
        if exists:
            continue
        types.append(i.id_competence_type.name)

    main_pick = "user_competencies"
    return render(request, 'html/user/competencies.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick,"types":types,"competences":user_comp})

@login_required
@employee_required
def user_status(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = get_user(request)
    competency = getCompetencies()
    get_participation = getParticipationByEmployeeUsername(user.username)
    main_pick = "user_status"
    return render(request, 'html/user/user_status.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick,"competency":competency,"participation":get_participation})

@login_required
@employee_required
def user_trainings(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = get_user(request)
    get_participation = getParticipationByEmployeeUsername(user.username)
    main_pick = "user_trainings"
    return render(request, 'html/user/trainings.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick,'participation':get_participation})

# endregion

#***API***
@login_required
@HR_required
def employeeAdd(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "employees"
    workplaces = getWorkplaces()
    competence_types = getCompetenceTypes()
    if addEmployee(request):
        employees = getEmployees()
        alert = {"show": "inline", "type": "success", "message": "Employee successfully added"}
        return render(request, 'html/admin/employees.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "employees": employees, "workplaces": workplaces, "competence_types": competence_types, "alert": alert})
    else:
        employees = getEmployees()
        alert = {"show": "inline", "type": "danger", "message": "Employee already exists, username and email must be unique!"}
        return render(request, 'html/admin/employees.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "employees": employees, "workplaces": workplaces, "competence_types": competence_types,"alert":alert})

def createHR(request):
    title = "Login"
    value = addHR_user(request)
    if value == 'not code':
        alert = {"show": "inline", "type": "danger", "message": "The code you entered is invalid"}
        return render(request, 'registration/login.html', {"title": title, "alert": alert})
    if value:
        alert = {"show": "inline", "type": "success", "message": "Successfully created an account. A email with your username and password has been sent."}
        return render(request, 'registration/login.html', {"title":title,"alert":alert})
    else:
        alert = {"show": "inline", "type": "danger", "message": "An account with that username or email already exists."}
        return render(request, 'registration/login.html', {"title": title, "alert": alert})

@login_required
@HR_required
def employeeEdit(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "employees"
    workplaces = getWorkplaces()
    competence_types = getCompetenceTypes()
    if editEmployee(request):
        employees = getEmployees()
        alert = {"show": "inline", "type": "success", "message": "Employee successfully changed"}
        return render(request, 'html/admin/employees.html',{'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "employees": employees, "workplaces": workplaces,"competence_types": competence_types, "alert": alert})
    else:
        employees = getEmployees()
        alert = {"show": "inline", "type": "danger", "message": "Employee was not edited, keep in mind you cannot change username and email at the same time."}
        return render(request, 'html/admin/employees.html',{'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "employees": employees, "workplaces": workplaces,"competence_types": competence_types, "alert": alert})

@login_required
@HR_required
def competencyAdd(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = 'competencies'
    if addCompetencies(request):
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "success", "message": "Competency successfully added"}
        return render(request, 'html/admin/competencies.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency":competency,"competency_type":competency_type,"alert":alert})
    else:
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "danger", "message": "Competency already exists, Hoegen id and Slovenian name need to be unique!"}
        return render(request, 'html/admin/competencies.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency":competency,"competency_type":competency_type,"alert":alert})

@login_required
@HR_required
def competenciesEdit(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = 'competencies'
    if editCompetenceByRequest(request):
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "success", "message": "Competency successfully changed!"}
        return render(request, 'html/admin/competencies.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency": competency,
                       "competency_type": competency_type, "alert": alert})
    else:
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "danger", "message": "Competency with that hoegen id already exists!"}
        return render(request, 'html/admin/competencies.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency": competency,
                       "competency_type": competency_type, "alert": alert})

@login_required
@HR_required
def competencies_type_edit(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = 'competencies'
    if editCompetenceType(request):
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "success", "message": "Competency type successfully changed"}
        return render(request, 'html/admin/competencies.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency":competency,"competency_type":competency_type,"alert":alert})
    else:
        competency = getCompetencies()
        competency_type = getAllCompetencies_type()
        alert = {"show": "inline", "type": "danger", "message": "Competency type name already exists!"}
        return render(request, 'html/admin/competencies.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency":competency,"competency_type":competency_type,"alert":alert})

@login_required
@HR_required
def trainingsAdd(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "trainings"
    competency = getCompetencies()
    if addTrainings(request):
        alert = {"show": "inline", "type": "success", "message": "Training successfully added"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency": competency,"trainings":trainings,"alert":alert})
    else:
        alert = {"show": "inline", "type": "danger", "message": "Training with that name already exists!"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency": competency, "trainings": trainings,
                       "alert": alert})

@login_required
@HR_required
def workplaceAdd(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "workplaces"
    if addWorkplace(request):
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "success", "message": "Workplace successfully added"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, 'competency': competency,'workplaces':workplaces,'alert':alert})
    else:
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "danger", "message": "Workplace with that name already exists!"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, 'competency': competency,'workplaces':workplaces, 'alert': alert})

@login_required
@HR_required
def workplaceEdit(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    user = "admin"
    main_pick = "workplaces"
    if editWorkplace(request):
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "success", "message": "Workplace successfully changed"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})
    else:
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "danger", "message": "Workplace with that name already exists!"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})

@login_required
@HR_required
def addExtraRelevanceToWorkplace(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    main_pick = "workplaces"
    if addExtraCompetenceRelevance(request):
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "success", "message": "Successfully added more competencies to workplace"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})
    else:
        workplaces = getWorkplaces()
        alert = {"show": "inline", "type": "danger", "message": "One or more competencies already exists for that workplace!"}
        competency = getCompetencies()
        return render(request, 'html/admin/workplaces.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, 'competency': competency, 'workplaces': workplaces,
                       'alert': alert})

@login_required
@HR_required
def editTraining(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    main_pick = "trainings"
    competency = getCompetencies()
    if editTrainings(request):
        alert = {"show": "inline", "type": "success", "message": "Training successfully changed!"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency": competency, "trainings": trainings,
                       "alert": alert})
    else:
        alert = {"show": "inline", "type": "danger", "message": "Training with that name already exists!"}
        trainings = getTrainings()
        return render(request, 'html/admin/trainings.html',
                      {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "competency": competency, "trainings": trainings,"alert":alert})

###AJAX USER###
@login_required
@employee_required
def getCompetencesByUser(request):
    type = request.GET.get('type', None)
    comp = request.GET.get('competence', None)

    user = get_user(request)
    employ = getEmployeeeByNameAndSurname(user.first_name,user.last_name)[0]
    compRelevance = getAllCompetenceRelevanceForWorkplace(employ.id_workplace.id_workplace)
    userCompetence = 0
    if comp is not None:
        userCompetence = getEmployeeCompetenceByTypeAndKey(type,comp)
    else:
        userCompetence = getEmployeeCompetenceByType(type)
    html = render_to_string(
        template_name="html/user/partial_table_competencies_user.html",
        context={'competences':userCompetence,'relevance':compRelevance}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

@login_required
@employee_required
def respondToTraining(request):
    train = request.GET.get('training',None)
    response = request.GET.get('response', None)
    user = get_user(request)
    if setResponseToParticipation(user.username,response,train):
        return JsonResponse(True,safe=False)

    return JsonResponse(False,safe=False)

@login_required
@employee_required
def changeDecision(request):
    info = request.GET.get('info',None)
    decision = request.GET.get('decision', None)
    if resetResponseParticipation(info,decision):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@employee_required
def getGraphUser(request):
    compList = request.GET.get('competences')
    fromDate = request.GET.get('from', None)
    toDate = request.GET.get('to', None)
    user = get_user(request)
    employ = getEmployeeByUsername(user.username)
    work = findWorkplaceByName(employ.id_workplace.name)
    dictionary = {}
    times = []

    lst = []
    relevance = getCompetenceRelevanceByWorkAndComp(compList,work.id_workplace,)
    if fromDate == "" or fromDate == None:
        fromDate = None
    if toDate == "" or toDate == None:
        toDate = None
    listOfEmpComp = getEmployeeHistoryFromTimeCompetenceAndEmployee(user.username,fromDate,toDate,compList)
    print(listOfEmpComp)
    data = []
    dataRel = []
    for j in listOfEmpComp:
        dicton = j.as_json()
        if dicton['dateOfChange'] not in times:
            times.append(dicton['dateOfChange'])
            data.append(dicton['level'])
            dataRel.append(relevance.minimum_required)
    new_dic = dict(
        label=compList,
        fill=False,
        data=data,
        borderColor="#3e95cd",
        backgroundColor="#3e95cd"
    )
    lst.append(new_dic)
    rele_dic = dict(
        label='workplace relevance ('+work.name+')',
        fill=False,
        data=dataRel,
        borderColor="#3cba9f",
        backgroundColor="#3cba9f"
    )
    lst.append(rele_dic)
    dictionary['information'] = lst
    dictionary['Times'] = times

    return JsonResponse(data=dictionary, safe=False)

###AJAX ADMIN###
@login_required
@HR_required
def getGraphAdmin(request):
    compList = request.GET.get('competences')
    fromDate = request.GET.get('from', None)
    toDate = request.GET.get('to', None)
    emp = request.GET.get('employ', None)
    devide = emp.split('(')
    newDevide = devide[1].split(')')
    worker = newDevide[0]
    employ = getEmployeeByUsername(worker)

    work = findWorkplaceByName(employ.id_workplace.name)
    dictionary = {}
    times = []

    lst = []
    relevance = getCompetenceRelevanceByWorkAndComp(compList, work.id_workplace, )
    if fromDate == "" or fromDate == None:
        fromDate = None
    if toDate == "" or toDate == None:
        toDate = None
    listOfEmpComp = getEmployeeHistoryFromTimeCompetenceAndEmployee(employ.username, fromDate, toDate, compList)
    data = []
    dataRel = []
    for j in listOfEmpComp:
        dicton = j.as_json()
        if dicton['dateOfChange'] not in times:
            times.append(dicton['dateOfChange'])
            data.append(dicton['level'])
            dataRel.append(relevance.minimum_required)
    new_dic = dict(
        label=compList,
        fill=False,
        data=data,
        borderColor="#3e95cd",
        backgroundColor="#3e95cd"
    )
    lst.append(new_dic)
    rele_dic = dict(
        label='workplace relevance (' + work.name + ')',
        fill=False,
        data=dataRel,
        borderColor="#3cba9f",
        backgroundColor="#3cba9f"
    )
    lst.append(rele_dic)
    dictionary['information'] = lst
    dictionary['Times'] = times

    return JsonResponse(data=dictionary, safe=False)

@login_required
@HR_required
def findEmployees(request):
    user = request.GET.get('username',None)
    foundUsers = getEmployeesByName(user)
    html = render_to_string(
        template_name="html/admin/partial_table_second.html",
        context={"employees":foundUsers}
    )
    data_dict = {"html_from_view": html}
    return JsonResponse(data=data_dict,safe=False)

@login_required
@HR_required
def getEmployeeCompetenceHistory(request):
    employ = request.GET.get('info', None)
    devide = employ.split('(')
    anotherDevide = devide[1].split(')')
    usernameOfEmp = anotherDevide[0]
    getEmp = getEmployeeByUsername(usernameOfEmp)
    getCompRelevance = getAllEmployeeCompetence(getEmp.id_employee)

    html = render_to_string(
        template_name="html/admin/partial_options_employee_competence.html",
        context={'EmpCompetences':getCompRelevance}
    )
    data_dict = {"html_from_view": html}
    return JsonResponse(data=data_dict, safe=False)


@login_required
@HR_required
def findCompetenceType(request):
    value = request.GET.get('types',None)
    foundTypes = getCompetenceType(value)
    html = render_to_string(
        template_name="html/admin/partial_table_competence_second.html",
        context={"competence_types":foundTypes}
    )
    data_dict = {"html_from_view": html}
    return JsonResponse(data=data_dict, safe=False)

@login_required
@HR_required
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

@login_required
@HR_required
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

@login_required
@HR_required
def getCompetenciesByTypeOnRequest(request):
    type = request.GET.get('types', None)
    competences = getCompetenciesByOnlyType(type)
    html = render_to_string(
        template_name="html/admin/partial_table_competencies_byType.html",
        context={"competency":competences}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

@login_required
@HR_required
def findWorkplaceRelevance(request):
    workplace_name = request.GET.get('name', None)
    competencesWithRelevance = findWorkplaceRelevanceAPI(workplace_name)
    html = render_to_string(
        template_name="html/admin/partial_table_workplaces_relevance.html",
        context={'competenceRelevance':competencesWithRelevance}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

@login_required
@HR_required
def findTrainingCompetencies(request):
    training_name = request.GET.get('name', None)
    trainingInfo = getTrainingByName(training_name)
    html = render_to_string(
        template_name="html/admin/partial_table_trainings.html",
        context={'training_competence':trainingInfo}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

@login_required
@HR_required
def getParticipationEmployee(request):
    information = request.GET.get('info', None)

    if information is not None:
        if information == "":
            return JsonResponse(False,safe=False)
        devide = information.split("(")
        username = devide[1].split(")")[0]
        party = getParticipationByEmployeeUsername(username)
        html = render_to_string(
            template_name="html/admin/partial_table_status_employee.html",
            context={'participations':party}
        )
        data_dict = {"html_from_view":html}
        return JsonResponse(data=data_dict, safe=False)
    return JsonResponse(False, safe=False)
@login_required
@HR_required
def findTrainingsByKey(request):
    keys = request.GET.get('training', None)
    allTrainings = getTrainingsByPartialName(keys)
    train = {}
    train = calculateForTrainings(allTrainings)
    html = render_to_string(
        template_name="html/admin/partial_table_status.html",
        context={'train':train}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

@login_required
@HR_required
def getEmployeeForOption(request):
    keys = request.GET.get('username', None)
    findWorkers = getEmployeesByNameOrUsername(keys)
    html = render_to_string(
        template_name="html/admin/partial_table_options.html",
        context={'employees':findWorkers}
    )
    data_dict = {"html_from_view":html}
    return JsonResponse(data=data_dict, safe=False)

@login_required
@HR_required
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

@login_required
@HR_required
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


@login_required
@HR_required
def uploadFile(request):
    if request.FILES['excel_One']:
        fs = FileSystemStorage()
        myFile = request.FILES['excel_One']
        devide = myFile.name.split('.')
        if devide[1] != 'xlsx':
            alert = {"show": "inline", "type": "danger", "message": "The file you uploaded is not an xlsx file."}
            return render(request, 'html/admin/upload.html',
                          {"alert": alert})
        x1 = pd.ExcelFile(myFile)
        if len(x1.sheet_names) > 1:
            alert = {"show": "inline", "type": "danger", "message": "The file you uploaded for competences should not have more then one sheet name."}
            return render(request, 'html/admin/upload.html',
                          {"alert": alert})
        excel = pd.read_excel(myFile,sheet_name=x1.sheet_names[0])
        if not excel.columns.contains('Hogan id'):
            alert = {"show": "inline", "type": "danger",
                     "message": "The file you uploaded for competences does not have Hogan id column."}
            return render(request, 'html/admin/upload.html',
                          {"alert": alert})
        hoganId = excel['Hogan id']
        jobs = []
        if setDatabase(jobs,excel):
            alert = {"show": "inline", "type": "success", "message": "Excel's have been successfully uploaded!"}
            return render(request, 'html/admin/upload.html',
                          {"alert": alert})

        alert = {"show": "inline", "type": "danger", "message": "There was an error in processing your xlsx file!"}
        return render(request, 'html/admin/upload.html',
                      {"alert": alert})
    else:
        alert = {"show": "inline", "type": "danger", "message": "No file uploaded."}
        return render(request, 'html/admin/upload.html',
                      {"alert": alert})

@login_required
@HR_required
def deleteEmployee(request):
    id_employee = request.GET.get('employee', None)
    if deleteEmployeeById(id_employee):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@HR_required
def deleteCompetenceType(request):
    name_type = request.GET.get('type', None)
    if deleteCompetenceTypeByName(name_type):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@HR_required
def deleteCompetence(request):
    hoeg_id = request.GET.get('hoeg_id', None)
    if deleteSelectedCompetenceByHoegId(hoeg_id):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@HR_required
def deleteWorkplaceAndRelevance(request):
    name = request.GET.get('name', None)
    if deleteSelectedWorkplace(name):
        return JsonResponse(True,safe=False)

    return JsonResponse(False,safe=False)

@login_required
@HR_required
def deleteCompetence_relevance(request):
    id_relevance = request.GET.get('id_relevance', None)
    if deleteCompetenceRelevanceAPI(id_relevance):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@HR_required
def deleteTrainings(request):
    id_education = request.GET.get('id_education', None)
    if deleteTrainingsById(id_education):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@HR_required
def deleteTrainingByName(request):
    name = request.GET.get('name', None)
    if deleteTrainingByNameAPI(name):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@HR_required
def getEditEmployee(request):
    id_employee = request.GET.get('employee',None)
    employee = getEmployeeById(id_employee)
    dic_employee = employee.as_json()
    return JsonResponse(data=dic_employee,safe=False)

@login_required
@HR_required
def getEditCompetenceType(request):
    name = request.GET.get('type', None)
    type = getCompetenceTypeStrict(name)
    dic_type = type.as_json()
    return JsonResponse(data=dic_type, safe=False)

@login_required
@HR_required
def getEditCompetences(request):
    id = request.GET.get('id', None)
    editCompetence = getCompetenceByIdOnly(id)
    dic_editCompetence = editCompetence.as_json()
    return JsonResponse(data=dic_editCompetence, safe=False)

@login_required
@HR_required
def getEditWorkplaces(request):
    name = request.GET.get('name', None)
    editWorkplace = findWorkplaceByName(name)
    dic_editWorkplace = editWorkplace.as_json()
    return JsonResponse(data=dic_editWorkplace, safe=False)

@login_required
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

@login_required
@HR_required
def sendEmployee(request):
    information = request.GET.get('information', None)
    devide = information.split('|')
    trainingName = devide[0]
    employee_id = devide[1]
    if sendEmployeeOnEducation(trainingName,employee_id):
        dataDic = {
            'info':information
        }
        return JsonResponse(data=dataDic,safe=False)

    return JsonResponse(False,safe=False)

@login_required
@HR_required
def resendInvitation(request):
    information = request.GET.get('information', None)
    party = request.GET.get('participation', None)
    if party is not None:
        if resendParticipationByParticipation(party):
            return JsonResponse(True,safe=False)
    else:
        devide = information.split('|')
        worker = devide[0].split(' ')
        first_name = worker[0]
        last_name = worker[1]
        training = devide[1]
        if resendParticipation(first_name,last_name,training):
            return JsonResponse(True,safe=False)

    return JsonResponse(False, safe=False)



@login_required
@HR_required
def resetPassword(request):
    username = request.GET.get('username', None)
    if changePassword(username):
        return JsonResponse(True, safe=False)

    return JsonResponse(False, safe=False)

@login_required
@HR_required
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
            print(i)
            if len(name) == 0:
                print("hello")
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

        #check which algorithems we use and use them
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

        #get information based off the results
        if alg1 != 0 and alg1 is not None:
            ids = alg1[3]
            print(idsOfRelevance)
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
    selects = {}
    selects['algorithem1'] = algorithemSelect1
    selects['algorithem2'] = algorithemSelect2
    selects['algorithem3'] = algorithemSelect3
    selects['algorithem4'] = algorithemSelect4
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    return render(request, 'html/admin/analytics.html', {'notifications':notifications,'number':nrOfNotifications,"main_pick": main_pick, "usr": user, "employees": employees,"competency":competency,"ALG1":ALG1,"ALG2":ALG2,"ALG3":ALG3,"ALG4":ALG4,"selects":selects})

### GENERAL AJAX ###
@login_required
def editMyself(request):
    username = request.GET.get('employee', None)
    worker = getEmployeeByUsername(username)
    hr = getHRUserByUsername(username)
    if worker is not None:
        data_dic = worker.as_json()
        return JsonResponse(data=data_dic,safe=False)
    data_dic = hr.as_json()
    return JsonResponse(data=data_dic, safe=False)
@login_required
def deleteNotifications(request):
    user = get_user(request)
    deleteUserNotifications(user.username)
    return JsonResponse(True, safe=False)

### GENERAL API ###
@login_required
def saveEditMyself(request):
    user = get_user(request)
    notifications = getAllNotifications(user)
    nrOfNotifications = len(notifications)
    if saveHRorEmployee(request):
        alert = {"show": "inline", "type": "success", "message": "Successfully changed!"}
        return render(request, 'html/index.html',{'notifications':notifications,'number':nrOfNotifications,'alert':alert})

    alert = {"show": "inline", "type": "danger",
                 "message": "User was not edited, keep in mind you cannot change username and email at the same time."}
    return render(request, 'html/index.html',{'notifications':notifications,'number':nrOfNotifications,'alert':alert})

