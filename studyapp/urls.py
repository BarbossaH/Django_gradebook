from django.urls import path

from studyapp.views import department,user,semester, course,login, _class, enrollment,student,lecturer,marks,upload

urlpatterns = [
    #login---------------------------------------------------
    
    path('login/', login.loginSystem, name='login'),
    path('register/', login.register, name='register'),
    path('logout/', login.logout, name='logout'),

    #department---------------------------------------------------
    path('', department.depList, name='depList'),
    path('department_add', department.department_add, name='department_add'),
    # /department/5/department_delete/
    path('department/<int:id>/department_delete/', department.department_delete, name='department_delete'),
    #Admin---------------------------------------------------
    path('userlist/user_add/', user.user_add,name='user_add'),
    path('userlist/<int:id>/user_delete/', user.user_delete,name='user_delete'),
    path('userlist/<int:id>/user_update/', user.user_update,name='user_update'),
    path('userlist/<int:id>/user_reset/', user.user_reset,name='user_reset'),
    path('userlist/', user.user_list, name='userlist'),
    path('upload/', upload.upload, name='upload'),

    #semester---------------------------------------------------
    path('semester/', semester.semesterList, name="semester"),
    path('semester/semester_add/', semester.semester_add, name="semester_add"),
    path('semester/<int:id>/semester_update/', semester.semester_update, name="semester_update"),
    path('semester/<int:id>/semester_delete/', semester.semester_delete, name="semester_delete"),
    
    #course---------------------------------------------------
    path('course/', course.courseList, name="course"),
    path('course/course_add/', course.course_add, name="course_add"),
    path('course/<int:id>/course_update/', course.course_update, name="course_update"),
    path('course/<int:id>/course_delete/', course.course_delete, name="course_delete"),


  #class---------------------------------------------------
    path('class/', _class.classList, name="class"),
    path('class/class_add/', _class.class_add, name="class_add"),
    path('class/<int:id>/class_update/', _class.class_update, name="class_update"),
    path('class/<int:id>/class_delete/', _class.class_delete, name="class_delete"),

      #lecturer---------------------------------------------------
    path('lecturer/', lecturer.lecturerList, name="lecturer"),
    path('lecturer/lecturer_add/', lecturer.lecturer_add, name="lecturer_add"),
    path('lecturer/<int:id>/lecturer_update/', lecturer.lecturer_update, name="lecturer_update"),
    path('lecturer/<int:id>/lecturer_delete/', lecturer.lecturer_delete, name="lecturer_delete"),

      #enrollment---------------------------------------------------
    path('enrollment/', enrollment.studentEnrollmentList, name="enrollment"),
    path('enrollment/studentEnrollment_add/', enrollment.studentEnrollment_add, name="studentEnrollment_add"),
    path('enrollment/<int:id>/studentEnrollment_update/', enrollment.studentEnrollment_update, name="studentEnrollment_update"),
    path('enrollment/<int:id>/studentEnrollment_delete/', enrollment.studentEnrollment_delete, name="studentEnrollment_delete"),

      #student---------------------------------------------------
    path('student/', student.studentList, name="student"),
    path('student/student_add/', student.student_add, name="student_add"),
    path('student/student_upload/', student.student_upload, name="student_upload"),
    path('student/<int:id>/student_update/', student.student_update, name="student_update"),
    path('student/<int:id>/student_delete/', student.student_delete, name="student_delete"),
      #marks---------------------------------------------------
    path('marks/', marks.marks_list, name="marks_list"),
    path('marks/<int:id>/marks_update/', marks.marks_update, name="marks_update"),
    path('marks/<int:id>/send_email/', marks.send_email, name="send_email"),

]
