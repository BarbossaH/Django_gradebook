# Generated by Django 4.1.7 on 2023-05-02 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyapp', '0002_administrator_class_course_studentenrollment_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_time',
            field=models.DateField(auto_now_add=True, verbose_name='Onboarding Time'),
        ),
    ]