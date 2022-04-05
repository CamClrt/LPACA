"""Feed database with fake data"""

import factory
from django.db.models import signals
from factory.faker import faker

from users.models import (  # isort:skip
    Availability,
    CandidateProfile,
    CustomUser,
    Location,
    Sector,
    Wish,
)

fake = faker.Faker(locale="fr_FR")


@factory.django.mute_signals(signals.post_save)
class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.CustomUser"
        django_get_or_create = (
            "username",
            "email",
            "status",
            "password",
            "first_name",
            "last_name",
        )
        abstract = True

    status = ""
    password = ""
    username = factory.Sequence(lambda n: "user%d" % n)

    @factory.lazy_attribute
    def first_name(self):
        return fake.first_name()

    @factory.lazy_attribute
    def last_name(self):
        return fake.last_name()

    @factory.lazy_attribute
    def email(self):
        return fake.ascii_free_email()


class CustomUserOrganizationFactory(CustomUserFactory):
    status = CustomUser.UserStatus.ASSOCIATION


class CustomUserCandidateFactory(CustomUserFactory):
    status = CustomUser.UserStatus.BENEVOLE


class OrganizationProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.OrganizationProfile"
        django_get_or_create = (
            "denomination",
            "rna_code",
            "siret_code",
            "email",
            "phone_number",
            "sector",
            "user",
            "location",
            "description",
            "web_site_url",
        )

    user = factory.SubFactory(
        "users.factories.CustomUserOrganizationFactory",
        organizationprofile=None,
    )
    sector = factory.Iterator(Sector.objects.all())
    location = factory.Iterator(Location.objects.all())


class CandidateProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.CandidateProfile"

    linkedin_url = ""
    github_url = ""
    gitlab_url = ""
    description = ""
    web_site_url = ""

    user = factory.SubFactory(
        "users.factories.CustomUserCandidateFactory",
        organizationprofile=None,
    )
    location = factory.Iterator(Location.objects.all())

    @factory.post_generation
    def availabilities(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.availabilities.add(group)

    @factory.post_generation
    def activities(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.activities.add(group)


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.Location"
        django_get_or_create = (
            "address_1",
            "address_2",
            "city",
            "zip_code",
        )


class AvailabilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.Availability"
        django_get_or_create = (
            "type",
            "start_date",
            "end_date",
            "hour_per_session",
        )

    type = factory.Iterator(
        [
            Availability.CandidateAvailability.OPTION_1,
            Availability.CandidateAvailability.OPTION_2,
            Availability.CandidateAvailability.OPTION_3,
            Availability.CandidateAvailability.OPTION_4,
            Availability.CandidateAvailability.OPTION_5,
            Availability.CandidateAvailability.OPTION_6,
            Availability.CandidateAvailability.OPTION_7,
        ]
    )


class WishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.Wish"

    remote = ""

    candidate = factory.Iterator(CandidateProfile.objects.all())

    scoop = factory.Iterator(
        [
            Wish.CandidateWish.OPTION_1,
            Wish.CandidateWish.OPTION_2,
            Wish.CandidateWish.OPTION_3,
            Wish.CandidateWish.OPTION_4,
        ]
    )

    @factory.post_generation
    def sectors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.sectors.add(group)
