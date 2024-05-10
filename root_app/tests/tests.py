import os
import shutil

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from file_loader.models import File, User
from file_loader.views import FileViewSet, UserViewSet
from root_app.settings import MEDIA_ROOT


@pytest.fixture
def test_user():
    user = User.objects.create_user(username='test_user', password='testpass')
    return user


@pytest.mark.django_db
def test_user_viewset_get(test_user):
    factory = APIRequestFactory()
    view = UserViewSet.as_view({'get': 'retrieve'})
    request = factory.get(f'/users/{test_user.id}/')
    force_authenticate(request, user=test_user)

    response = view(request, pk=test_user.id)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_viewset_post(test_user):
    factory = APIRequestFactory()
    view = UserViewSet.as_view({'post': 'create'})
    request = factory.post('/users/',
                           {'username': 'new_user', 'password': 'newpass'})

    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_viewset_patch(test_user):
    factory = APIRequestFactory()
    view = UserViewSet.as_view({'patch': 'partial_update'})
    request = factory.patch(f'/users/{test_user.id}/',
                            {'first_name': 'new_name'})
    force_authenticate(request, user=test_user)

    response = view(request, pk=test_user.id)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_viewset_delete(test_user):
    factory = APIRequestFactory()
    view = UserViewSet.as_view({'delete': 'destroy'})
    request = factory.delete(f'/users/{test_user.id}/')
    force_authenticate(request, user=test_user)

    response = view(request, pk=test_user.id)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_file_viewset(test_user):
    factory = APIRequestFactory()
    # check create
    view = FileViewSet.as_view({'post': 'create'})
    request = factory.post('/files/',
                           {'file': 'data:@file/plain;base64,dGVzdA=='})
    force_authenticate(request, user=test_user)
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert File.objects.count() == 1
    file = File.objects.first()
    assert file.file_name == f'file_{file.id}.txt'
    assert file.owner == test_user

    # check read
    view = FileViewSet.as_view({'get': 'retrieve'})
    request = factory.get(f'/files/{file.id}/')
    force_authenticate(request, user=test_user)
    response = view(request, pk=file.id)
    assert response.status_code == status.HTTP_200_OK

    # check delete
    view = FileViewSet.as_view({'delete': 'destroy'})
    request = factory.delete(f'/files/{file.id}/')
    force_authenticate(request, user=test_user)
    response = view(request, pk=file.id)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # delete test_user dir after tests completed
    test_media_dir = os.path.join(str(MEDIA_ROOT), f'user_{test_user.id}')
    if os.path.exists(test_media_dir):
        shutil.rmtree(test_media_dir)
