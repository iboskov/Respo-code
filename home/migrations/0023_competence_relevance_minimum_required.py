# Generated by Django 2.2.1 on 2019-07-15 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_employee_competence'),
    ]

    operations = [
        migrations.AddField(
            model_name='competence_relevance',
            name='minimum_required',
            field=models.IntegerField(default=0),
        ),
    ]
