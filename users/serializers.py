from rest_framework import serializers

from users.models import User
from users.tasks import send_verification_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined',
                  'is_verified_email')  # 'image'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='Повторите пароль:')

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        send_verification_email.delay(user.id)
        return user
