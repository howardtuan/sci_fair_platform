from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('join/', views.join_course, name='join_course'),
    path('course/<int:course_id>/projects/', views.course_projects, name='course_projects'),
    path('course/<int:course_id>/upload/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),

    # 助教功能
    path('course/create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/monitor/', views.comment_monitor, name='comment_monitor'),
    path('project/<int:project_id>/grade/', views.grade_project, name='grade_project'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)