from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Post, Category, Location, Comments

User = get_user_model()
today = date.today()


class PostTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.category = Category.objects.create(
            title='Тестовая категория',
            description='Тестовое описание',
            slug='Тестовый слаг',
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

    def test_post_have_correct_object_names(self):
        task = PostTest.post
        expected_object_name = task.title
        self.assertEqual(expected_object_name, str(task))

    def test_category_have_correct_object_names(self):
        task = PostTest.category
        expected_object_name = task.title
        self.assertEqual(expected_object_name, str(task))

    def test_location_have_correct_object_names(self):
        task = PostTest.location
        expected_object_name = task.name
        self.assertEqual(expected_object_name, str(task))

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = PostTest.post
        field_verboses = {
            'title': 'Заголовок',
            'text': 'Текст',
            'pub_date': 'Дата и время публикации',
            'author': 'Автор публикации',
            'location': 'Местоположение',
            'category': 'Категория',
            'image': 'Фото',
            'is_published': 'Опубликовано',
            'created_at': 'Добавлено'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)
