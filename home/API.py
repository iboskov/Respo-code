from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db.models import Q
import json
from django.http import JsonResponse
from django.http.request import HttpRequest
from home.models import *


###USER###
def createUser(username,email,type):
    password = get_random_string(length=10,allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789@*=?')
    new_user = user(user_name=username,email=email,password=password,type=type)
    new_user.save()
    #send_mail(subject, message, from_email, to_list(or single), fail_silently=True)
    subject = 'Account on Respo project app'
    message = 'Welcome to the Respo project App.\n you are seeing this email because an administrator added you on the list of employees\n Here is your username and password for logging into the respo application\n \n Username: '+username+'\n password: '+password+'\n \n best wishes the Respo team'
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject,message,from_email,to_list,fail_silently=False)

###EMPLOYEE###
def addEmployee(request):

    worker = request.POST.copy()
    first_name = worker.get("employee_name","")
    last_name = worker.get("employee_lastname","")
    phone = worker.get("employee_phone","")
    city = worker.get("employee_city","")
    country = worker.get("employee_country","")
    email = worker.get("employee_email","")
    username = worker.get("employee_username","")
    worker_workplace = worker.get("employee-workplace","")
    #TODO ERROR CODING IN CASE IT FAILS
    new_workplace = workplace.objects.get_or_create(name=worker_workplace)[0]
    if employee.objects.filter(email=email).exists() or employee.objects.filter(username=username).exists():
        return False
    else:
        new_employee = employee(first_name=first_name, last_name=last_name, phone=phone, city=city, country=country, email=email, username=username,id_workplace=new_workplace)
        new_employee.save()
        createUser(username,email,'user')

    return True

def editEmployee(request):
    worker = request.POST.copy()
    id_employee = worker.get("edit-employee_id", "")
    first_name = worker.get("edit-employee_name", "")
    last_name = worker.get("edit-employee_lastname", "")
    phone = worker.get("edit-employee_phone", "")
    city = worker.get("edit-employee_city", "")
    country = worker.get("edit-employee_country", "")
    email = worker.get("edit-employee_email", "")
    username = worker.get("edit-employee_username", "")
    worker_workplace = worker.get("edit-employee_workplace", "")
    new_workplace = workplace.objects.get_or_create(name=worker_workplace)[0]
    new_worker = employee.objects.filter(id_employee=id_employee)[0]
    # check when username and email are different
    newUser = 0
    newEmail = 0
    if new_worker.username != username:
        if employee.objects.filter(username=username).exists():
            return False
        else:
            newUser = 1

    if new_worker.email != email:
        if employee.objects.filter(email=email).exists():
            return False
        else:
            newEmail = 1
    if newUser == 1 and newEmail == 1:
        return False

    employee.objects.filter(id_employee=id_employee).update(first_name=first_name,last_name=last_name,phone=phone,city=city,country=country,email=email,username=username,id_workplace=new_workplace)
    if newUser == 1:
        edit_user = user.objects.filter(email=email).update(user_name=username)
    if newEmail == 1:
        edit_user = user.objects.filter(user_name=username).update(email=email)

    return True


def getEmployees():
    return employee.objects.all()[0:10]

def getEmployeesByName(name):
    return employee.objects.filter(first_name__icontains=name)

def deleteEmployeeById(id):
    delete_emp = employee.objects.filter(id_employee=id)[0]
    employee_competence.objects.filter(id_employee=delete_emp.id_employee).delete()
    user.objects.filter(user_name=delete_emp.username).delete()
    employee.objects.filter(id_employee=id).delete()
    return True

def getEmployeeeByNameAndSurname(first_name,last_name):
    return employee.objects.filter(first_name=first_name,last_name=last_name)

def getEmployeeById(id_employee):
    return employee.objects.filter(id_employee=id_employee)[0]

###COMPETENCIES###
def addCompetencies(request):
    comp = request.POST.copy()
    nameENG = comp.get("competence_name_eng")
    nameSLO = comp.get("competence_name_slo")
    type = comp.get("competence_type")
    desc = comp.get("competence_desc")
    hoeg_id = comp.get("hoegen_id")

    if competence.objects.filter(hoegen_id=hoeg_id).exists() or competence.objects.filter(slo_name=nameSLO).exists():
        return False

    new_type = competence_type.objects.get_or_create(name=type)[0]
    new_competence = competence(slo_name=nameSLO,eng_name=nameENG,hoegen_id=hoeg_id,desc=desc,id_competence_type=new_type)
    new_competence.save()
    return True

def getCompetenceByIdOnly(id):
    return competence.objects.filter(hoegen_id=id)[0]

def getCompetencies():
    return competence.objects.all()

def getCompetenciesByType(id,new_list):
    return competence.objects.filter(Q(id_competence_type=id) & ~Q(id_competence__in=new_list))[0:8]

def getCompetenciesByName(name):
    return competence.objects.filter(slo_name=name)[0:8]

def getCompetenciesByTwo(value,type,new_list):
    return competence.objects.filter(Q(id_competence_type=type,slo_name__icontains=value) & ~Q(id_competence__in=new_list))

def getCompetenciesByOnlyType(type):
    typeOf = competence_type.objects.filter(name=type)[0]
    return competence.objects.filter(id_competence_type=typeOf.id_competence_type)

def getCompetenceByEmployee(id_employee,type):
    return employee_competence.objects.filter(id_employee=id_employee,id_competence_type=type)

