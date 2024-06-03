from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post, Category, Location, Comments
from django import forms

User = get_user_model()
today = date.today()


class PostViewsTest(TestCase):
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
            title='Тестовый пост',
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
        self.user = PostViewsTest.user
        # Создаем второй клиент
        self.authorized_client = Client(SERVER_NAME='localhost')
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

        # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'blog/index.html': reverse('blog:index'),
            'blog/category.html': (
                reverse('blog:category_posts',
                        kwargs={'category_slug': 'test-slug'})
            ),
            'blog/create.html': reverse('blog:create_post'),
            'blog/detail.html': (
                reverse('blog:post_detail', kwargs={'pk': '1'})
            ),
            'blog/profile.html': (
                reverse('blog:profile', kwargs={'username': 'auth'})
            ),
            'blog/user.html': (
                reverse('blog:edit_profile', kwargs={'username': 'auth'})
            ),
            'blog/comment.html': (
                reverse('blog:edit_comment',
                        kwargs={'id': '1', 'pk': '1'})
            ),
        }
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_create_post_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('blog:create_post'))
        # Словарь ожидаемых типов полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'title': forms.fields.CharField,
            'text': forms.fields.CharField,
            'pub_date': forms.fields.DateTimeField,
            'image': forms.fields.ImageField,
        }
        # Проверяем, что типы полей формы в словаре context
        # соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    # Здесь создаются фикстуры: клиент и 13 тестовых записей.
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

        for i in range(13):
            cls.post = Post.objects.create(
                title=f'Тестовый пост {i}',
                text=f'Тестовый текст {i}',
                pub_date=today,
                author=cls.user,
                location=cls.location,
                category=cls.category,
            )

    def test_first_page_contains_ten_records(self):
        response = self.client.get(reverse('blog:index'))
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(response.context['object_list']), 10)

    def test_second_page_contains_three_records(self):
        # Проверка: на второй странице должно быть три поста.
        response = self.client.get(reverse('blog:index') + '?page=2')
        self.assertEqual(len(response.context['object_list']), 3)
