from django.db import models


# Create your models here.
class Motobike(models.Model):
    name = models.CharField(max_length=20, verbose_name='Наименование')
    manufacturer = models.CharField(max_length=20, verbose_name='Производитель')
    model = models.CharField(max_length=20, verbose_name='Модель')
    description = models.TextField(verbose_name='Описание')
    foto = models.ImageField('Фото', upload_to='moto_images', blank=True)

    class Meta:
        verbose_name = 'мотоцикл'
        verbose_name_plural = 'Мотоциклы'
        ordering = ('manufacturer', 'model')

    def __str__(self):
        return self.name
