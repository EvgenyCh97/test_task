import os
import shutil

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from file_loader.settings import MEDIA_ROOT

from .models import File
from .permissions import IsFileOwner, IsSameUser
from .serializers import FileSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSameUser]

    def perform_update(self, serializer):
        updated_data = self.request.data
        if (updated_data.get('username') and
                updated_data.get('username') != serializer.instance.username):
            # rename users media dir
            old_path = str(MEDIA_ROOT) + '\\' + serializer.instance.username
            new_path = '\\'.join(old_path.split('\\')[:-1] +
                                 [updated_data['username']])
            os.rename(src=old_path, dst=new_path)
            for user_file in serializer.instance.file_set.all():
                # rename file_path
                user_file.file_path = new_path + '\\' + user_file.file_name
                # rename 'file' field in File model
                url_path = str(user_file.file.name).split('/')
                url_path[0] = updated_data['username']
                user_file.file.name = '/'.join(url_path)
                user_file.save()
        serializer.save(**updated_data)

    def perform_destroy(self, instance):
        instance.delete()
        # delete user dir from media
        if instance.username in os.listdir(path=MEDIA_ROOT):
            shutil.rmtree(path=str(MEDIA_ROOT) + '\\' + instance.username)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        updated_data = self.request.data
        if updated_data.get('file'):
            # temporarily not allowed
            raise MethodNotAllowed("PATCH or PUT for 'file' field")
        # rename file_name in file path
        old_path = serializer.instance.file.path
        new_path = '\\'.join(old_path.split('\\')[:-1] +
                             [updated_data['file_name']])
        os.rename(src=old_path, dst=new_path)
        serializer.save(file='\\'.join(new_path.split('\\')[-2:]))

    def perform_destroy(self, instance):
        instance.delete()
        # delete file from media dir
        os.remove(path=instance.file.path)
