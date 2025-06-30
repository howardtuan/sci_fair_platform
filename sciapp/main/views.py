import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (RegistrationForm, JoinCourseForm, ProjectForm,
                    CommentForm, CourseForm, GradeForm)
from .models import Course, Project, Comment
import openai
import fitz #PyMuPDF  
from django.http import HttpResponse

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = os.getenv('OPENAI_API_KEY')
from django.contrib.auth.models import Group

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ➕ 自動加入「學生」群組
            student_group = Group.objects.get(name='學生')
            user.groups.add(student_group)

            messages.success(request, '註冊成功，請登入！')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '使用者名稱或密碼錯誤')
    return render(request, 'main/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    courses = Course.objects.all()
    return render(request, 'main/home.html', {'courses': courses})

@login_required
def join_course(request):
    if request.method == 'POST':
        form = JoinCourseForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                course = Course.objects.get(code=code)
                course.students.add(request.user)
                messages.success(request, f'已加入課程：{course.name}')
                return redirect('course_projects', course_id=course.id)
            except Course.DoesNotExist:
                messages.error(request, '課程代碼錯誤')
    else:
        form = JoinCourseForm()
    return render(request, 'main/join_course.html', {'form': form})

from django.utils.crypto import get_random_string

@login_required
def create_course(request):
    if request.method == "POST":
        name = request.POST.get("name")
        course = Course(name=name, owner=request.user)
        course.code = get_random_string(8)  # 修正這一行
        course.save()
        messages.success(request, f"課程已建立，課程代碼是 {course.code}")
        return redirect("home")
    return render(request, "main/create_course.html")


@login_required
def course_projects(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.students.all() and request.user != course.owner:
        messages.warning(request, '你尚未加入此課程')
        return redirect('home')
    projects = Project.objects.filter(course=course).order_by('-upload_time')
    return render(request, 'main/course_projects.html', {'course': course, 'projects': projects})

from .forms import ProjectForm
@login_required
def create_project(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user not in course.students.all() and request.user != course.owner:
        return HttpResponse("你沒有權限上傳這門課的專題", status=403)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.course = course
            project.author = request.user
            project.save()
            messages.success(request, "專題上傳成功！")
            return redirect("course_projects", course_id=course.id)
    else:
        form = ProjectForm()

    return render(request, "main/create_project.html", {"form": form, "course": course})


from .models import Comment
from .forms import CommentForm

from .models import Project, Comment

@login_required
def project_detail(request, project_id):
    proj = get_object_or_404(Project, id=project_id)
    comments = Comment.objects.filter(project=proj).order_by("-date_posted")

    # ✅ 加入留言權限條件
    course = proj.course
    can_comment = request.user in course.students.all() or request.user == course.owner

    # ✅ 處理留言送出
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(project=proj, user=request.user, content=content)
            messages.success(request, "留言已送出")
            return redirect("project_detail", project_id=project_id)

    return render(request, "main/project_detail.html", {
        "proj": proj,
        "comments": comments,
        "can_comment": can_comment
    })


@login_required
def comment_monitor(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.owner:
        messages.error(request, '無權限')
        return redirect('home')
    data = []
    for stu in course.students.all():
        cnt = Comment.objects.filter(user=stu).exclude(project__author=stu).count()
        data.append({'username': stu.username, 'comments': cnt})
    return render(request, 'main/comment_monitor.html', {'course': course, 'data': data})

@login_required
def grade_project(request, project_id):
    proj = get_object_or_404(Project, id=project_id)
    course = proj.course
    if request.user != course.owner:
        messages.error(request, '無權限')
        return redirect('home')

    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            criteria = form.cleaned_data['criteria']
            teacher_comment = form.cleaned_data['comment']

            # 讀取 PDF
            doc = fitz.open(proj.pdf_file.path)
            text = ""
            for page in doc:
                text += page.get_text()

            prompt = (
                f"你是一位大學助教，"
                f"專題標題：{proj.title}\n"
                f"學生報告內容如下：\n{text}\n"
                f"評分項目：{', '.join(criteria)}\n"
                f"助教補充意見：{teacher_comment}\n"
                "請根據上述內容撰寫一份約100字的中肯評語。"
            )

            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一位助教，撰寫專題評語。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            ai_comment = resp.choices[0].message.content

            proj.ai_feedback = ai_comment
            proj.save()
            messages.success(request, 'AI 評語已生成並保存')
            return redirect('project_detail', project_id=project_id)
    else:
        form = GradeForm()

    return render(request, 'main/grade_project.html', {'form': form, 'proj': proj})
