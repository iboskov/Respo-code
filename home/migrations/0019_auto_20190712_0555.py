# Generated by Django 2.2.1 on 2019-07-12 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20190712_0325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee_competence',
            old_name='id_employeee',
            new_name='id_employee',
        ),
    ]