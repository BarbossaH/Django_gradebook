from django.shortcuts import redirect, render
from studyapp import models
from studyapp.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from studyapp.utils.bootstrap import BootStrapModelFrom
from studyapp.utils.pagination import Pagination
from studyapp.utils.encrypt import md5 
# Create your views here.

#-----------------------------user-----------------------------------------
class UserModelForm(BootStrapModelFrom):
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=models.User
        fields= ["name","password","confirm_password", "department"]
        widgets={
            "password":forms.PasswordInput(render_value=True),
            # "name":forms.TextInput(attrs={"class":"form-control"}),
        }
        # fields="__all__"
        # exclude = ['name']
    def clean_name(self):
        txt_name = self.cleaned_data['name']
        is_exist = User.objects.filter(name=txt_name).exists()
        if is_exist:
            raise ValidationError("name existed")
        return txt_name
    

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm= md5(self.cleaned_data.get("confirm_password"))
        print("this is encrypted password",confirm)
        if confirm!=pwd:
            raise ValidationError("The passwords are not consistent.")
        return confirm



def user_list(req):

    #id=1
    #id__gt=1
    #id__gte=1
    #id__lte=1
    #name__startswith="a" 以某字符开头
    #name__endswith="a"
    #name__contains="abc"
    #name="abc"
    # data_dict = {"name__contains":"a"}
    # for i in range(5):
    #     User.objects.create(name="test", password="123",age=11,  gender=1, created_time="2023-4-5")

    
    # print(req.session.get("info"))
    # if not req.session.get("info"):
    #     return redirect("login")


    data_dict={}
    value = req.GET.get('q')
    if value:
        data_dict = {"name__contains":value}
    
    #add some data for the pagination test
    # for i in range(101):
    #     models.User.objects.create(name="Julian"+str(i),password="123")
    # users = User.objects.filter(**data_dict)
    #------------------------------------------------
    # this section is just for testing the relate_name
    # user = User.objects.get(id=1)  # 获取一个User对象
    # student = user.student_profile  # 通过related_name获取对应的Student对象
    # print(student.first_name)

    users = User.objects.filter(**data_dict).order_by("id")

    page_object=Pagination(req,users)
    page_users = page_object.page_queryset  
    page_string = page_object.html()

    # users = User.objects.all()
    # print(users)
    return render(req, 'user_list.html',{"users":page_users, "page_string":page_string})

def user_add(req):
    if req.method=="GET":
    #    print(req.GET)  
        # context={'gender':models.User.gender_choices, 'department':models.Department.objects.all()}   
        form = UserModelForm()
        return render(req,'user_add.html',{"form":form})
    if req.method=='POST': 
        form = UserModelForm(data=req.POST)
        if form.is_valid():            
            # User.objects.create(name=username,password=pwd, age=age)
            form.save()
            return redirect('userlist')      
        return render(req, "user_add.html", {"form":form})
    

def user_delete(req,id):
    # userId = req.GET.get('id')
    User.objects.filter(id=id).delete()
    return redirect('userlist')

class UserEditModelForm(BootStrapModelFrom):
    #not allowed to change the name
    # name = forms.CharField(disabled=True)
    # password = forms.CharField(validators=[RegexValidator(r'^\w+$', "Only letter and number")])
    class Meta:
        model=models.User
        fields= ["name"]
        # fields="__all__"
        # exclude = ['name']


    def clean_name(self):
        txt_name = self.cleaned_data['name']
        is_exist = User.objects.filter(name=txt_name).exclude(id=self.instance.id).exists()
        if is_exist:
            raise ValidationError("name existed")
        return txt_name
    

class AdminRestModelForm(BootStrapModelFrom):
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.User
        fields= ['password','confirm_password']
        widgets={
            "password":forms.PasswordInput(render_value=True),
        }        
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        encrypted_pwd = md5(pwd)
        is_exist=User.objects.filter(id=self.instance.pk, password=encrypted_pwd)
        if is_exist:
            raise ValidationError("The new password cannot be same as the existing password")
        return encrypted_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm= md5(self.cleaned_data.get("confirm_password"))
        print("this is encrypted password",confirm)
        if confirm!=pwd:
            raise ValidationError("The passwords are not consistent.")
        return confirm

def user_reset(req,id):
    user = User.objects.filter(id=id).first()
    if not user:
        return redirect('userlist')
    title = "Reset Password---{}".format(user.name)
    if req.method == "GET":
        form = AdminRestModelForm( )
        return render(req,'update.html', {"form":form,"title":title})
    
    form = AdminRestModelForm(data=req.POST,instance = user )
    if form.is_valid():
        form.save()
        return redirect('userlist')
    return render(req,'update.html', {"form":form,"title":title})



def user_update(req, id):
    user = User.objects.filter(id=id).first()
    if not user:
        return redirect('userlist')
    if req.method == "GET":
        form = UserEditModelForm(instance=user)
        return render(req, 'user_update.html',{"form":form})
    if req.method=="POST":
        form=UserEditModelForm(data=req.POST, instance=user)
        #if there is no instance, then save will add a piece of data, not update it
        # form=UserModelForm(data=req.POST) 
        if form.is_valid():
            form.save()
            return redirect('userlist')
        return render(req, 'user_update.html',{"form":form})
    