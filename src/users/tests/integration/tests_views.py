from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser, Sector


class TestRegisterView(TestCase):
    def test_registration_get(self):
        response = self.client.get(reverse("users:register"))
        self.assertTemplateUsed(response, "users/register.html")
        self.assertEqual(response.status_code, 200)

    def test_registration_ok(self):
        data = {
            "status": "BENEVOLE",
            "username": "JD",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com",
            "password1": "1234AZERTY$",
            "password2": "1234AZERTY$",
        }

        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertRedirects(response, reverse("users:login"))

    def test_registration_fail(self):
        data = {
            "status": "BENEVOLE",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "1234AZERTY$",
            "password2": "1234AZERTY$",
        }

        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(response.status_code, 200)


class TestProfileView(TestCase):
    def setUp(self):
        Sector.objects.create(entitled="A")
        CustomUser.objects.create_user(
            username="inconnu1",
            email="inconnu1@mail.com",
            first_name="inconnu",
            last_name="1",
            password="1234AZERTY",
            status="BENEVOLE",
        )
        CustomUser.objects.create_user(
            username="inconnu2",
            email="inconnu2@mail.com",
            first_name="inconnu",
            last_name="2",
            password="1234AZERTY",
            status="ASSOCIATION",
        )

    def test_display_and_update_candidate_profile_ok(self):
        self.client.login(
            username="inconnu1",
            email="inconnu1@mail.com",
            password="1234AZERTY",
        )
        data = {
            "first_name": "john",
            "last_name": "doe",
            "avatar": "default.jpg",
            "web_site_url": "http://www.mon-site.com",
            "linkedin_url": "http://www.linkedin.com",
            "github_url": "http://www.github.com",
            "gitlab_url": "http://www.gitlab.com",
            "description": "bio",
            "address_1": "A",
            "address_2": "B",
            "city": "ZION",
            "zip_code": "99999",
        }

        response = self.client.post(reverse("users:profile"), data)
        self.assertRedirects(response, reverse("users:profile"), 302)

        user = CustomUser.objects.get(email="inconnu1@mail.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "DOE")
        self.assertEqual(user.candidateprofile.avatar, "default.jpg")
        self.assertEqual(
            user.candidateprofile.web_site_url,
            "http://www.mon-site.com",
        )
        self.assertEqual(
            user.candidateprofile.linkedin_url,
            "http://www.linkedin.com",
        )
        self.assertEqual(
            user.candidateprofile.github_url,
            "http://www.github.com",
        )
        self.assertEqual(
            user.candidateprofile.gitlab_url,
            "http://www.gitlab.com",
        )
        self.assertEqual(user.candidateprofile.description, "bio")
        self.assertEqual(user.candidateprofile.location.address_1, "A")
        self.assertEqual(user.candidateprofile.location.address_2, "B")
        self.assertEqual(user.candidateprofile.location.city, "ZION")
        self.assertEqual(user.candidateprofile.location.zip_code, "99999")

    def test_display_and_update_organization_profile_ok(self):
        self.client.login(
            username="inconnu2",
            email="inconnu2@mail.com",
            password="1234AZERTY",
        )
        data = {
            "first_name": "other john",
            "last_name": "other doe",
            "logo": "default.jpg",
            "denomination": "association",
            "description": "bio",
            "entitled": "A",
            "rna_code": "W999999999",
            "siret_code": "99999999999999",
            "email": "mail@mail.com",
            "phone_number": "0000000000",
            "web_site_url": "http://www.notre-site.com",
            "address_1": "A",
            "address_2": "B",
            "city": "ZION",
            "zip_code": "99999",
        }

        response = self.client.post(reverse("users:profile"), data)
        self.assertRedirects(response, reverse("users:profile"), 302)

        user = CustomUser.objects.get(email="inconnu2@mail.com")
        self.assertEqual(user.first_name, "Other john")
        self.assertEqual(user.last_name, "OTHER DOE")
        self.assertEqual(user.organizationprofile.logo, "default.jpg")
        self.assertEqual(user.organizationprofile.denomination, "association")
        self.assertEqual(user.organizationprofile.description, "bio")
        self.assertEqual(user.organizationprofile.sector.entitled, "A")
        self.assertEqual(user.organizationprofile.rna_code, "W999999999")
        self.assertEqual(user.organizationprofile.siret_code, "99999999999999")
        self.assertEqual(user.organizationprofile.email, "mail@mail.com")
        self.assertEqual(user.organizationprofile.phone_number, "0000000000")
        self.assertEqual(
            user.organizationprofile.web_site_url,
            "http://www.notre-site.com",
        )
        self.assertEqual(user.organizationprofile.location.address_1, "A")
        self.assertEqual(user.organizationprofile.location.address_2, "B")
        self.assertEqual(user.organizationprofile.location.city, "ZION")
        self.assertEqual(user.organizationprofile.location.zip_code, "99999")

    def test_display_profile_not_ok(self):
        self.client.logout()
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)
