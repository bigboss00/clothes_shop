# отвечает за настройку моделей
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    # избежание дублирования кода
    def _create(self, email, password, name, **extra_fields):
        # проверка, есть ли email
        if not email:
            raise ValueError('Email не может быть пустым')
        # разбивает на части и приводит к стандартному виду
        email = self.normalize_email(email)
        # создается пользователь
        user = self.model(email=email, name=name, **extra_fields)
        # шифровка пароля
        user.set_password(password)
        # сохраняет пароль в БД(так же может изменять)
        user.save()
        return user

    # создание обычного пользователя
    def create_user(self, email, password, name, **extra_fields):
        # устанавливается значение по умолчанию
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        return self._create(email, password, name, **extra_fields)

    # создание админа
    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, name, **extra_fields)


# модель пользователя
class User(AbstractBaseUser):
    email = models.EmailField('Электронная почта', primary_key=True)
    name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    is_active = models.BooleanField('Активный?', default=False)
    is_staff = models.BooleanField('Aдмин?', default=False)
    activation_code = models.CharField('Код активации', max_length=8, blank=True)

    # привязка менеджера
    objects = UserManager()

    # указывает поле, которое будет использоваться как логин
    USERNAME_FIELD = 'email'
    # указываются обязательные поля, кроме username и password
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    # какие пользователи могут иметь доступ к админ панели и к действия в ней(только с разрешения is_staff)
    def has_module_perms(self, app_label):
        return self.is_staff
    # дает доступ в целом
    def has_perm(self, obj=None):
        return self.is_staff

    # создает код активации
    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        self.activation_code = get_random_string(6)
        self.save()

    # отправляет письмо активации
    def send_activation_mail(self):
        from django.core.mail import send_mail
        message = f'Ваш код активации: {self.activation_code}'
        send_mail('Активация аккаунта', message, 'test@test.com', [self.email])
