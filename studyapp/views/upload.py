from django.http import HttpResponse
from django.shortcuts import  render,redirect

def upload(req):

    if(req.method=="GET"):
      return render(req,"upload_list.html")
    if(req.method=="POST"):
      # print(req.POST,"123")
      # print(req.FILES,"fdsfdsfsd")
      file_object = req.FILES.get("file")
      # print(file_object.name)
      f = open(file_object.name, mode='wb')
      for chunk in file_object.chunks():
         f.write(chunk)
      f.close()
      return HttpResponse("POST")
