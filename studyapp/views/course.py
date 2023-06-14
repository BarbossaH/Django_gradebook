from studyapp import models
from django.shortcuts import  render,redirect
from studyapp.models import Course
from django.core.exceptions import ValidationError
from studyapp.utils.bootstrap import BootStrapModelFrom
from studyapp.utils.pagination import Pagination


# Create your views here.
class CourseModelForm(BootStrapModelFrom):
    class Meta:
        model=models.Course
        fields="__all__"

    def clean_code(self):
          txt_code = self.cleaned_data["code"]
          is_exist = Course.objects.filter(code=txt_code).exists()
          if(is_exist  ):
            raise ValidationError("Course existed")
          return txt_code
    def clean_name(self):
        txt_name = self.cleaned_data['name']
        is_exist = Course.objects.filter(name=txt_name).exists()
        if is_exist:
            raise ValidationError("name existed")
        return txt_name

class CourseUpdateModelForm(BootStrapModelFrom):
    # code = forms.CharField(disabled=True)
    class Meta:
        model=models.Course
        fields="__all__"

    def clean_code(self):
        txt_code = self.cleaned_data['code']

        is_code_exist = Course.objects.filter(code=txt_code).exclude(id=self.instance.id).exists()
        if is_code_exist:
            raise ValidationError("code existed")
        return txt_code
    def clean_name(self):
        txt_name = self.cleaned_data['name']
        is_exist = Course.objects.filter(name=txt_name).exclude(id=self.instance.id).exists()
        if is_exist:
            raise ValidationError("name existed")
        return txt_name

def courseList(req):
    data_dict={}
    value = req.GET.get('q')
    if value:
        data_dict = {"code__contains":value} 
    tes = Course.objects.all()
    courseList = Course.objects.filter(**data_dict).order_by("code")
    page_object=Pagination(req,courseList)
    page_courses = page_object.page_queryset  
    page_string = page_object.html()
    return render(req, "course_list.html", {"courseList":page_courses,"page_string":page_string})

def course_add(req):
    if req.method=="GET":
     form = CourseModelForm()
     return render(req,"course_add.html",{"form":form})
    if req.method=="POST":
        form = CourseModelForm(data=req.POST)
        if form.is_valid():            
            form.save()
            return redirect('course')      
        return render(req, "course_add.html", {"form":form})

def course_delete(req,id):
    Course.objects.filter(id=id).delete()
    return redirect("course")

def course_update(req,id):
    course = Course.objects.filter(id=id).first()
    if req.method == "GET":
        form = CourseUpdateModelForm(instance=course)
        return render(req, 'course_update.html',{"form":form})
    if req.method=="POST":
        form=CourseUpdateModelForm(data=req.POST, instance=course)
        #if there is no instance, then save will add a piece of data, not update it
        # form=UserModelForm(data=req.POST) 
        if form.is_valid():
            form.save()
            return redirect('course')
        return render(req, 'course_update.html',{"form":form})
        