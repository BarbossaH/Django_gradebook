# Generated by Django 4.1.7 on 2023-05-04 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studyapp', '0010_lecturer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='mark',
        ),
        migrations.RemoveField(
            model_name='studentenrollment',
            name='classId',
        ),
        migrations.RemoveField(
            model_name='studentenrollment',
            name='studentId',
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='enrolled_student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='studyapp.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='mark',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]