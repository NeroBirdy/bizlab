from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import User, Course, CourseAndUser, UserProgress, Material, Lesson
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
import base64, json
from django.db.models import Q
import random, string
from django.core.mail import EmailMessage
import os
from django.http import FileResponse, Http404
from django.conf import settings

class Registration(APIView):
    def post(self, request):
        firstName = request.data.get('firstName')
        secondName = request.data.get('secondName')
        lastName = request.data.get('lastName')
        phoneNumber = request.data.get('phoneNumber')
        email = request.data.get('email')
        birthday = request.data.get('birthday')
        role=request.data.get('role')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        password = self.generatePassword()
        print(password)
        hashed_password = make_password(password)

        user = User.objects.create(
            firstName=firstName,
            secondName=secondName,
            lastName=lastName,
            phoneNumber=phoneNumber,
            email=email,
            password=hashed_password,
            birthday = birthday,
            role=role
        )
        email_message = EmailMessage(
                'Регистрация студента',
                f'Для авторизации вам понадобится ваш email и пароль - {password}, желаю потратить побольше денег на курсы искатель',
                to=[email]
            )
        email_message.send()

        return Response({'message': 'Регистрация успешна',},
                         status=status.HTTP_201_CREATED)

    def generatePassword(self, length=12):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits

        all_chars = lower + upper + digits 

        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits)
        ]

        password += random.choices(all_chars, k=length - 4)

        random.shuffle(password)

        return ''.join(password)
    

    
class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Неверное имя пользователя или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Авторизация успешна',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен успешно'}, status=status.HTTP_200_OK)
    
class getUsersByCourse(APIView):
    def get(self, request):
        users = []
        usrs = User.objects.all()

        for user in usrs:
            users.append({
                'id': user.id,
                'FIO': f'{user.secondName} {user.firstName} {user.lastName}',
                'email': user.email
            })

        return Response({'users': users}, status=status.HTTP_200_OK)
    
#Добавить пользователя на курс
class inviteUserOnCourse(APIView):
    def post(self, request):
        userId = request.data.get('userId')
        courseId = request.data.get('courseId')
        user = User.objects.get(id = userId)
        course = Course.objects.get(id = courseId)

        CourseAndUser.objects.create(user = user, course = course)

        lessons = Lesson.objects.filter(course = course)

        for lesson in lessons:
            UserProgress.objects.create(user = user, course = course, lesson = lesson)
        
        return Response(status=status.HTTP_201_CREATED)

#Создать урок
class createTask(APIView):
    def post(self, request):
        courseId = request.data.get('courseId')
        name = request.data.get('name')

        course = Course.objects.get(id = courseId)
        Lesson.objects.create(name = name, course = course)

        return Response(status=status.HTTP_201_CREATED)

#Создать материал
class createMaterial(APIView):
    def post(self, request):
        lessonId = request.data.get('lessonId')
        type = request.data.get('type')
        name = request.data.get('name')
        file = request.FILES.get('file')

        ext = os.path.splitext(file.name)[1]
        name = f'{name}{ext}'

        if type == 3:
            link = request.data.get('link')
            Material.objects.create(name = name, type = type, link = link, lesson = lesson)
            Response(status=status.HTTP_201_CREATED)

        lesson = Lesson.objects.get(id = lessonId)
        lessonName = lesson.name
        courseName = lesson.course.name

        target_directory = os.path.join(os.getcwd(), f'../files/courses/{courseName}/{lessonName}')
        os.makedirs(target_directory, exist_ok=True)

        target_path = os.path.join(target_directory, name)
        
        with open(target_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        Material.objects.create(name = name, type = type,file = f'../files/courses/{courseName}/{lessonName}/{name}', lesson = lesson)

        return Response(status=status.HTTP_201_CREATED)

#Курсы студента
class getCourseByUser(APIView):
    def get(self, request):
        userId = request.query_params.get('userId')
        user = User.objects.get(id = userId)

        courses = []
        crs = CourseAndUser.objects.filter(user = user)

        for courseAndUser in crs:
            course = courseAndUser.course
            userProgress = UserProgress.objects.filter(user = user, course = course, type__in = [1,2])
            done = userProgress.filter(done = True)
            progress = len(done) / len(userProgress) * 100
            courses.append({
                'id': course.id,
                'picture': course.picture,
                'name': course.name,
                'progress': progress
            })
        
        return Response({'courses': courses}, status=status.HTTP_200_OK)

#Курс студента
class getCourseForUser(APIView):
    def get(self, request):
        userId = request.query_params.get('userId')
        courseId = request.query_params.get('courseId')
        user = User.objects.get(id = userId)
        crs = Course.objects.get(id = courseId)
        
        course = {}
        lessons = Lesson.filter(course = crs)
        for lesson in lessons:
            mtrls = Material.objects.filter(lesson = lesson)
            materials = []
            for material in mtrls:
                if material.type == 3:
                    materials.append({
                        'id': material.id,
                        'name': material.name,
                        'type': material.type,
                        'link': material.link
                    })
                else:
                    materials.append({
                    'id': material.id,
                    'name': material.name,
                    'type': material.type,
                    'file': material.file
                })
            course[lesson.name] = materials

            return Response({'course': course}, status=status.HTTP_200_OK)

#Скачать файл
class downloadFile(APIView):
    def post(self, request):
        filePath = request.data.get('path')
        
        if os.path.exists(filePath):
            return FileResponse(open(filePath, 'rb'), as_attachment=True)
        else:
            raise Http404("Файл не найден")
        
#Прикрепить файл
class uploadFile(APIView):
    def post(self, request):
        userId = request.data.get('userId')
        lessonId = request.data.get('lessonId')
        file = request.FILES.get('file')

        user = Lesson.objects.get(id = userId)
        lesson = Lesson.objects.get(id = lessonId)
        lessonName = lesson.name
        courseName = lesson.course.name

        target_directory = os.path.join(os.getcwd(), f'../files/users/{userId}/{courseName}/{lessonName}')
        os.makedirs(target_directory, exist_ok=True)

        target_path = os.path.join(target_directory, file.name)
        
        with open(target_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        userProgress = UserProgress.objects.get(user = user, lesson = lesson)
        userProgress.file = f'./files/users/{userId}/{courseName}/{lessonName}/{file.name}'
        userProgress.needToCheck = True
        userProgress.save()

        return Response(status=status.HTTP_200_OK)
    
#Домашка для проверки
class getFilesForTeacher(APIView):
    def post(self, request):
        courseId = request.data.get('courseId')
        course = Course.objects.get(id = courseId)

        userProgress = UserProgress.objects.filter(course = course, needToCheck = True)
        homeworks = []

        for progress in userProgress:
            user = progress.user
            fio = f'{user.secondName} {user.firstName} {user.lastName}'
            lesson = progress.lesson
            material = progress.material
            file = progress.file
            homeworks.append({
                'id': progress.id,
                'fio': fio,
                'lessonName': lesson.name,
                'materialName': material.name,
                'file': file
            })
        
        return Response({'homeworks': homeworks}, status=status.HTTP_200_OK)
    
#Кнопка проверки
class checked(APIView):
    def post(self, request):
        userProgressId = request.date.get('userProgressId')

        userProgress = UserProgress.objects.get(userProgressId)

        userProgress.needToCheck = False
        userProgress.done = True
        userProgress.save()

        return Response(status=status.HTTP_200_OK)
    
#Учебные материалы для учителя


#Редактирование учебных материалов
        



        



                






