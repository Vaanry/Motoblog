import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Motobike
from ..forms import MotobikeForm

User = get_user_model()


class MotoCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.moto = Motobike.objects.create(
            name='Тестовое название',
            manufacturer='Тестовая марка',
            model='Тестовая модель',
            description='Тестовое описание',
        )
        
        cls.form = MotobikeForm()
        
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client(SERVER_NAME='localhost')
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)
        
    def test_create_moto(self):
        """Валидная форма создает запись в Motobike."""
        tasks_count = Motobike.objects.count()  

        form_data = {
            'name': 'Тестовый заголовок',
            'manufacturer': 'Тестовая марка',
            'model': 'Тестовая модель',
            'description': 'Тестовое описание',
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('moto:create_moto'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('moto:catalog'))
        self.assertEqual(Motobike.objects.count(), tasks_count+1)
        
        self.assertTrue(
            Motobike.objects.filter(
                name='Тестовое название',
                manufacturer='Тестовая марка',
                model='Тестовая модель',
                description='Тестовое описание',
            ).exists()
        )
