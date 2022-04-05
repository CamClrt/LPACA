from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="JD",
            email="john.doe@mail.com",
            first_name="John",
            last_name="Doe",
            password="1234AZERTY$",
            status="BENEVOLE",
        )

    def test_create_simple_user_without_username(self):
        message = "The given username must be set"
        with self.assertRaisesMessage(ValueError, message):
            CustomUser.objects.create_user(
                username="",
                email="",
                first_name="Other",
                last_name="User",
                password="1234AZERTY$",
                status="BENEVOLE",
            )
