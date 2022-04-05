import datetime

from django.test import TestCase
from django.urls import reverse

from candidate.models import Activity
from users.models import Availability, CustomUser, Sector


class TestDashboardView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="inconnu",
            email="inconnu@mail.com",
            password="1234AZERTY",
            first_name="John",
            last_name="Doe",
            status="BENEVOLE",
        )

    def test_display_dashboard_ok(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:dashboard"))
        self.assertTemplateUsed(response, "candidate/dashboard.html")
        self.assertEqual(response.status_code, 200)

    def test_display_dashboard_not_ok(self):
        response = self.client.get(reverse("candidate:dashboard"))
        self.assertEqual(response.status_code, 302)


class TestActivityView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="inconnu",
            email="inconnu@mail.com",
            password="1234AZERTY",
            first_name="John",
            last_name="Doe",
            status="BENEVOLE",
        )

    def test_get_activity_ok(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:activity"))
        self.assertTemplateUsed(response, "candidate/activity.html")
        self.assertEqual(response.status_code, 200)

    def test_get_activity_not_ok(self):
        response = self.client.get(reverse("candidate:activity"))
        self.assertEqual(response.status_code, 302)

    def test_post_activity_ok(self):
        Activity.objects.bulk_create(
            [
                Activity(name="autres"),
                Activity(name="base-de-donnees"),
                Activity(name="developpement-back-end"),
                Activity(name="developpement-front-end"),
            ]
        )
        self.client.force_login(self.user)
        data = {"name": [1, 2, 3, 4]}
        response = self.client.post(reverse("candidate:activity"), data)
        self.assertRedirects(response, reverse("candidate:dashboard"), 302)
        self.assertEqual(len(self.user.candidateprofile.activities.all()), 4)

        data = {"name": []}
        response = self.client.post(reverse("candidate:activity"), data)
        self.assertRedirects(response, reverse("candidate:dashboard"), 302)
        self.assertEqual(len(self.user.candidateprofile.activities.all()), 0)


class TestAvailabilityView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="inconnu",
            email="inconnu@mail.com",
            password="1234AZERTY",
            first_name="John",
            last_name="Doe",
            status="BENEVOLE",
        )

    def test_display_availability_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:availability"))
        self.assertTemplateUsed(response, "candidate/availability.html")
        self.assertEqual(response.status_code, 200)

    def test_display_availability_post(self):
        data = {
            "type": "ponctuel",
            "hour_per_session": "2",
            "start_date_day": "1",
            "start_date_month": "7",
            "start_date_year": "2021",
            "end_date_day": "",
            "end_date_month": "",
            "end_date_year": "",
        }
        self.client.force_login(self.user)
        response = self.client.post(reverse("candidate:availability"), data)
        self.assertRedirects(response, reverse("candidate:availability"), 302)
        self.assertEqual(
            len(self.user.candidateprofile.availabilities.all()), 1
        )  # noqa: E501

    def test_remove_availability(self):
        availability = Availability.objects.create(
            type="ponctuel",
            hour_per_session="2",
            start_date=datetime.date(2021, 8, 1),
            end_date=datetime.date(2022, 8, 1),
        )
        self.client.force_login(self.user)
        self.user.candidateprofile.availabilities.set([availability])
        self.assertEqual(
            len(self.user.candidateprofile.availabilities.all()), 1
        )  # noqa: E501
        self.client.get(
            reverse("candidate:remove_availability", args=(availability.id,))
        )
        self.assertEqual(
            len(self.user.candidateprofile.availabilities.all()), 0
        )  # noqa: E501


class TestWishView(TestCase):
    def setUp(self):
        Sector.objects.create(entitled="A")
        self.user = CustomUser.objects.create_user(
            username="inconnu",
            email="inconnu@mail.com",
            password="1234AZERTY",
            first_name="John",
            last_name="Doe",
            status="BENEVOLE",
        )

    def test_display_wish_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("candidate:wish"))
        self.assertTemplateUsed(response, "candidate/wish.html")
        self.assertEqual(response.status_code, 200)

    def test_display_wish_post(self):
        data = {
            "remote": "True",
            "scoop": "city",
            "sector": ["A"],
        }
        self.client.force_login(self.user)
        response = self.client.post(reverse("candidate:wish"), data)
        self.assertRedirects(response, reverse("candidate:dashboard"), 302)
        self.assertEqual(self.user.candidateprofile.wish.remote, True)
        self.assertEqual(self.user.candidateprofile.wish.scoop, "city")
        self.assertEqual(len(self.user.candidateprofile.wish.sectors.all()), 1)
