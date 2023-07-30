from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)
    name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Адрес email уже зарегистрирован')
        return email

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, attrs):
        user = User.objects.create_user(**attrs)
        user.create_activation_code()
        user.send_activation_mail()
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=6, max_length=6, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Неправильный код')
        return code

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Код не совападает')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(username=email,
                                password=password,
                                request=request)
            if not user:
                raise serializers.ValidationError('Введены неверные данные')
        else:
            raise serializers.ValidationError('Email и пароль обязательны к заполнению')
        attrs['user'] = user
        return attrs
