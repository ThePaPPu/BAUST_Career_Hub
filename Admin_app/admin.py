from django.contrib import admin
from .models import Student, Teacher, CustomUser, Department, Level_Term, Designation, Follow

# from django.contrib.auth.admin import UserAdmin




# # admin.site.register(CustomUser, UserAdmin)



admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Level_Term)
admin.site.register(Follow)
