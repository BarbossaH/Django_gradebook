# Generated by Django 4.1.7 on 2023-05-04 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studyapp', '0012_remove_student_studentenrollment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentenrollment',
            name='grade',
        ),
    ]
