from django.http import HttpResponse
from studyapp.utils.encrypt import md5
from studyapp import models
from django.shortcuts import  render,redirect
from studyapp.models import Department, Student, User
from django.core.exceptions import ValidationError
from studyapp.utils.bootstrap import BootStrapModelFrom
from django import forms
from studyapp.utils.pagination import Pagination

# Create your views here.
class studentModelForm(BootStrapModelFrom):
    class Meta:
        model=models.Student
        fields="__all__"

    def clean_studentId(self):
          txt_id = self.cleaned_data["studentId"]
          is_exist = Student.objects.filter(studentId=txt_id).exists()
          if(is_exist  ):
            raise ValidationError("student existed")
          return txt_id

class studentUpdateModelForm(BootStrapModelFrom):
    
    studentId = forms.CharField(disabled=True)
    class Meta:
        model=models.Student
        fields="__all__"

    def clean_studentId(self):
        txt_id = self.cleaned_data['studentId']

        is_exist = Student.objects.filter(studentId=txt_id).exclude(id=self.instance.id).exists()
        if is_exist:
            raise ValidationError("Student Id existed")
        return txt_id


def studentList(req):
    data_dict={}
    value = req.GET.get('q')
    if value:
        data_dict = {"studentId__contains":value} 
    
    from django.db.models import IntegerField, CharField
    from django.db.models.functions import Cast
    studentList = Student.objects.filter(**data_dict).annotate(student_id_int=Cast('studentId', IntegerField())).order_by('student_id_int')

    # studentList = Student.objects.filter(**data_dict).order_by("studentId")

    page_object=Pagination(req,studentList)
    page_students = page_object.page_queryset  
    page_string = page_object.html()
    return render(req, "student_list.html", {"studentList":page_students, "page_string":page_string})

def student_add(req):
    if req.method=="GET":
       form = studentModelForm()
       return render(req,"update.html",{"form":form})
    if req.method=="POST":
        form = studentModelForm(data=req.POST)
        if form.is_valid():            
            form.save()
            return redirect('student')      
        return render(req, "update.html", {"form":form})

def student_delete(req,id):
    Student.objects.filter(id=id).delete()
    return redirect("student")

def student_update(req,id):
    student = Student.objects.filter(id=id).first()
    if req.method == "GET":
        form = studentUpdateModelForm(instance=student)
        return render(req, 'update.html',{"form":form})
    if req.method=="POST":
        form=studentUpdateModelForm(data=req.POST, instance=student)
        #if there is no instance, then save will add a piece of data, not update it
        # form=UserModelForm(data=req.POST) 
        if form.is_valid():
            form.save()
            return redirect('student')
        return render(req, 'update.html',{"form":form})
    


from openpyxl import load_workbook
def student_upload(req):
    if req.method == 'POST' and req.FILES.get('file'):
        file = req.FILES.get('file')
        wb = load_workbook(file)
        sheet = wb.worksheets[0]
        data = list(sheet.values)
        department=None
        try:
            department = Department.objects.get(title="student")
        except:
            print("An exception occurred, but the program will continue to run.")
        # print(department, 'this is aadss')
        if not department:
            department = Department.objects.create(title='student')
        # print(department)

        headers = data[0]
        for row in data[1:]:
            student= Student()
            is_row_invalid=False
            #to judge this row exists or not
            for col_idx, col_value in enumerate(row):
                if headers[col_idx]=="user" :
                    # print(col_value,"doaisjdsaodjsaodij")
                    if col_value==None or User.objects.filter(name=col_value).exists():
                        is_row_invalid=True
                        break
            # print(is_row_exist,"1111111")
            if(not is_row_invalid):
                for col_idx, col_value in enumerate(row):
                    if headers[col_idx]=="user":
                        user=User.objects.create(name=col_value,password=md5("000000"),department=department)
                        col_value=user
                    setattr(student, headers[col_idx], col_value)
                student.save()
    return redirect("student")
    # return HttpResponse('Data imported successfully!')
   

