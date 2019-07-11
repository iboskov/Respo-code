from django.db import models
import json
from django.db import transaction
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

# Create your models here.

#HERE WE SET OUR MODELS FOR THE DATABASE, FIRST WE NEED TO SET UP THE SQLLITE DB THEN MIGRATE


class workplace(models.Model):
    id_workplace = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=False)

    def __str__(self):
        return self.name

class employee(models.Model):
    id_employee = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,blank=False, default="")
    last_name = models.CharField(max_length=100,blank=False, default="")
    phone = models.CharField(max_length=100,blank=False, default="")
    city = models.CharField(max_length=100,blank=False, default="")
    country = models.CharField(max_length=100, blank=False, default="")
    email = models.CharField(max_length=100,blank=False, default="")
    username = models.CharField(max_length=100,blank=False, default="",unique=True)
    id_workplace = models.ForeignKey(workplace,on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.first_name

class competence_type(models.Model):
    id_competence_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=False, unique=True)

    def __str__(self):
        return self.name

class competence(models.Model):
    id_competence = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=False, unique=True)
    desc = models.CharField(max_length=500,blank=True, default="")
    id_competence_type = models.ForeignKey(competence_type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class competence_relevance(models.Model):
    id_competence_relevance = models.AutoField(primary_key=True)
    competence_weight = models.IntegerField(blank=False)
    id_competence = models.ForeignKey(competence, on_delete=models.CASCADE)
    id_workplace = models.ForeignKey(workplace, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_competence_relevance

class education(models.Model):
    id_education = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    desc = models.CharField(max_length=500, blank=True)
    id_competence = models.ForeignKey(competence, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class employee_competence(models.Model):
    id_employee_competence = models.AutoField(primary_key=True)
    level = models.IntegerField(blank=False)
    id_competence = models.ForeignKey(competence, on_delete=models.CASCADE)
    id_employeee = models.ForeignKey(employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_employee_competence

class participation(models.Model):
    id_participation = models.AutoField(primary_key=True)
    time = models.DateField()
    id_employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    id_education = models.ForeignKey(education, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_participation

#Users for login
class user(models.Model):
    id_user = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100,blank=False)
    password = models.CharField(max_length=500, blank=False)
    user_image = models.ImageField(max_length=100, default=0)

    def __str__(self):
        return self.email