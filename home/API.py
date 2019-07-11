from home.models import *
import json
from django.http import JsonResponse
from django.http.request import HttpRequest


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
    worker_workplace = worker.get("employee_type","")
    #TODO ERROR CODING IN CASE IT FAILS
    new_workplace = workplace.objects.get_or_create(name=worker_workplace)[0]
    new_employee = employee(first_name=first_name, last_name=last_name, phone=phone, city=city, country=country, email=email, username=username,id_workplace=new_workplace)
    new_employee.save()
    new_user = user(username=username,email=email,password="RANDOMATFIRST")
    new_user.save()
    return True

def getEmployees():
    return employee.objects.all()

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

def getCompetencies_type():
    return competence_type.objects.all()


###TRAININGS###
def addTrainings(request):
    training = request.POST.copy()
    name = training.get("training_name")
    desc = training.get("training_desc")
    date_from = training.get("date_from")
    date_to = training.get("date_to")
    competency = training.get("training_competence").split(" ")[1]
    add_to_competence = competence.objects.filter(name=competency)[0]
    new_education = education(name=name,date_from=date_from,date_to=date_to,desc=desc,id_competence=add_to_competence,)
    new_education.save()
    return True

def getTrainings():
    return education.objects.all()