from django.db import models
from django.utils.timezone import now
import json
from django.db import transaction
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

# Create your models here.

#HERE WE SET OUR MODELS FOR THE DATABASE, FIRST WE NEED TO SET UP THE SQLLITE DB THEN MIGRATE


class workplace(models.Model):
    id_workplace = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=False,unique=True)
    desc = models.CharField(max_length=500, blank=False,default="")

    def __str__(self):
        return self.name
    def as_json(self):
        return dict(
            id_workplace=self.id_workplace,
            name=self.name,
            desc=self.desc)

class employee(models.Model):
    id_employee = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,blank=False, default="")
    last_name = models.CharField(max_length=100,blank=False, default="")
    phone = models.CharField(max_length=100,blank=False, default="")
    city = models.CharField(max_length=100,blank=False, default="")
    country = models.CharField(max_length=100, blank=False, default="")
    email = models.CharField(max_length=100,blank=False, default="",unique=True)
    username = models.CharField(max_length=100,blank=False, default="",unique=True)
    id_workplace = models.ForeignKey(workplace,on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.first_name

    def as_json(self):
        return dict(
            id_employee=self.id_employee,
            first_name=self.first_name,
            last_name=self.last_name,
            phone=self.phone,
            city=self.city,
            country=self.country,
            email=self.email,
            username=self.username,
            workplace=self.id_workplace.name)

class competence_type(models.Model):
    id_competence_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=False, unique=True)

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(
            id_competence_type=self.id_competence_type,
            name=self.name)

class competence(models.Model):
    id_competence = models.AutoField(primary_key=True)
    hoegen_id = models.IntegerField(blank=False,default=0, unique=True)
    slo_name = models.CharField(max_length=100,blank=False)
    eng_name = models.CharField(max_length=100,blank=True)
    desc = models.CharField(max_length=500,blank=True, default="")
    id_competence_type = models.ForeignKey(competence_type, on_delete=models.CASCADE)

    def __str__(self):
        return self.slo_name

    def as_json(self):
        return dict(
            id_competence=self.id_competence,
            hoegen_id=self.hoegen_id,
            slo_name=self.slo_name,
            eng_name=self.eng_name,
            desc=self.desc,
            id_competence_type=self.id_competence_type.name)

class competence_relevance(models.Model):
    id_competence_relevance = models.AutoField(primary_key=True)
    competence_weight = models.IntegerField(blank=False)
    minimum_required = models.IntegerField(blank=False,default=0)
    id_competence = models.ForeignKey(competence, on_delete=models.CASCADE)
    id_workplace = models.ForeignKey(workplace, on_delete=models.CASCADE)

    def __int__(self):
        return self.competence_weight

class education(models.Model):
    id_education = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    desc = models.CharField(max_length=500, blank=True)
    date_from = models.DateField(default=now)
    date_to = models.DateField(default=now)
    id_competence = models.ManyToManyField(competence)

    def __str__(self):
        return self.name

class employee_competence(models.Model):
    id_employee_competence = models.AutoField(primary_key=True)
    level = models.IntegerField(blank=False)
    id_competence_type = models.ForeignKey(competence_type, on_delete=models.CASCADE)
    id_competence = models.ForeignKey(competence, on_delete=models.CASCADE)
    id_employee = models.ForeignKey(employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_employee_competence

class participation(models.Model):
    id_participation = models.AutoField(primary_key=True)
    participated = models.BooleanField(default=False)
    status = models.CharField(max_length=100, blank=False,default="")
    id_employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    id_education = models.ForeignKey(education, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_participation

#Users for login
class user(models.Model):
    id_user = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100,blank=False,unique=True)
    email = models.CharField(max_length=100,blank=False,unique=True)
    password = models.CharField(max_length=500, blank=False)
    user_image = models.ImageField(max_length=100, default=0)
    type=models.CharField(max_length=10, blank=False, default="user")
    def __str__(self):
        return self.user_name

class notifications(models.Model):
    id_notification = models.AutoField(primary_key=True)
    for_user = models.ForeignKey(user,on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    id_education = models.ForeignKey(education, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_notification

