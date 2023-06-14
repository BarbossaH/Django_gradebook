from django.middleware.common import MiddlewareMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class AdminAuth(MiddlewareMixin):
    def process_request(self, request):
        # return
        
        print(request.user)
        if request.path_info=="/login/":
            return
        if request.user=="Julian":
            return
        info_dict = request.session.get('info')
        if not info_dict:
            return redirect('/login/')
        if (info_dict.get("department").lower()=="admin"):
            return
        if (info_dict.get("department").lower()=="student" or info_dict.get("department").lower()=="lecturer") and request.path_info.startswith("/marks/"):
             return
        if (info_dict.get("department").lower()=="student" or info_dict.get("department").lower()=="lecturer"):
            return redirect("/marks/")
   
        return redirect('/login/')
    
    def process_response(self,request, response):
        # print("I am out")
        return response


# class UserRoleMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # 从session中读取"user_role"字段
#         user_role = request.session.get('user_role', None)

#         # 根据"user_role"字段的值来判断用户的访问权限
#         if user_role == 'admin':
#             # 如果用户的角色为"admin"，则拥有全部权限，可以直接访问页面
#             print("I am admin")
#             pass
#         elif user_role == 'lecturer':
#             print("I am lecturer")

#             # 如果用户的角色为"lecturer"，则只能访问特定页面
#             if request.path != '/lecturer_page':
#                 return HttpResponseForbidden('Access Denied')
#         elif user_role == 'student':
#             print("I am student")

#             # 如果用户的角色为"student"，则只能访问特定页面
#             if request.path != '/student_page':
#                 return HttpResponseForbidden('Access Denied')

#         response = self.get_response(request)

#         return response
