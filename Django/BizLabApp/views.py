from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import User, Course, CourseAndUser, UserProgress, Material, Lesson, Compound
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
from urllib.parse import quote

class Registration(APIView):
    def post(self, request):
        firstName = request.data.get('firstName')
        secondName = request.data.get('secondName')
        lastName = request.data.get('lastName')
        email = request.data.get('email')
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
            email=email,
            password=hashed_password,
            role=role
        )
        if role == 0:
            email_message = EmailMessage(
                    'Регистрация студента',
                    f'Для авторизации вам понадобится ваш email и пароль - {password}, желаю потратить побольше денег на курсы искатель',
                    to=[email]
                )
        else:
            email_message = EmailMessage(
                'Регистрация учителя',
                f'Для авторизации вам понадобится ваш email и пароль - {password}, желаю приобрести побольше денег на родителях бедных детишек',
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
        courseId = request.query_params.get('courseId')

        course = Course.objects.get(id = courseId)

        existing_user_ids = CourseAndUser.objects.filter(course=course).values_list('user_id', flat=True)
        usrs = User.objects.exclude(id__in=existing_user_ids).filter(role = 0)
        users = []
    
        for user in usrs:
            users.append({
                'id': user.id,
                'FIO': f'{user.secondName} {user.firstName} {user.lastName}',
                'email': user.email
            })
        print(users)
        return Response({'users': users}, status=status.HTTP_200_OK)
    
class getUser(APIView):
    def post(self, request):
        userId = request.data.get('userId')

        user = User.objects.get(id = userId)

        return Response({'role': user.role}, status=status.HTTP_200_OK)
    
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
            materials = Material.objects.filter(lesson = lesson)
            for material in materials:
                UserProgress.objects.create(user = user, course = course, lesson = lesson, material = material)
        
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
        courseId = request.data.get('courseId')
        lessonName = request.data.get('lessonName')
        type = request.data.get('type')
        name = request.data.get('name')
        file = request.FILES.get('file')

        course = Course.objects.get(id = courseId)

        lesson = Lesson.objects.get(course = course, name = lessonName)


        if type == '4':
            link = request.data.get('link')
            material = Material.objects.create(name = name, type = type, link = link, lesson = lesson)

            return Response(status=status.HTTP_201_CREATED)

        ext = os.path.splitext(file.name)[1]
        fileName = f'{name}{ext}'

        lessonName = lesson.name
        courseName = lesson.course.name

        target_directory = os.path.join(os.getcwd(), f'../files/courses/{courseName}/{lessonName}')
        os.makedirs(target_directory, exist_ok=True)

        target_path = os.path.join(target_directory, fileName)
        
        with open(target_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        material = Material.objects.create(name = name, type = type,file = f'../files/courses/{courseName}/{lessonName}/{fileName}', lesson = lesson)
        if type != 1:
            usersOnCourse = CourseAndUser.objects.filter(course = course)
            for userOnCourse in usersOnCourse:
                UserProgress.objects.create(user = userOnCourse.user, course = course, lesson = lesson, material = material)

        tmp = {
            'name': name,
            'type': type,
            'id': material.id
        }
        return Response({'material': tmp},status=status.HTTP_201_CREATED)
    
#Создать курс
class createCourse(APIView):
    def post(self, request):
        teacherId = request.data.get('userId')
        name = request.data.get('name')
        description = request.data.get('description')
        places = request.data.get('places')
        price = request.data.get('price')
        salePrice = request.data.get('salePrice')
        sale = request.data.get('sale')
        credit = request.data.get('credit')
        picture = request.FILES.get('picture')
        compounds = json.loads(request.data.get('compounds'))
        teacher = User.objects.get(id = teacherId)

        if Course.objects.filter(name=name).exists():
                return Response(
                    {'error': 'Курс с таким названием уже существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        ext = os.path.splitext(picture.name)[1]
        picName = f'{name}{ext}'

        target_directory = os.path.join(os.getcwd(), f'../nuxt-app/public/images/courses')
        os.makedirs(target_directory, exist_ok=True)

        target_path = os.path.join(target_directory, picName)
        
        with open(target_path, 'wb') as destination:
            for chunk in picture.chunks():
                destination.write(chunk)

        course = Course.objects.create(teacher = teacher, name = name, description = description, places = places, price = price,
                              salePrice = salePrice, sale = sale, credit = credit, picture = f'/images/courses/{picName}')
        
        for compound in compounds:
            Compound.objects.create(course = course, name = compound)

        return Response(status=status.HTTP_201_CREATED)


#Курсы студента
class getCourseByUser(APIView):
    def post(self, request):
        userId = request.data.get('userId')
        user = User.objects.get(id = userId)

        courses = []
        crs = CourseAndUser.objects.filter(user = user)

        for courseAndUser in crs:
            course = courseAndUser.course
            check = UserProgress.objects.filter(user=user,course=course).exists()
            if check:
            
                userProgress = UserProgress.objects.filter(user = user, course = course)
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
        lessons = Lesson.objects.filter(course = crs)
        for lesson in lessons:
            mtrls = Material.objects.filter(lesson = lesson)
            materials = []
            for material in mtrls:
                if material.type == '4':
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
        file_path = request.data.get('path')

        if not os.path.exists(file_path):
            raise Http404("Файл не найден")

        # Получаем имя файла из пути
        file_name = os.path.basename(file_path)

        # Открываем файл
        file = open(file_path, 'rb')

        # Создаём ответ с файлом
        response = FileResponse(file)

        # Устанавливаем Content-Disposition для скачивания с оригинальным названием
        response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}'

        return response
        
#Прикрепить файл
class uploadFile(APIView):
    def post(self, request):
        userId = request.data.get('userId')
        materialId = request.data.get('materialId')
        file = request.FILES.get('file')

        user = User.objects.get(id = userId)
        material = Material.objects.get(id = materialId)
        lesson = material.lesson
        lessonName = lesson.name
        courseName = lesson.course.name

        target_directory = os.path.join(os.getcwd(), f'../files/users/{userId}/{courseName}/{lessonName}')
        os.makedirs(target_directory, exist_ok=True)

        target_path = os.path.join(target_directory, file.name)
        
        with open(target_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        userProgress = UserProgress.objects.get(user = user, lesson = lesson, material = material)
        userProgress.file = f'../files/users/{userId}/{courseName}/{lessonName}/{file.name}'
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
        userProgressId = request.data.get('userProgressId')

        userProgress = UserProgress.objects.get(id = userProgressId)

        userProgress.needToCheck = False
        userProgress.done = True
        userProgress.save()

        return Response(status=status.HTTP_200_OK)

#Курсы учителя
class getCoursesForTeacher(APIView):
    def get(self, request):
        teacherId = request.query_params.get('teacherId')
        teacher = User.objects.get(id = teacherId)

        crs = Course.objects.filter(teacher = teacher)

        courses = []

        for course in crs:
            needToCheck = UserProgress.objects.filter(course = course, needToCheck = True).count()
            courses.append({
                'id': course.id,
                'name': course.name,
                'needToCheck': needToCheck,
                'picture': course.picture
            })
        
        return Response({'courses': courses}, status=status.HTTP_200_OK)


#Учебные материалы для учителя
class getCourseForTeacher(APIView):
    def post(self, request):
        courseId = request.data.get('courseId')
        crs = Course.objects.get(id = courseId)

        course = {}
        lessons = Lesson.objects.filter(course = crs)
        for lesson in lessons:
            mtrls = Material.objects.filter(lesson = lesson)
            materials = []
            for material in mtrls:
                materials.append({
                    'id': material.id,
                    'name': material.name,
                    'type': material.type,
                    
                })
               
            course[lesson.name] = materials


        return Response({'course': course}, status=status.HTTP_200_OK)
    
class updateLesson(APIView):
    def post(self, request):
        courseId = request.data.get('courseId')
        lessonName = request.data.get('oldName')
        newName = request.data.get('newName')
        print(courseId)
        course = Course.objects.get(id = courseId)

        lesson = Lesson.objects.get(course = course,name = lessonName)
        lesson.name = newName

        lesson.save()

        return Response(status=status.HTTP_200_OK)
    
class updateMaterial(APIView):
    def post(self, request):
        materialId = request.data.get('materialId')
        newName = request.data.get('newName')

        material = Material.objects.get(id = materialId)
        material.name = newName

        material.save()

        return Response(status=status.HTTP_200_OK)


class getDoneUserProgress(APIView):
    def post(self, request):
        userId = request.data.get('userId')

        user = User.objects.get(id = userId)

        userProgress = UserProgress.objects.filter(user = user, done = True)

        materials = [progress.material.id for progress in userProgress]

        return Response({'materials': materials}, status=status.HTTP_200_OK)



        



        



                






