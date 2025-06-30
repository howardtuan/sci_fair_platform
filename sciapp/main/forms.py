from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Comment, Course

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class JoinCourseForm(forms.Form):
    code = forms.CharField(max_length=20)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'video_url', 'pdf_file', 'github_url']

# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': '輸入留言...'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class GradeForm(forms.Form):
    DESIGN_CHOICES = [
        ('美編設計', '美編設計'),
        ('表達清晰', '表達清晰'),
        ('內容深度', '內容深度'),
        ('創意', '創意'),
    ]
    criteria = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple,
        choices=DESIGN_CHOICES
    )
    comment = forms.CharField(widget=forms.Textarea, required=False)
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'video_url', 'pdf_file', 'github_url']
