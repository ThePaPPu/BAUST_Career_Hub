from django.conf import settings
from .models import CustomUser, Department, Designation, Level_Term, Student, Teacher, Follow
from django.http import HttpResponse, HttpResponseRedirect, response
from django.contrib import messages
from django.urls import reverse
from .forms import   UserCreateForm,StudentAddForm, TeacherAddForm, UserUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, CreateView
from post.models import Post
from django.db import transaction


User = settings.AUTH_USER_MODEL 


def index(request):
    return render(request, 'Admin_app/index.html')

def team(request):
    return render(request, 'Admin_app/team.html')

def about(request):
    return render(request, 'Admin_app/about.html')

def student_signup(request):
    user_form = UserCreateForm()
    student_form = StudentAddForm()
    return render(request, 'Admin_app/StudentSignUp.html', {"user_form": user_form, "student_form": student_form}) 


def teacher_signup(request):
    user_form = UserCreateForm()
    teacher_form = TeacherAddForm()
    return render(request, 'Admin_app/TeacherSignUp.html', {"user_form": user_form, "teacher_form": teacher_form})

# follow function 
class FollowDoneView(View):
    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get('followed_user_id')
        followed_user_obj = CustomUser.objects.get(pk=followed_user_id)

        try:
            Follow.objects.get(user=request.user, followed=followed_user_obj, follow_status=True)
        except Exception as e:
            follow_obj = Follow.objects.create(followed=followed_user_obj)

        return redirect(request.META.get('HTTP_REFERER'))


class UnfollowDoneView(View):
    def post(self, request, *args, **kwargs):
        unfollowed_user_id = request.POST.get('unfollowed_user_id')
        unfollowed_user_obj = CustomUser.objects.get(pk=unfollowed_user_id)

        try:
            follow_obj = Follow.objects.get(user=request.user, followed=unfollowed_user_obj)
            follow_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))


def student_signup_save(request):
    user_form = UserCreateForm()
    student_form = StudentAddForm()

    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        student_form = StudentAddForm(request.POST)
        
        if user_form.is_valid() and student_form.is_valid():
            with transaction.atomic():
                user_obj = user_form.save(commit=False)
                user_obj.is_student = True
                user_obj.save()
                print(user_obj)
                student_obj = student_form.save(commit = False)
                
                student_obj.user = user_obj
                student_obj.save()
                return redirect('signin')
        else:
            return render(request, 'Admin_app/StudentSignUp.html', {'user_form': user_form,'student_form':student_form})
        
        
    return render(request, 'Admin_app/StudentSignUp.html', {'user_form': user_form,'student_form':student_form})
    


def teacher_signup_save(request):
    user_form = UserCreateForm()
    teacher_form = TeacherAddForm()

    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        teacher_form = TeacherAddForm(request.POST)
        
        if user_form.is_valid() and teacher_form.is_valid():
            user_obj = user_form.save(commit=False)
            teacher_obj = teacher_form.save(commit = False)
            user_obj.is_teacher = True
            user_obj.save()

            teacher_obj.user = user_obj
            teacher_obj.save()
            return redirect('signin')
        else:
            return render(request, 'Admin_app/TeacherSignUp.html', {'user_form': user_form,'teacher_form':teacher_form})
        
    return render(request, 'Admin_app/TeacherSignUp.html', {'user_form': user_form,'teacher_form':teacher_form})             


                
#with user type
def user_signin(request):
    if request.user.is_active:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_student:
                return redirect('student_home')
            elif user.is_teacher:
                return redirect('teacher_home')
            elif user.is_superuser:
                return redirect('admin_home')
            
        else:
            messages.info(request, f'account done not exit plz sign in')
    return render(request, "Admin_app/Login.html")



def user_logout(request):
    logout(request)
    return HttpResponseRedirect("user_signin")


@login_required(login_url='signin')  
def student_home(request):
    if request.user.is_student:
        all_user = CustomUser.objects.all()
        posts = Post.objects.all()
        return render(request, 'Admin_app/Student/StudentHome.html', {'posts': posts, 'all_user':all_user})
        # return render(request, 'Admin_app/Student/StudentHome.html')
    else:
        return HttpResponse('You are not as Student!')



@login_required(login_url='signin')  
def admin_home(request):
    if request.user.is_superuser:
        return render(request, 'Admin_app/Admin/AdminHome.html')
    else:
        return HttpResponse('You are not as Admin!')



