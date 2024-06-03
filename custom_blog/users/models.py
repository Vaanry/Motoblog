from django.contrib.auth.models import AbstractUser
from django.db import models
from motobikes.models import Motobike


class MotoUser(AbstractUser):
    foto = models.ImageField('Фото', upload_to='profile_images', blank=True)
    bio = models.TextField(verbose_name='Обо мне', blank=True)
    motobike = models.ManyToManyField(
        Motobike,
        verbose_name='Мотоцикл',
        related_name='bikes',
        through='Owners',
        help_text='''Нет вашего мотоцикла?<br>
        Вы можете его добавить на странице каталога.'''
    )


class Owners(models.Model):
    owner = models.ForeignKey(MotoUser, on_delete=models.CASCADE)
    motorbike = models.ForeignKey(Motobike, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'мотоцикл'
        verbose_name_plural = 'Мотоциклы'

    def __str__(self):
        return self.motorbike.name