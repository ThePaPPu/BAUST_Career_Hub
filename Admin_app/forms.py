
from django import forms
from django.db import transaction
from django.forms import fields
from django.contrib.auth.forms import UserCreationForm
from . models import  CustomUser, Department, Designation, Level_Term, Student, Teacher


class UserCreateForm(UserCreationForm): 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1','password2', 'department', 'phone']
    



class UserUpdateForm(forms.ModelForm): 

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','department', 'phone']

    


class StudentAddForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']


class TeacherAddForm(forms.ModelForm):
    class  Meta:
        model = Teacher
        exclude = ['user']
