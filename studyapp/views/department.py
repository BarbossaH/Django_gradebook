from django.shortcuts import redirect, render
from studyapp.models import Department

# Create your views here.


#-----------------------------Department-----------------------------------------
def depList(req):
    depList = Department.objects.all()
    # print(depList)
    return render(req, 'department.html', {"depList":depList})

def department_add(req):
    if req.method == "GET":
        return render(req, 'department_add.html')
    if req.method =="POST":
        # print(req.POST)
        title = req.POST.get('title')
        Department.objects.create(title=title.lower())
        return redirect('depList')
def department_delete(req,id):
    # print(12321321321321321321)
    # userId = req.GET.get('id')
    Department.objects.filter(id=id).delete()
    return redirect('depList')