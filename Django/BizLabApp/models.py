from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserManager(models.Manager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет обычного пользователя."""
        if not email:
            raise ValueError('Email должен быть указан')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)  # Поле для идентификации
    password = models.CharField(max_length=100)
    firstName = models.CharField(max_length=255)
    secondName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=11)
    birthday = models.DateField()
    role = models.CharField(max_length=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()  # Подключаем кастомный менеджер

    # Поля для Django
    USERNAME_FIELD = 'email'  # Используется для аутентификации
    REQUIRED_FIELDS = ['name']  # Дополнительные поля для createsuperuser

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        """Всегда возвращает True для авторизованных пользователей."""
        return True

    @property
    def is_anonymous(self):
        """Всегда возвращает False для авторизованных пользователей."""
        return False

    class Meta:
        db_table = 'users'
        managed = True

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    price = models.IntegerField()
    salePrice = models.IntegerField()
    credit = models.IntegerField()
    places = models.IntegerField()
    sale = models.CharField(max_length=255)

    class Meta:
        db_table = 'courses'
        managed = True

class Compound(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courseId')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'compounds'
        managed = True

class CourseAndUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userId_courseanduser')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courseId_courseanduser')

class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')

    class Meta:
        db_table = 'lessons'
        managed = True

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1)
    file = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials')

    class Meta:
        db_table = 'materials'
        managed = True

class UserProgress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userId_userprogress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='userprogress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lessonId')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='materialID')
    file = models.CharField(max_length=255)
    needToCheck = models.BooleanField(default=False)
    done = models.BooleanField(default=False)