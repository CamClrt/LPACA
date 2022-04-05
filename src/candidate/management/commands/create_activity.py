"""Feed database with pre determined activities"""

import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from candidate.models import Activity


class Command(BaseCommand):
    help = "Create activities in database"

    def handle(self, *args, **kwargs):
        logging.info("Create activities in database")
        try:
            Activity.objects.bulk_create(
                [
                    Activity(name="autres"),
                    Activity(name="base-de-donnees"),
                    Activity(name="developpement-back-end"),
                    Activity(name="developpement-front-end"),
                    Activity(name="developpement-full-stack"),
                    Activity(name="gestion-de-projet"),
                    Activity(name="gestion-de-site-reseaux-sociaux"),
                    Activity(name="marketing"),
                    Activity(name="produit"),
                    Activity(name="pedagogie-formation"),
                    Activity(name="seo-sea"),
                    Activity(name="support"),
                    Activity(name="systeme"),
                ]
            )
        except IntegrityError:
            logging.warning("activity data already existed")
        logging.info("activity data insertion in DB: finished")
        return
