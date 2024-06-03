from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Category, Location, Comments

User = get_user_model()
today = date.today()


class PostURLTests(TestCase):
    # Проверка URL
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.category = Category.objects.create(
            title='Тестовая категория',
            description='Тестовое описание',
            slug='test-slug',
        )

        cls.location = Location.objects.create(
            name='Тестовое наименование',
        )

        cls.post = Post.objects.create(
            title='Тестовая пост',
            text='Тестовый текст',
            pub_date=today,
            author=cls.user,
            location=cls.location,
            category=cls.category,
        )

        cls.comments = Comments.objects.create(
            text='Тестовый текст',
            post=cls.post,
            created_at=today,
            author=cls.user,
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client(SERVER_NAME='localhost')
        # Создаем пользователя
        self.user = PostURLTests.user
        # Создаем второй клиент
        self.authorized_client = Client(SERVER_NAME='localhost')
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_common_pages_exists(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        id = PostURLTests.post.id
        pages = ['/',
                 '/test-slug/',
                 f'/{id}/',
                 '/profile/auth/',]
        for page in pages:
            with self.subTest(field=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, 200)

    def test_post_list_url_exists_at_desired_location(self):
        """Страницы доступны авторизованным пользователям."""
        id = PostURLTests.post.id
        id_comm = PostURLTests.comments.id
        pages = [f'/{id}/',
                 '/create_post/',
                 f'/{id}/edit/',
                 f'/{id}/delete/',
                 f'/{id}/edit_comment/{id_comm}/',
                 f'/{id}/delete_comment/{id_comm}/']
        for page in pages:
            with self.subTest(field=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, 200)

    # Проверяем редиректы для неавторизованного пользователя
    def test_post_list_url_redirect_anonymous(self):
        """Страница перенаправляет анонимного пользователя."""
        id = PostURLTests.post.id
        id_comm = PostURLTests.comments.id
        pages = ['/create_post/',
                 f'/{id}/edit_comment/{id_comm}/',
                 f'/{id}/delete_comment/{id_comm}/']
        for page in pages:
            with self.subTest(field=page):
                response = self.guest_client.get(page, follow=True)
                self.assertRedirects(
                    response, (f'/auth/login/?next={page}'))

    def add_test_post_list_url_redirect_anonymous(self):
        """Страница перенаправляет анонимного пользователя."""
        username = PostURLTests.post.username
        page = [f'/edit/{username}/']
        response = self.guest_client.get(page, follow=True)
        self.assertRedirects(response, ('/auth/login/'))

    def test_post_list_url_403_anonymous(self):
        """Страница запрещает доступ."""
        id = PostURLTests.post.id
        pages = [f'/{id}/edit/',
                 f'/{id}/delete/']
        for page in pages:
            with self.subTest(field=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, 403)
