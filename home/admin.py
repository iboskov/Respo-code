from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from home.models import myuser

admin.site.register(myuser,UserAdmin)