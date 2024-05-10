import os
import shutil

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from root_app.settings import MEDIA_ROOT

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
        serializer.save(**updated_data)

    def perform_destroy(self, instance):
        # delete user dir from media
        if f'user_{instance.id}' in os.listdir(path=MEDIA_ROOT):
            shutil.rmtree(path=os.path.join(MEDIA_ROOT, f'user_{instance.id}'))
        instance.delete()


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsFileOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # temporarily not allowed
        raise MethodNotAllowed("PATCH or PUT")

    def perform_destroy(self, instance):
        instance.delete()
        # delete file from media dir
        os.remove(path=instance.file.path)
