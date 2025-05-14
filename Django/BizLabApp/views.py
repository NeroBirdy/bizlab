from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import User, Course, CourseAndUser
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
import base64, json
from django.db.models import Q
import random, string
from django.core.mail import EmailMessage

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
                'FIO': f'{user.secondName} {user.firstName} {user.lastName}',
                'email': user.email
            })

        return Response({'users': users}, status=status.HTTP_200_OK)
    
# class createTask(APIView):
#     def post(self, request):
#         name = request.data.get('name')




