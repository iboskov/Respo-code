from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.conf import settings
from django.db.models import Q
import json
from django.http import JsonResponse
from django.http.request import HttpRequest
from home.models import *


###USER###
def createUser(username,email,type):
    while True:
        password = get_random_string(length=10,allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789@*=?%$#()+')
        if user.objects.filter(password=password).exists():
            continue
        break

    new_user = user(user_name=username,email=email,password=password,type=type)
    new_user.save()
    #send_mail(subject, message, from_email, to_list(or single), fail_silently=True)
    subject = 'Account on Respo project app'
    message = 'Welcome to the Respo project App.\n you are seeing this email because an administrator added you on the list of employees\n Here is your username and password for logging into the respo application\n \n Username: '+username+'\n Password: '+password+'\n \n best wishes the Respo team'
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject,message,from_email,to_list,fail_silently=False)

def changePassword(username):
    while True:
        password = get_random_string(length=10,
                                     allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789@*=?%$#()+')
        if user.objects.filter(password=password).exists():
            continue
        break
    worker = employee.objects.filter(username=username)[0]
    user.objects.filter(user_name=username).update(password=password)
    #send email
    subject = 'Account on Respo project app'
    message = 'Hello '+worker.first_name+' '+worker.last_name+',\n you are seeing this email because an administrator changed your password. \n Here is your new password for logging into the respo application\n \n Username: '+username+'\n Password: '+password+'\n \n best wishes the Respo team'
    from_email = settings.EMAIL_HOST_USER
    to_list = [worker.email]
    send_mail(subject, message, from_email, to_list, fail_silently=False)
    return True
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

def getEmployeesByNameOrUsername(name):
    return employee.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(username__icontains=name))

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

def getCompetenceOnlyByNameAPI(name):
    return competence.objects.filter(slo_name=name)[0]

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

    if education.objects.filter(name=name).exists():
        return False
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
    return education.objects.all().order_by('-date_from')

def getTrainingsByNameAPI(name):
    return education.objects.filter(name=name)[0]

def getTrainingsByPartialName(name):
    return education.objects.filter(name__icontains=name).order_by('-date_from')

def getTrainingsById(id):
    return education.objects.filter(id_education=id)[0]

def deleteTrainingsById(id):
    education.objects.filter(id_education=id).delete()
    return True

def deleteTrainingByNameAPI(name):
    education.objects.filter(name=name).delete()
    return True

def getTrainingByName(name):
    return education.objects.filter(name=name)[0].id_competence.all()

def getTrainingByCompetenceAPI(comp):
    time = now().date()
    if education.objects.filter(id_competence=comp).exists():
        for i in education.objects.filter(id_competence=comp).order_by('-date_from'):
            if i.date_from < time:
                continue
            if i.date_from > time:
                return i
        return False
    else:
        return False

def editTrainings(request):
    training = request.POST.copy()
    competences = request.POST.getlist('edit_training_competence')
    id = training.get('edit_training_id', None)
    name = training.get('edit_training_name', None)
    desc  = training.get('edit_training_desc', None)
    date_from = training.get('edit_training_date_from', None)
    date_to = training.get('edit_training_date_to', None)

    if education.objects.filter(name=name).exists() and int(education.objects.filter(name=name)[0].id_education) != int(id):
        return False
    listOfCompetences = []
    for i in competences:
        comp = competence.objects.filter(slo_name=i)[0]
        listOfCompetences.append(comp)

    education.objects.filter(id_education=id).update(name=name,desc=desc,date_from=date_from, date_to=date_to)
    education.objects.filter(id_education=id)[0].id_competence.set(listOfCompetences)
    return True

###WORKPLACE###
def addWorkplace(request):
    workplaces = request.POST.copy()
    name = workplaces.get('workplace_name')
    desc = workplaces.get('workplace_desc')
    i = 0
    if workplace.objects.filter(name=name).exists():
        return False
    j = True
    new_workplace = workplace(name=name,desc=desc)
    new_workplace.save()
    while j:
        competen = "competence"+str(i)
        relevance = "relevance"+str(i)
        minimumVal = "minReq"+str(i)
        comp = workplaces.get(competen,None)
        relevant = workplaces.get(relevance,None)
        minim = workplaces.get(minimumVal,None)
        if comp == None and relevant == None and minim == None:
            break
        if comp == None:
            i = i+1
            continue
        get_competence = competence.objects.filter(slo_name=comp)[0]
        new_comp_relevance = competence_relevance(competence_weight=relevant,id_competence=get_competence,id_workplace=new_workplace,minimum_required=minim)
        new_comp_relevance.save()
        i = i+1


    return True

