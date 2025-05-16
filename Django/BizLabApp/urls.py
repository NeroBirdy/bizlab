from django.urls import path
from .views import Registration, Login, Logout, downloadFile, uploadFile, createCourse, getCoursesForTeacher, createMaterial, getUsersByCourse, createTask, inviteUserOnCourse, getFilesForTeacher
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import re_path

urlpatterns = [
    path('auth/registration', Registration.as_view(), name='registration'),
    path('auth/login', Login.as_view(), name='login'),
    path('auth/logout', Logout.as_view(), name='logout'),
    path('download', downloadFile.as_view(), name='downloadFile'),
    path('upload', uploadFile.as_view(), name='uploadFile'),
    path('createCourse', createCourse.as_view(), name='createCourse'),
    path('createTask', createTask.as_view(), name='createTask'),
    path('createMaterial', createMaterial.as_view(), name='createMaterial'),
    path('getCoursesForTeacher', getCoursesForTeacher.as_view(), name='getCoursesForTeacher'),
    path('getUsersByCourse', getUsersByCourse.as_view(), name='getUsersByCourse'),
    path('inviteUserOnCourse', inviteUserOnCourse.as_view(), name='inviteUserOnCourse'),
    path('homework', getFilesForTeacher.as_view(), name='getFilesForTeacher'),
]