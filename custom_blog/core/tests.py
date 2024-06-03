from django.test import TestCase, Client

class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client(SERVER_NAME='localhost')

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса /page/about/."""
        response = self.guest_client.get('/pages/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/about/."""
        response = self.guest_client.get('/pages/about/')
        self.assertTemplateUsed(response, 'pages/about.html')
        
    def test_rules_url_exists_at_desired_location(self):
        """Проверка доступности адреса /page/rules/."""
        response = self.guest_client.get('/pages/rules/')
        self.assertEqual(response.status_code, 200)

    def test_rules_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/rules/."""
        response = self.guest_client.get('/pages/rules/')
        self.assertTemplateUsed(response, 'pages/rules.html')
