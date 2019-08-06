# Generated by Django 2.2.1 on 2019-08-05 12:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20190805_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='employee_history',
            fields=[
                ('id_employee_history', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.IntegerField()),
                ('dateOfChange', models.DateField(default=django.utils.timezone.now)),
                ('id_competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.competence')),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.employee')),
            ],
        ),
    ]