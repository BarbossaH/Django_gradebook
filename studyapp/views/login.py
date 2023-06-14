from django.shortcuts import redirect, render
from django import forms
from studyapp.utils.bootstrap import BootStrapFrom
from studyapp.utils.encrypt import md5
from studyapp.models import User
# Create your views here.

class LoginForm(BootStrapFrom):
    name = forms.CharField(label="Username", widget=forms.TextInput)
    password = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=True))

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

# class LoginModelForm(forms.ModelForm):
#     class Meta:
#         model = models.User
#         fields = ['username','password']


def loginSystem(req):
    
    if req.method=='POST':
        form=LoginForm(data=req.POST)
        # print("form", form.is_valid())
        if form.is_valid():
            # print(form.cleaned_data)
            user = User.objects.filter(**form.cleaned_data).first()
            # print(user)
            if not user:
                form.add_error("password","username or password incorrect")
                return render(req, 'login.html',{"form":form})
            # print("user:",user.department)
            req.session['info']={"id":user.id,"name":user.name,"department":str(user.department)}
            return redirect('userlist')
        return render(req, 'login.html',{"error_msg":"Username or password incorrect!"})
    else:
        form = LoginForm()
        return render(req, 'login.html', {"form":form})

def register(req):
    if req.method == "GET":
        print(123)
    if req.method=="POST":
        print(111)
def logout(req):
    req.session.clear()
    return redirect('/login/')
    