def getCompetenceByEmployeePart(id_employee,type,value):
    findCompetences = competence.objects.filter(id_competence_type=type,slo_name__icontains=value)
    listOfComp = []
    for i in findCompetences:
        listOfComp.append(i.id_competence)
    return employee_competence.objects.filter(id_employee=id_employee,id_competence_type=type,id_competence__in=listOfComp)

def editCompetenceByRequest(request):
    competences = request.POST.copy()
    id_competence = competences.get('edit_comp_id',None)
    type = competences.get('edit_comp_type', None)
    hoeg_id = competences.get('edit_comp_hoegenId', None)
    eng_name = competences.get('edit_comp_engName', None)
    slo_name = competences.get('edit_comp_sloName', None)
    desc = competences.get('edit_comp_desc', None)

    editable_competence = competence.objects.filter(id_competence=id_competence)[0]
    if int(hoeg_id) != int(editable_competence.hoegen_id) and competence.objects.filter(hoegen_id=hoeg_id).exists():
        return False
    new_type = competence_type.objects.get_or_create(name=type)[0]
    competence.objects.filter(id_competence=id_competence).update(id_competence_type=new_type,hoegen_id=hoeg_id,slo_name=slo_name,eng_name=eng_name,desc=desc)
    return True

def deleteSelectedCompetenceByHoegId(id):
    competence.objects.filter(hoegen_id=id).delete()
    return True

###TRAININGS###
def addTrainings(request):
    training = request.POST.copy()
    competences = request.POST.getlist('training_competence')
    name = training.get("training_name")
    desc = training.get("training_desc")
    date_from = training.get("date_from")
    date_to = training.get("date_to")

    new_education = education(name=name, date_from=date_from, date_to=date_to, desc=desc)
    new_education.save()
    new_education = education.objects.filter(name=name)[0]
    list_of_competences = []
    for i in competences:
        new_competence = competence.objects.filter(slo_name=i)[0]
        list_of_competences.append(new_competence)
    new_education.id_competence.set(list_of_competences)
    return True

def getTrainings():
    return education.objects.all()

###WORKPLACE###
def addWorkplace(request):
    workplaces = request.POST.copy()
    name = workplaces.get('workplace_name')
    desc = workplaces.get('workplace_desc')
    i = 0
    if workplace.objects.filter(name=name).exists():
        return False

    new_workplace = workplace(name=name,desc=desc)
    new_workplace.save()
    while i < 6:
        competen = "competence"+str(i)
        relevance = "relevance"+str(i)
        minimumVal = "minReq"+str(i)
        comp = workplaces.get(competen,None)
        relevant = workplaces.get(relevance,None)
        minim = workplaces.get(minimumVal,None)
        if comp == None:
            i = i+1
            continue
        get_competence = competence.objects.filter(slo_name=comp)[0]
        new_comp_relevance = competence_relevance(competence_weight=relevant,id_competence=get_competence,id_workplace=new_workplace,minimum_required=minim)
        new_comp_relevance.save()
        i = i+1


    return True


def getWorkplaces():
    return workplace.objects.all()

def findWorkplace(id):
    return workplace.objects.filter(id_workplace=id).values('name')

###COMPETENCE_TYPE###
def getCompetenceType(value):
    return competence_type.objects.filter(name__icontains=value)

def getCompetenceTypes():
    return competence_type.objects.all()[0:10]

def getAllCompetencies_type():
    return competence_type.objects.all()

def getCompetenceTypeStrict(value):
    return competence_type.objects.filter(name=value)[0]

def editCompetenceType(request):
    types = request.POST.copy()
    id = types.get('edit_competenceType_id',None)
    name = types.get('edit_competenceType_name', None)
    if competence_type.objects.filter(name=name).exists():
        return False

    competence_type.objects.filter(id_competence_type=id).update(name=name)

    return True

def deleteCompetenceTypeByName(name):
    type = competence_type.objects.filter(name=name)[0]
    competence.objects.filter(id_competence_type=type.id_competence_type).delete()
    competence_type.objects.filter(name=name).delete()
    return True

###EMPLOYEE_COMPETENCE###
def saveEmployeeCompetence(id_competence,id_employee,score):
    selected_employee = employee.objects.filter(id_employee=id_employee)[0]
    selected_competence = competence.objects.filter(hoegen_id=id_competence)[0]
    selected_competence_type = competence_type.objects.filter(id_competence_type=selected_competence.id_competence_type.id_competence_type)[0]

    if employee_competence.objects.filter(id_competence=selected_competence.id_competence,id_employee=selected_employee.id_employee).exists():
        editCompetence = employee_competence.objects.filter(id_competence=selected_competence.id_competence,id_employee=selected_employee.id_employee)
        editCompetence.update(level=score)

    else:
        new_employee_competence = employee_competence(level=score,id_competence=selected_competence,id_competence_type=selected_competence_type,id_employee=selected_employee)
        new_employee_competence.save()

    return True
def getAllEmployeeCompetence(id_employee):
    return employee_competence.objects.filter(id_employee=id_employee)

###COMPETENCE_RELEVANCE###
def getAllCompetenceRelevanceForWorkplace(id_workplace):
    return competence_relevance.objects.filter(id_workplace=id_workplace)

def getSpecificCompetenceOfRelevanceById(id_competence_relevance):
    return competence_relevance.objects.filter(id_competence_relevance=id_competence_relevance)
