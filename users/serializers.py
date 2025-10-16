from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'avatar', 'city', 'is_active']
        read_only_fields = ['id', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'avatar', 'city']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            avatar=validated_data.get('avatar'),
            city=validated_data.get('city'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
