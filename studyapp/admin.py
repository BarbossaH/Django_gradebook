from django.contrib import admin

from .models import Department,  Semester,User,Class, Student,StudentEnrollment, Lecturer, Course
# Register your models here.
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Semester)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(StudentEnrollment)
admin.site.register(Lecturer)
admin.site.register(Course)