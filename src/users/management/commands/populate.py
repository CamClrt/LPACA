"""Feed database with fake data in commande line"""

import datetime
import random

from django.core.management.base import BaseCommand
from factory.faker import faker

from users.factories import (  # isort:skip
    AvailabilityFactory,
    CandidateProfileFactory,
    LocationFactory,
    OrganizationProfileFactory,
    WishFactory,
)

fake = faker.Faker(locale="fr_FR")


class Command(BaseCommand):
    help = "Create fake data in database"

    def handle(self, *args, **kwargs):

        # generate Locations
        [
            LocationFactory(
                address_1=fake.street_address(),
                address_2=fake.text(max_nb_chars=25)[:-1],
                city=fake.city(),
                zip_code=fake.postcode(),
            )
            for _ in range(30)
        ]

        # generate availability
        [
            AvailabilityFactory(
                start_date=fake.date_between_dates(
                    datetime.date(2021, 8, 1),
                    datetime.date(2021, 12, 31),
                ),
                end_date=fake.date_between_dates(
                    datetime.date(2022, 1, 1),
                    datetime.date(2023, 12, 31),
                ),
                hour_per_session=fake.random_int(1, 7),
            )
            for _ in range(21)
        ]

        # generate organization's profile
        [
            OrganizationProfileFactory(
                denomination=fake.company(),
                rna_code=fake.bothify("W%%%%%%%%%"),
                siret_code=fake.bothify("%%%%%%%%%%%%%%"),
                email=fake.company_email(),
                phone_number=fake.random_number(10),
                description=fake.sentence(25),
                web_site_url=fake.url(),
            )
            for _ in range(5)
        ]

        # generate candidates profile
        [
            CandidateProfileFactory(
                linkedin_url=fake.url(),
                github_url=fake.url(),
                gitlab_url=fake.url(),
                description=fake.sentence(25),
                web_site_url=fake.url(),
                activities=[
                    fake.random_int(1, 13) for _ in range(random.randint(1, 5))
                ],
                availabilities=[
                    fake.random_int(1, 21) for _ in range(random.randint(0, 4))
                ],
            )
            for _ in range(30)
        ]

        # generate wishes
        [
            WishFactory(
                remote=fake.boolean(75),
                sectors=[
                    fake.random_int(1, 6)
                    for _ in range(
                        random.randint(1, 6),
                    )
                ],
            )
            for _ in range(30)
        ]