@login_required(login_url='signin')  
def teacher_home(request):
    if request.user.is_teacher:
        all_user = CustomUser.objects.all()
        posts = Post.objects.all()
        return render(request, 'Admin_app/Teacher/TeacherHome.html', {'posts': posts, 'all_user':all_user})
       
    else:
        return HttpResponse('You are not as Teacher!')

@login_required(login_url='signin')  
def Add_Department(request):
    return render(request, 'Admin_app/Admin/Add_Department.html')



def Add_Department_Save(request):
    if request.method == "POST":
        department = request.POST.get("department_name")

        try:
            dept_model = Department(department_name=department)
            dept_model.save()
            messages.success(request, "Successfully Added Department")
            return HttpResponseRedirect(reverse("add_department"))
        except:
            messages.error(request, "Failed to Add Department")
            return HttpResponseRedirect(reverse("add_department"))
    
    else:
        return HttpResponse("Method not allowed")


@login_required(login_url='signin')  
def Manage_Department(request):
    department = Department.objects.all()
    return render(request, "Admin_app/Admin/Manage_Department.html", {"department": department})




@login_required(login_url='signin')  
def Manage_Student(request):
    students = Student.objects.all()
    # print(students[0].id)
    return render(request, "Admin_app/Admin/Manage_Student.html", {"students": students})



@login_required(login_url='signin')  
def Manage_Teacher(request):
    teacher = Teacher.objects.all()
    return render(request, "Admin_app/Admin/Manage_Teacher.html", {"teacher": teacher})



@login_required(login_url='signin')  
def Add_Designation(request):
    return render(request, 'Admin_app/Admin/Add_Designation.html')



def Add_Designation_Save(request):
    if request.method == "POST":
        designation = request.POST.get("designation_name")
        try:
            designation_model = Designation(designation_name=designation)
            designation_model.save()
            messages.success(request, "Successfully Added Designation")
            return HttpResponseRedirect(reverse("add_designation"))
        except:
            messages.error(request, "Failed to Add Designation")
            return HttpResponseRedirect(reverse("add_designation"))
    
    else:
        return HttpResponse("Method not allowed")


@login_required(login_url='signin')  
def Manage_Designation(request):
    designation = Designation.objects.all()
    return render(request, "Admin_app/Admin/Manage_Designation.html", {"designation": designation})



@login_required(login_url='signin')  
def Add_Level_Term(request):
    return render(request, 'Admin_app/Admin/Add_Level_Term.html')



def Add_Level_Term_Save(request):
    if request.method == "POST":
        level_term_name = request.POST.get("level_term_name")

        try:
            level_term_model = Level_Term(level_term_name=level_term_name)
            level_term_model.save()
            messages.success(request, "Successfully Added Level-Term")
            return HttpResponseRedirect(reverse("add_level_term"))
        except:
            messages.error(request, "Failed to Add Level-Term")
            return HttpResponseRedirect(reverse("add_level_term"))
    
    else:
        return HttpResponse("Method not allowed")


@login_required(login_url='signin')  
def Manage_Level_Term(request):
    level_term = Level_Term.objects.all()
    return render(request, "Admin_app/Admin/Manage_Level_term.html", {"level_term": level_term})



def add_student_from_admin(request):
    user_form = UserCreateForm()
    student_form = StudentAddForm()

    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        student_form = StudentAddForm(request.POST)
        
        if user_form.is_valid() and student_form.is_valid():
            user_obj = user_form.save(commit=False)
            student_obj = student_form.save(commit = False)
            user_obj.is_student = True
            user_obj.save()

            student_obj.user = user_obj
            student_obj.save()
            return redirect('manage_student')
        else:
            return render(request, 'Admin_app/Admin/Add_Student.html', {'user_form': user_form,'student_form':student_form})
        
        
    return render(request, 'Admin_app/Admin/Add_Student.html', {'user_form': user_form,'student_form':student_form})
            
            

    


def add_teacher_from_admin(request):
    user_form = UserCreateForm()
    teacher_form = TeacherAddForm()

    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        teacher_form = TeacherAddForm(request.POST)
        
        if user_form.is_valid() and teacher_form.is_valid():
            user_obj = user_form.save(commit=False)
            teacher_obj = teacher_form.save(commit = False)
            user_obj.is_teacher = True
            user_obj.save()

            teacher_obj.user = user_obj
            teacher_obj.save()
            return redirect('manage_teacher')
        else:
            return render(request, 'Admin_app/Admin/Add_Teacher.html', {'user_form': user_form,'teacher_form':teacher_form})
        
        
    return render(request, 'Admin_app/Admin/Add_Teacher.html', {'user_form': user_form,'teacher_form':teacher_form})