def addExtraCompetenceRelevance(request):
    request_for_extra = request.POST.copy()
    nameOfWorkplace = request_for_extra.get('extra_workplace_name', None)
    work = workplace.objects.filter(name=nameOfWorkplace)[0]
    i = 0
    j = True
    error = False
    while j:
        competen = "extracompetence"+str(i)
        relevance = "extrarelevance"+str(i)
        minimumVal = "extraminReq"+str(i)
        comp = request_for_extra.get(competen, None)
        relevant = request_for_extra.get(relevance, None)
        minim = request_for_extra.get(minimumVal, None)
        if comp == None and relevant == None and minim == None:
            break
        if comp == None:
            i = i+1
            continue
        get_competence = competence.objects.filter(slo_name=comp)[0]

        if competence_relevance.objects.filter(id_competence=get_competence.id_competence,id_workplace=work.id_workplace).exists():
            error=True
            break
        new_comp_relevance = competence_relevance(competence_weight=relevant,id_competence=get_competence,id_workplace=work,minimum_required=minim)
        new_comp_relevance.save()
        i = i+1

    if error:
        return False
    return True

def getWorkplaces():
    return workplace.objects.all()

def findWorkplace(id):
    return workplace.objects.filter(id_workplace=id).values('name')

def findWorkplaceByName(name):
    return workplace.objects.filter(name=name)[0]

def editWorkplace(request):
    workspace = request.POST.copy()
    id = workspace.get('edit-workplace-id', None)
    name = workspace.get('edit-workplace-name', None)
    desc = workspace.get('edit-workplace-desc', None)

    editable_workplace = workplace.objects.filter(id_workplace=id)[0]
    if editable_workplace.name != name and workplace.objects.filter(name=name).exists():
        return False

    workplace.objects.filter(id_workplace=id).update(name=name,desc=desc)
    return True

def deleteSelectedWorkplace(name):
    workspace = workplace.objects.filter(name=name)[0]
    competence_relevance.objects.filter(id_workplace=workspace.id_workplace).delete()
    workplace.objects.filter(name=name).delete()
    return True

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
    time = now()
    new_history = employee_history(id_competence=selected_competence,level=score,dateOfChange=time,id_employee=selected_employee)
    new_history.save()
    return True
def getAllEmployeeCompetence(id_employee):
    return employee_competence.objects.filter(id_employee=id_employee)

###COMPETENCE_RELEVANCE###
def getAllCompetenceRelevanceForWorkplace(id_workplace):
    return competence_relevance.objects.filter(id_workplace=id_workplace)

def getSpecificCompetenceOfRelevanceById(id_competence_relevance):
    return competence_relevance.objects.filter(id_competence_relevance=id_competence_relevance)

def findWorkplaceRelevanceAPI(name):
    work_place = workplace.objects.filter(name=name)[0]
    return competence_relevance.objects.filter(id_workplace=work_place.id_workplace)

def deleteCompetenceRelevanceAPI(id_relevance):
    competence_relevance.objects.filter(id_competence_relevance=id_relevance).delete()
    return True

def editCompetencyRelevance(nameOfCompetence,work,score):
    devidedScores = score.split(' ')
    relevance = devidedScores[0]
    minReq = devidedScores[1]
    selectedWorkplace = workplace.objects.filter(name=work)[0]
    selectedCompetence = competence.objects.filter(slo_name=nameOfCompetence)[0]

    competence_relevance.objects.filter(id_workplace=selectedWorkplace.id_workplace,id_competence=selectedCompetence.id_competence).update(competence_weight=relevance,minimum_required=minReq)
    return True

###PARTICIPATION###
def getParticipationByEmployee(worker,competence):
    emp = employee.objects.filter(id_employee=worker)[0]
    training = 0
    if education.objects.filter(id_competence=competence).exists():
        training = education.objects.filter(id_competence=competence)[0]
    else:
        return False

    if participation.objects.filter(id_employee=emp.id_employee,id_education__id_competence=competence).exists():
        if participation.objects.filter(id_employee=emp.id_employee,id_education__id_competence=competence)[0].participated:
            return False
        else:
            if participation.objects.filter(id_employee=emp.id_employee,id_education__id_competence=competence)[0].id_education.date_from <= now().date():
                return False

            return True
    else:
        False

def sendEmployeeOnEducation(edu,worker):
    training = education.objects.filter(name=edu)[0]
    emp = employee.objects.filter(id_employee=worker)[0]
    new_part = participation(participated=False,status="Waiting",id_employee=emp,id_education=training)
    new_part.save()
    return True

def getParticipationByEducation(edu_id,status):
     party = participation.objects.filter(id_education=edu_id)
     if len(party) > 0:
         if party[0].participated == False and status == 'Finished':
             for i in party:
                 if i.status == 'Accepted':
                    participation.objects.filter(id_employee=i.id_employee.id_employee,id_education=edu_id).update(participated=True)
                 if i.status == 'Waiting':
                    participation.objects.filter(id_employee=i.id_employee.id_employee,id_education=edu_id).update(status='Declined')
         elif party[0].participated == False and status == 'Ongoing':

                for i in party:
                    if i.status == 'Waiting':
                        participation.objects.filter(id_employee=i.id_employee.id_employee,id_education=edu_id).update(status='Declined')

     return participation.objects.filter(id_education=edu_id)

def getParticipationByEmployeeUsername(username):
    worker = employee.objects.filter(username=username)[0]
    return participation.objects.filter(id_employee=worker.id_employee).order_by('-id_education__date_from')