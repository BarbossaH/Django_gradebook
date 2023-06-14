import datetime
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

#model - 1 
class Department(models.Model):
    title = models.CharField(verbose_name="Title", max_length=30)
    def __str__(self):
        return str(self.title)
#model - 2 User
class User(models.Model):
    name = models.CharField(max_length=32,default='', validators=[RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_]*$','Only a-z and _')])
    password = models.CharField(max_length=64,default='')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='users')
    created_time = models.DateField(verbose_name="Onboarding Time", auto_now_add=True)  
    def __str__(self):
        return f"{self.department.title } {self.name}"

#model - 3 Semester

class Semester(models.Model):
      semester_choices = (   
        (1, "Spring"),
        (2, "Fall"), ) 
      id = models.AutoField(primary_key=True)
      year = models.IntegerField(default=datetime.datetime.now().year)
      semester = models.IntegerField(default=1, choices= semester_choices)

      def __str__(self):
        return f"{self.year}-{'Spring' if self.semester == 1 else 'Fall'}"
    
#model - 4 Course

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    semesters = models.ManyToManyField(Semester,  blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

#model - 5 Class
class Class(models.Model):
    number = models.IntegerField(default=1)
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
      return f"{self.number}-{self.id}-{self.semester}-{self.course}-{self.lecturer}"
    

#model - 6 Lecturer
class Lecturer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='lecturer_profile')
    staffId = models.CharField(max_length=32)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL, null=True)
    DOB = models.DateField(default=None)

    def __str__(self):
      return f"Lecturer:{self.firstname}  {self.lastname}"

#model - 7 Student
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_profile')
    studentId = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    DOB = models.DateField(default=None)
    def __str__(self):
        return f"{self.studentId}-{self.first_name} {self.last_name}"
    

#model - 8 StudentEnrollment

class StudentEnrollment(models.Model):
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrolled_student = models.ForeignKey(Student,on_delete=models.CASCADE)
    enrollTime = models.DateField(auto_now_add=True)
    gradeTime = models.DateField(null=True, blank=True)
    #grade
    mark = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
      return self.mark
    
