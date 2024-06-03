from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from ..models import Motobike

User = get_user_model()

class MotoViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.moto = Motobike.objects.create(
            name='Тестовое название',
            manufacturer='Тестовая марка',
            model='Тестовая модель',
            description='Тестовое описание',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client(SERVER_NAME='localhost')
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client(SERVER_NAME='localhost')
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)
        # Проверяем используемые шаблоны
        
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'moto/catalog.html': reverse('moto:catalog'),
            'moto/create.html': reverse('moto:create_moto'),
            'moto/detail.html': (
                reverse('moto:moto_detail', kwargs={'pk': '1'})
            ),

        }
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_create_moto_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('moto:create_moto'))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'name': forms.fields.CharField,
            'manufacturer': forms.fields.CharField,
            'model': forms.fields.CharField,
            'description': forms.fields.CharField,
        }
        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)
