from django.test import Client, TestCase
from django.urls import reverse


class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse("users:register"))

    def test_display_register_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "users/register.html")
        self.assertContains(self.response, "status")
        self.assertContains(self.response, "first_name")
        self.assertContains(self.response, "last_name")
        self.assertContains(self.response, "email")
        self.assertContains(self.response, "password1")
        self.assertContains(self.response, "password2")
