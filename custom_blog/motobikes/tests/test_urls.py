from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Motobike

User = get_user_model()

class MotoURLTests(TestCase):
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
                 
    # Проверяем общедоступные страницы
    def test_pages_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        id = MotoURLTests.moto.id
        pages = [f'/motobikes/catalog/',
                 f'/motobikes/{id}/'
                 ]
        for page in pages:
            with self.subTest(field=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, 200)
        
    def test_moto_edit_url(self):
        id = MotoURLTests.moto.id
        pages = [f'/motobikes/{id}/edit/',
                 f'/motobikes/create_moto/'
                 ]
        for page in pages:
            with self.subTest(field=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, 200)

    def test_moto_edit_url_for_guest(self):
        id = MotoURLTests.moto.id
        pages = [f'/motobikes/{id}/edit/',
                 f'/motobikes/create_moto/'
                 ]
        for page in pages:
            with self.subTest(field=page):
                response = self.guest_client.get(page)
                self.assertRedirects(
                    response, f'/auth/login/?next={page}')
        
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        id = MotoURLTests.moto.id
        templates_url_names = {
            'moto/catalog.html': '/motobikes/catalog/',
            'moto/create.html': '/motobikes/create_moto/',
            'moto/detail.html': f'/motobikes/{id}/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
