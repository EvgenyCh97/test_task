from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.owner_id, instance.file_name)


class File(models.Model):
    file_name = models.CharField(max_length=255, verbose_name='Имя файла',
                                 blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path,
                            verbose_name='Файл')
    check_sum = models.CharField(max_length=255,
                                 verbose_name='Контрольная сумма', blank=True,
                                 null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name
