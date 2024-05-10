import os

from django.contrib.auth import get_user_model
from drf_base64.fields import Base64FileField
from rest_framework import serializers

from .models import File
from .utils import get_check_sum

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'date_joined',
                  'password', 'id']
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'date_joined': {'read_only': True},
                        'id': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FileSerializer(serializers.ModelSerializer):
    file = Base64FileField()

    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs = {'created_at': {'read_only': True},
                        'owner': {'read_only': True}}

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        old_path = instance.file.path
        new_file_name = f'file_{str(instance.id)}.txt'
        new_path = os.path.join(os.path.dirname(old_path), new_file_name)
        os.rename(src=old_path, dst=new_path)
        instance.file.name = os.path.join(os.path.dirname(instance.file.name),
                                          new_file_name)
        instance.file_name = new_file_name
        instance.check_sum = get_check_sum(new_path)
        instance.save()
