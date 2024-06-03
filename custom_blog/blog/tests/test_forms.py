import shutil
import tempfile
from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import CommentForm
from ..models import Post, Category, Location, Comments


User = get_user_model()
today = date.today()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
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
        cls.form = CommentForm()


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = PostCreateFormTests.user
        self.authorized_client = Client(SERVER_NAME='localhost')
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        comment_count = Comments.objects.count()

        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('blog:add_comment', kwargs={'pk': '1'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('blog:post_detail', kwargs={'pk': '1'}))
        self.assertEqual(Comments.objects.count(), comment_count + 1)
        self.assertTrue(
            Comments.objects.filter(
                text='Тестовый текст',
            ).exists()
        )
