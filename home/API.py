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
    new_employee = employee(first_name=first_name, last_name=last_name, phone=phone, city=city, country=country, email=email, username=username,id_workplace=new_workplace)
    new_employee.save()
    createUser(username,email,'user')
    return True

def getEmployees():
    return employee.objects.all()[0:10]

def getEmployeesByName(name):
    return employee.objects.filter(first_name__icontains=name)

def deleteEmployee(id):
    employee.objects.filter(id=id).delete()
    return True

###COMPETENCIES###
def addCompetencies(request):
    comp = request.POST.copy()
    nameENG = comp.get("competence_name_eng")
    nameSLO = comp.get("competence_name_slo")
    type = comp.get("competence_type")
    desc = comp.get("competence_desc")
    hoeg_id = comp.get("hoegen_id")
    new_type = competence_type.objects.get_or_create(name=type)[0]
    new_competence = competence(slo_name=nameSLO,eng_name=nameENG,hoegen_id=hoeg_id,desc=desc,id_competence_type=new_type)
    new_competence.save()
    return True

def getCompetencies():
    return competence.objects.all()

def getCompetenciesByType(id,new_list):
    return competence.objects.filter(Q(id_competence_type=id) & ~Q(id_competence__in=new_list))[0:8]

def getCompetenciesByName(name):
    return competence.objects.filter(slo_name=name)[0:8]

def getCompetenciesByTwo(value,type,new_list):
    return competence.objects.filter(Q(id_competence_type=type,slo_name__icontains=value) & ~Q(id_competence__in=new_list))

def getCompetenceByEmployee(id_employee,type):
    return employee_competence.objects.filter(id_employee=id_employee,id_competence_type=type)
def getCompetenceByEmployeePart(id_employee,type,value):
    findCompetences = competence.objects.filter(id_competence_type=type,slo_name__icontains=value)
    listOfComp = []
    for i in findCompetences:
        listOfComp.append(i.id_competence)
    return employee_competence.objects.filter(id_employee=id_employee,id_competence_type=type,id_competence__in=listOfComp)
###TRAININGS###
def addTrainings(request):
    training = request.POST.copy()
    competences = request.POST.getlist('training_competence')
    name = training.get("training_name")
    desc = training.get("training_desc")
    date_from = training.get("date_from")
    date_to = training.get("date_to")

    print(competences)
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
    print(workplaces)
    name = workplaces.get('workplace_name')
    desc = workplaces.get('workplace_desc')
    i = 0
    new_workplace = workplace(name=name,desc=desc)
    new_workplace.save()
    while i < 6:
        competen = "competence"+str(i)
        relevance = "relevance"+str(i)
        comp = workplaces.get(competen,None)
        relevant = workplaces.get(relevance,None)
        if comp == None:

            i = i+1
            continue
        get_competence = competence.objects.filter(slo_name=comp)[0]
        new_comp_relevance = competence_relevance(competence_weight=relevant,id_competence=get_competence,id_workplace=new_workplace)
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

###EMPLOYEE_COMPETENCE###
def saveEmployeeCompetence(id_competence,id_employee,score):
    selected_employee = employee.objects.filter(id_employee=id_employee)[0]
    selected_competence = competence.objects.filter(hoegen_id=id_competence)[0]
    selected_competence_type = competence_type.objects.filter(id_competence_type=selected_competence.id_competence_type.id_competence_type)[0]
    print(selected_competence)
    print(selected_employee)
    if employee_competence.objects.filter(id_competence=selected_competence.id_competence,id_employee=selected_employee.id_employee).exists():
        editCompetence = employee_competence.objects.filter(id_competence=selected_competence.id_competence,id_employee=selected_employee.id_employee)
        editCompetence.update(level=score)

    else:
        new_employee_competence = employee_competence(level=score,id_competence=selected_competence,id_competence_type=selected_competence_type,id_employee=selected_employee)
        new_employee_competence.save()

    return True
