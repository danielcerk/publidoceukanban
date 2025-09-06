from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from .models import Profile

from django.contrib.auth.hashers import make_password

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod

    def get_token(cls, user):

        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True, validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    password = serializers.CharField(
        write_only=True, required=True, 
    )

    class Meta:

        model = User
        fields = ('name', 
            'first_name', 'last_name', 
            'email', 'password')
        
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


    def create(self, validated_data):

        user = User.objects.create(
            name=validated_data['name'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Profile
        fields = '__all__'

        read_only_fields = [

            'id', 'user', 'created_at',
            'updated_at'

        ]
    
class AccountSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        
        model = User
        fields = (
            'id', 'name', 
            'first_name', 'last_name',
            'email','password', 'profile',
            'is_active', 'is_staff', 'is_superuser'
        )

        read_only_fields = (
            'id', 'is_staff', 'is_superuser',
            'created_at', 'updated_at'
        )

        extra_kwargs = {
            'name': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'is_active': {'required': False},
            'is_staff': {'required': False},
            'is_superuser': {'required': False},
            'email': {'required': False},
            'password': {'required': False},
        }

    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)
        profile_data = validated_data.pop("profile", None)

        if password:

            instance.password = make_password(password)

        for attr in ('name', 'first_name', 'last_name', 'email', 'is_active'):

            if attr in validated_data:

                setattr(instance, attr, validated_data[attr])

        instance.save()

        if profile_data:

            profile_serializer = ProfileSerializer(
                instance.profile,
                data=profile_data,
                partial=True,
                context=self.context
            )

            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        return instance
