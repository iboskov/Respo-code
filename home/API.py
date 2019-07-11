from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
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
    send_mail(subject,message,from_email,to_list,fail_silently=True)

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
    createUser(username,email,'user')
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

###WORKPLACE###
def getWorkplaces():
    return workplace.objects.all()

