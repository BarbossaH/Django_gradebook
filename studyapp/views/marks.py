from django import forms
from django.http import HttpResponse
from django.shortcuts import  render,redirect
from studyapp import models

from studyapp.models import StudentEnrollment, Student
from studyapp.utils.bootstrap import BootStrapModelFrom
from studyapp.utils.pagination import Pagination

class markUpdateModelForm(BootStrapModelFrom):
    
    # last_name = forms.CharField(disabled=True)
    # mark = forms.CharField(disabled=True)
    class Meta:
        model=models.StudentEnrollment
        fields=["mark"]
        # fields="__all__"

    
def marks_list(req):
    studentList = StudentEnrollment.objects.all()
    # user = User.objects.filter()
    # studentList = StudentEnrollment.objects.filter(enrolled_student=)
    # print(req.session['info'].get("department"))
    # department=''
    department=req.session['info'].get('department')       
    page_object=Pagination(req,studentList)
    page_students = page_object.page_queryset
    page_string = page_object.html()
    return render(req, "marks.html", {"studentList":page_students, "page_string":page_string,"department":department})

def marks_update(req,id):
    studentEnroll = StudentEnrollment.objects.filter(id=id).first()
    if req.method == "GET":
        form = markUpdateModelForm(instance=studentEnroll)
        return render(req, 'marks_update.html',{"form":form})
    if req.method=="POST":
        form=markUpdateModelForm(data=req.POST, instance=studentEnroll)

        #if there is no instance, then save will add a piece of data, not update it
        # form=UserModelForm(data=req.POST) 
        if form.is_valid():
            form.save()
            return redirect('marks_list')
        return render(req, 'marks_update.html',{"form":form})
    return render(req,"marks_update.html")


#send email
from django.core.mail import send_mail
from django.contrib import messages

def send_email(req, id):
    studentEnroll = StudentEnrollment.objects.filter(id=id).first()
    
    if not studentEnroll:
        messages.error("there is no this student")

    # print(student.first_name)
    # print(student.last_name)

    student_email = studentEnroll.enrolled_student.email
    subject = "Your Grade is Available"
    message = f"Dear {studentEnroll.enrolled_student},\n\nYour grade for {studentEnroll.mark} is now available. "
    from_email = None  # Uses the default email in settings.py

    try:
        send_mail(subject, message, from_email, [student_email])
        messages.success(req, f"Email sent to {studentEnroll}.")
    except Exception as e:
        messages.error(req, str(e))
    
    return HttpResponse("Email has sent")
    return redirect('marks_list')

