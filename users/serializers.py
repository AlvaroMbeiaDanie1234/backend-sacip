from rest_framework import serializers
from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'roles', 'first_name', 'last_name', 'is_active')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'roles', 'first_name', 'last_name')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        roles = validated_data.pop('roles')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        user.roles.set(roles)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()