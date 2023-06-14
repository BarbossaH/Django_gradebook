from studyapp import models
from django.shortcuts import  render,redirect
from studyapp.models import Class
from django.core.exceptions import ValidationError
from studyapp.utils.bootstrap import BootStrapModelFrom
from studyapp.utils.pagination import Pagination

# Create your views here.
class classModelForm(BootStrapModelFrom):
    class Meta:
        model=models.Class
        fields="__all__"

    def clean_id(self):
          txt_id = self.cleaned_data["id"]
          is_exist = Class.objects.filter(id=txt_id).exists()
          if(is_exist  ):
            raise ValidationError("class existed")
          return txt_id

class classUpdateModelForm(BootStrapModelFrom):
    class Meta:
        model=models.Class
        fields="__all__"

    def clean_id(self):
        txt_id = self.cleaned_data["id"]
        is_id_exist = Class.objects.filter(id=txt_id).exclude(id=self.instance.id).exists()
        if is_id_exist:
            raise ValidationError("the class has existed")
        return txt_id


def classList(req):
    data_dict={}
    value = req.GET.get('q')
    if value:
        data_dict = {"number__contains":value} 
    classList = Class.objects.filter(**data_dict).order_by("number")
    page_object=Pagination(req,classList)
    page_classes = page_object.page_queryset  
    page_string = page_object.html()
    return render(req, "class_list.html", {"classList":page_classes,"page_string":page_string})

def class_add(req):
    if req.method=="GET":
     form = classModelForm()
     return render(req,"class_add.html",{"form":form})
    if req.method=="POST":
        form = classModelForm(data=req.POST)
        if form.is_valid():            
            form.save()
            return redirect('class')      
        return render(req, "class_add.html", {"form":form})

def class_delete(req,id):
    Class.objects.filter(id=id).delete()
    return redirect("class")

def class_update(req,id):
    _class = Class.objects.filter(id=id).first()
    if req.method == "GET":
        form = classUpdateModelForm(instance=_class)
        return render(req, 'class_update.html',{"form":form})
    if req.method=="POST":
        form=classUpdateModelForm(data=req.POST, instance=_class)
        #if there is no instance, then save will add a piece of data, not update it
        # form=UserModelForm(data=req.POST) 
        if form.is_valid():
            form.save()
            return redirect('class')
        return render(req, 'class_update.html',{"form":form})
        