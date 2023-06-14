from studyapp import models
from django.shortcuts import  render,redirect
from studyapp.models import Semester
from django.core.exceptions import ValidationError
from studyapp.utils.pagination import Pagination

from studyapp.utils.bootstrap import BootStrapModelFrom

# Create your views here.
class SemesterModelForm(BootStrapModelFrom):
    class Meta:
        model=models.Semester
        # fields= ["id","year","semester"]
        fields="__all__"
    def clean_year(self):
        txt_year = self.cleaned_data["year"]
        self.is_year_exist = Semester.objects.filter(year=txt_year).exists()
        return txt_year
    def clean_semester(self):
          txt_semester = self.cleaned_data["semester"]
          is_semester_exist = Semester.objects.filter(semester=txt_semester).exists()
          if(self.is_year_exist and is_semester_exist):
            raise ValidationError("semester existed")
          return txt_semester
class SemesterUpdateModelForm(BootStrapModelFrom):
    class Meta:
        model=models.Semester
        fields="__all__"

    def clean_year(self):
        txt_year = self.cleaned_data["year"]
        self.is_year_exist = Semester.objects.filter(year=txt_year).exclude(id=self.instance.id).exists()
        return txt_year
    def clean_semester(self):
          txt_semester = self.cleaned_data["semester"]
          is_semester_exist = Semester.objects.filter(semester=txt_semester).exclude(id=self.instance.id).exists()
          if(self.is_year_exist and is_semester_exist):
            raise ValidationError("semester existed")
          return txt_semester
    
def semesterList(req):
    # semesterList = Semester.objects.all()
    # return render(req, "semester.html", {"semesterList":semesterList})
    data_dict={}
    value = req.GET.get('q')
    if value:
        data_dict = {"year__contains":value}
  
    semesterList = Semester.objects.filter(**data_dict).order_by("year")
    page_object=Pagination(req,semesterList)
    page_semesters = page_object.page_queryset  
    page_string = page_object.html()
    return render(req, "semester_list.html", {"semesterList":page_semesters,"page_string":page_string})

def semester_add(req):
    if req.method=="GET":
     form = SemesterModelForm()
     return render(req,"semester_add.html",{"form":form})
    if req.method=="POST":
        form = SemesterModelForm(data=req.POST)
        if form.is_valid():            
            form.save()
            return redirect('semester')      
        return render(req, "semester_add.html", {"form":form})

def semester_delete(req,id):
    Semester.objects.filter(id=id).delete()
    return redirect("semester")

def semester_update(req,id):
    semester = Semester.objects.filter(id=id).first()
    if req.method == "GET":
        form = SemesterUpdateModelForm(instance=semester)
        return render(req, 'semester_update.html',{"form":form})
    if req.method=="POST":
        form=SemesterUpdateModelForm(data=req.POST, instance=semester)
        #if there is no instance, then save will add a piece of data, not update it
        # form=UserModelForm(data=req.POST) 
        if form.is_valid():
            form.save()
            return redirect('semester')
        return render(req, 'semester_update.html',{"form":form})
        