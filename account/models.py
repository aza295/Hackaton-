from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import  AbstractUser
from django.db import models
import hashlib


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,email, password, ** extra_fields ):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)   #данный метод будет будет сохраннять пароль в хэшированном виде
        user.create_activation_code()
        user.save(using=self._db)
        return user


    def create_superuser(self,email,password=None, **extra_fields ):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


"""Создаем модель пользователя"""
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code




# Draft Part
    # создает код активации
    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        self.activation_code = get_random_string(8)
        self.save()

    # отправляет письмо с активацией
    def send_activation_mail(self):
        from django.core.mail import send_mail
        message = f'Your activation code is: {self.activation_code}'
        send_mail('Account activation', message,'shrek@gmail.com',[self.email])