@login_required(login_url='signin')  
def student_details(request, id):
    data = Student.objects.get(id = id)
    context = {'data': data}
    return render(request, 'Admin_app/Admin/Student_details.html', context)


def student_update(request, id):
    student =get_object_or_404(Student, id=id)
    user_form = UserUpdateForm(instance = student.user)
    student_form = StudentAddForm(instance = student)
    return render(request, 'Admin_app/Admin/Update_student.html', {'user_form':user_form, 'student_form':student_form, 'student':student})

def student_update_save(request,id):
    student = get_object_or_404(Student,id=id)
    user_form = UserUpdateForm(request.POST or None, instance = student.user)
    student_form = StudentAddForm(request.POST or None, instance = student)
    
    if user_form.is_valid() and student_form.is_valid():
        user_obj = user_form.save()
        student_obj = student_form.save()
        #student_obj.user = user_obj # no need assign user again in update user remain same
        #student_obj.save()
        return redirect('manage_student')
        
    else:
        return render(request, 'Admin_app/Admin/Add_Student.html', {'user_form': user_form,'student_form':student_form})
        


def student_delete(request, id):
    data = Student.objects.get(id=id)
    data.delete()
    return redirect('manage_student')


def teacher_details(request, id): 
    data = Teacher.objects.get(id = id)
    context = {'data': data}
    return render(request, 'Admin_app/Admin/Teacher_details.html', context)

def teacher_update(request, id):
    teacher =get_object_or_404(Teacher, id=id)
    user_form = UserUpdateForm(instance = teacher.user)
    teacher_form = TeacherAddForm(instance = teacher)
    return render(request, 'Admin_app/Admin/Update_Teacher.html', {'user_form':user_form, 'teacher_form':teacher_form, 'teacher':teacher})

def teacher_update_save(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    user_form = UserUpdateForm(request.POST or None, instance = teacher.user)
    teacher_form = TeacherAddForm(request.POST or None, instance = teacher)

    print("teacher upd")
    
    if user_form.is_valid() and teacher_form.is_valid():
        user_obj = user_form.save()
        teacher_obj = teacher_form.save()
        # teacher_obj.user = user_obj
        # teacher_obj.save()
        return redirect('manage_teacher')
        
    else:
        print(user_form.errors,teacher_form.errors)
        return render(request, 'Admin_app/Admin/Update_Teacher.html', {'user_form': user_form,'teacher_form':teacher_form})


def teacher_delete(request, id):
    data = Teacher.objects.get(id=id)
    data.delete()
    return redirect('manage_teacher')


def department_delete(request, id):
    data = Department.objects.get(id=id)
    data.delete()
    return redirect('manage_department')



def designation_delete(request, id):
    data = Designation.objects.get(id=id)
    data.delete()
    return redirect('manage_designation')


def level_term_delete(request, id):
    data = Level_Term.objects.get(id=id)
    data.delete()
    return redirect('manage_level_term')


class student_profile(View):
    template_name_anon = 'Admin_app/profile.html'
    template_name_auth = 'Admin_app/Student/student_profile.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            posts = Post.objects.filter(user=user)
            # student = Student.objects.get(user = user)
        except Exception as e:
            return HttpResponse('<h1>This page does not exist.</h1>')

        
        if username == request.user.username:
            context = { 'user': user, 'posts':posts, }
            return render(request, self.template_name_auth, context=context)
        else:
            try:
                Follow.objects.get(user=request.user, followed=user)
                is_follows_this_user = True
            except Exception as e:
                is_follows_this_user = False
                    
            context = { 'user': user, 'posts':posts,  'is_follows_this_user': is_follows_this_user }
            return render(request, self.template_name_anon, context=context)

class teacher_profile(View):
    template_name_anon = 'Admin_app/profile.html'
    template_name_auth = 'Admin_app/Teacher/teacher_profile.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            posts = Post.objects.filter(user=user)
        except Exception as e:
            return HttpResponse('<h1>This page does not exist.</h1>')

        
        if username == request.user.username:
            context = { 'user': user, 'posts':posts, }
            return render(request, self.template_name_auth, context=context)
        else:
            try:
                Follow.objects.get(user=request.user, followed=user)
                is_follows_this_user = True
            except Exception as e:
                is_follows_this_user = False
                    
            context = { 'user': user, 'posts':posts, 'is_follows_this_user': is_follows_this_user }
            return render(request, self.template_name_anon, context=context)


def back(request):
    return HttpResponseRedirect('/')