from studyapp import models
from django.shortcuts import  render,redirect
from studyapp.models import StudentEnrollment
from django.core.exceptions import ValidationError
from studyapp.utils.bootstrap import BootStrapModelFrom
from studyapp.utils.pagination import Pagination

# Create your views here.
class studentEnrollmentModelForm(BootStrapModelFrom):
    class Meta:
        model=models.StudentEnrollment
        fields="__all__"

    def clean_studentId(self):
          txt_studentId = self.cleaned_data["enrolled_student"]
          is_exist = StudentEnrollment.objects.filter(enrolled_student=txt_studentId).exists()
          if(is_exist  ):
            raise ValidationError("studentEnrollment existed")
          return txt_studentId

class studentEnrollmentUpdateModelForm(BootStrapModelFrom):
    class Meta:
        model=models.StudentEnrollment
        fields="__all__"

    def clean_studentId(self):
        txt_studentId = self.cleaned_data['enrolled_student']

        is_exist = StudentEnrollment.objects.filter(enrolled_student=txt_studentId).exclude(id=self.instance.id).exists()
        if is_exist:
            raise ValidationError("studentEnrollment existed")
        return txt_studentId


def studentEnrollmentList(req):
    data_dict={}
    value = req.GET.get('q')
    if value:
        data_dict = {"enrolled_student__contains":value} 
    # stu = StudentEnrollment.objects.all()
    studentEnrollmentList = StudentEnrollment.objects.filter(**data_dict).order_by("enrolled_student")
    page_object=Pagination(req,studentEnrollmentList)
    page_enrollments = page_object.page_queryset  
    page_string = page_object.html()
    return render(req, "enrollment_list.html", {"studentEnrollmentList":page_enrollments,"page_string":page_string})

def studentEnrollment_add(req):
    if req.method=="GET":
     form = studentEnrollmentModelForm()
     return render(req,"enrollment_add.html",{"form":form})
    if req.method=="POST":
        form = studentEnrollmentModelForm(data=req.POST)
        if form.is_valid():            
            form.save()
            return redirect('enrollment')      
        return render(req, "enrollment_add.html", {"form":form})

def studentEnrollment_delete(req,id):
    StudentEnrollment.objects.filter(id=id).delete()
    return redirect("enrollment")

def studentEnrollment_update(req,id):
    studentEnrollment = StudentEnrollment.objects.filter(id=id).first()
    if req.method == "GET":
        form = studentEnrollmentUpdateModelForm(instance=studentEnrollment)
        return render(req, 'enrollment_update.html',{"form":form})
    if req.method=="POST":
        form=studentEnrollmentUpdateModelForm(data=req.POST, instance=studentEnrollment)
     
        if form.is_valid():
            form.save()
            return redirect('enrollment')
        return render(req, 'enrollment_update.html',{"form":form})
        