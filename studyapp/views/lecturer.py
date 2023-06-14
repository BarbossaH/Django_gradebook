from studyapp import models
from django.shortcuts import  render,redirect
from studyapp.models import Lecturer
from django.core.exceptions import ValidationError
from studyapp.utils.bootstrap import BootStrapModelFrom
from django import forms
from studyapp.utils.pagination import Pagination

# Create your views here.
class lecturerModelForm(BootStrapModelFrom):
    class Meta:
        model=models.Lecturer
        fields="__all__"

    def clean_staffId(self):
          txt_id = self.cleaned_data["staffId"]
          is_exist = Lecturer.objects.filter(staffId=txt_id).exists()
          if(is_exist  ):
            raise ValidationError("staffId existed")
          return txt_id

class lecturerUpdateModelForm(BootStrapModelFrom):
    staffId = forms.CharField(disabled=True)    
    class Meta:
        model=models.Lecturer
        fields="__all__"

    def clean_staffId(self):
        txt_id = self.cleaned_data['staffId']

        is_exist = Lecturer.objects.filter(staffId=txt_id).exclude(id=self.instance.id).exists()
        if is_exist:
            raise ValidationError("staffId existed")
        return txt_id


def lecturerList(req):
    data_dict={}
    value = req.GET.get('q')
    if value:
        data_dict = {"staffId__contains":value} 
    lecturerList = Lecturer.objects.filter(**data_dict).order_by("staffId")
    page_object=Pagination(req,lecturerList)
    page_lecturers = page_object.page_queryset  
    page_string = page_object.html()
    return render(req, "lecturer_list.html", {"lecturerList":page_lecturers, "page_string":page_string})

def lecturer_add(req):
    if req.method=="GET":
     form = lecturerModelForm()
     return render(req,"update.html",{"form":form})
    if req.method=="POST":
        form = lecturerModelForm(data=req.POST)
        if form.is_valid():            
            form.save()
            return redirect('lecturer')      
        return render(req, "update.html", {"form":form})

def lecturer_delete(req,id):
    Lecturer.objects.filter(id=id).delete()
    return redirect("lecturer")

def lecturer_update(req,id):
    lecturer = Lecturer.objects.filter(id=id).first()
    if req.method == "GET":
        form = lecturerUpdateModelForm(instance=lecturer)
        return render(req, 'update.html',{"form":form})
    if req.method=="POST":
        form=lecturerUpdateModelForm(data=req.POST, instance=lecturer)
        #if there is no instance, then save will add a piece of data, not update it
        # form=UserModelForm(data=req.POST) 
        if form.is_valid():
            form.save()
            return redirect('lecturer')
        return render(req, 'update.html',{"form":form})
        