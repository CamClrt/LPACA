"""Feed database with pre determined sectors"""

import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from users.models import Sector


class Command(BaseCommand):
    help = "Create sector in database"

    def handle(self, *args, **kwargs):
        logging.info("data insertion in DB: starting")
        try:
            Sector.objects.bulk_create(
                [
                    Sector(entitled="ASH"),
                    Sector(entitled="CL"),
                    Sector(entitled="DD"),
                    Sector(entitled="EFI"),
                    Sector(entitled="S"),
                    Sector(entitled="A"),
                ]
            )
        except IntegrityError:
            logging.warning("sector data already existed")
        logging.info("sector data insertion in DB: finished")
