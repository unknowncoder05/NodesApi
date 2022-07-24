from rest_framework import serializers
from api.utils.auth0.user import get_user as auth0_get_user
from .models import User
from .interfaces import Auth0User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', )
        read_only_fields = ('username', )

class DetailUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', )
        read_only_fields = ('username', )
    
    def to_representation(self, instance):
        ret = super(DetailUserSerializer, self).to_representation(instance)
        auth_token = self.context['request'].headers['Authorization'].replace('Bearer ', '')
        user = Auth0User(auth_token, self.context['request']._auth['sub'], instance)
        ret.update(
            user.data
        )
        print(user.data)
        return ret
    
    # def get_user_data():


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class Auth0CreateUserSerializer(serializers.ModelSerializer):

    key = serializers.CharField(write_only=True)
    user_sub = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        key = validated_data['key']
        user_sub = validated_data['user_sub']
        data = auth0_get_user(key, user_sub)

        user_data = dict(
            email=data['email'],
            username=data['nickname'],
            auth0_id=data['user_id'].split('|')[1],
        )
        user = User.objects.create_user(**user_data)
        return user
    

    class Meta:
        model = User
        fields = ('key', 'user_sub')
