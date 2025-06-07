from django.urls import path
from .views import Registration, Login, Logout, welcomeToTeacher, parseFile, downloadFile, getTeachers, deleteTeacher, createComment, getFeedback, getCourseForMain, sendEmailToAdmin, getUser, getCourseByUser, getDoneUserProgress, getCourseForUser, checked, getCourseForTeacher, updateLesson, updateMaterial, uploadFile, createCourse, getCoursesForTeacher, createMaterial, getUsersByCourse, createTask, inviteUserOnCourse, getFilesForTeacher
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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('download', downloadFile.as_view(), name='downloadFile'),
    path('upload', uploadFile.as_view(), name='uploadFile'),
    path('createCourse', createCourse.as_view(), name='createCourse'),
    path('createTask', createTask.as_view(), name='createTask'),
    path('createMaterial', createMaterial.as_view(), name='createMaterial'),
    path('getCoursesForTeacher', getCoursesForTeacher.as_view(), name='getCoursesForTeacher'),
    path('getUsersByCourse', getUsersByCourse.as_view(), name='getUsersByCourse'),
    path('inviteUserOnCourse', inviteUserOnCourse.as_view(), name='inviteUserOnCourse'),
    path('homework', getFilesForTeacher.as_view(), name='getFilesForTeacher'),
    path('homework/checked', checked.as_view(), name='checked'),
    path('getCourseForTeacher', getCourseForTeacher.as_view(), name='getCourseForTeacher'),
    path('updateLesson', updateLesson.as_view(), name='updateLesson'),
    path('updateMaterial', updateMaterial.as_view(), name='updateMaterial'),
    path('getUser', getUser.as_view(), name='getUser'),
    path('getCourseByUser', getCourseByUser.as_view(), name='getCourseByUser'),
    path('getCourseForUser', getCourseForUser.as_view(), name='getCourseForUser'),
    path('getDone', getDoneUserProgress.as_view(), name='getDone'),
    path('getCourseForMain', getCourseForMain.as_view(), name='getCourseForMain'),
    path('sendEmailToAdmin', sendEmailToAdmin.as_view(), name='sendEmailToAdmin'),
    path('getTeachers', getTeachers.as_view(), name='getTeachers'),
    path('deleteTeacher', deleteTeacher.as_view(), name='deleteTeacher'),
    path('getFeedback', getFeedback.as_view(), name='getFeedback'),
    path('createComment', createComment.as_view(), name='createComment'),
    path('parseFile', parseFile.as_view(), name='parseFile'),
    path('welcomeToTeacher', welcomeToTeacher.as_view(), name='welcomeToTeacher'),
]