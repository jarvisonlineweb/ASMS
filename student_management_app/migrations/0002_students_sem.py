# Generated by Django 4.1.3 on 2022-11-20 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='sem',
            field=models.CharField(default='Sem 1', max_length=50),
        ),
    ]
