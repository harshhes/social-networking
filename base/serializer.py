from .models import User, FriendRequest
from .utils import get_user

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset = User.objects.all())])
    password = serializers.CharField(write_only =True,required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password':{"Password fields didn't match"}})

        return attrs
    

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data.get('email', None),
            first_name = validated_data.get('first_name',None),
            last_name = validated_data.get('last_name', None)
            )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only =True,required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')


        
class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_joined')


    def to_representation(self, instance):
        representation  = super().to_representation(instance)
        
        if 'date_joined' in representation:
            representation['date_joined'] = instance.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        return representation
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_joined')


class SendFriendRequestSerializer(serializers.ModelSerializer):
    to_user =  serializers.EmailField(required=True)

    class Meta:
        model = FriendRequest
        fields = ("to_user",)


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = "__all__"

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        if 'id' in representation:
            representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
            representation['updated_at'] = instance.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            representation['from_user'] =  instance.from_user.email 
            representation['to_user'] = instance.to_user.email 
        return representation