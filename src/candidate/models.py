from django.db import models


class Activity(models.Model):
    """
    Model for an activity related to CandidateProfile
    """

    class CandidateActivity(models.TextChoices):
        OTHER = "autres", "Autres"
        BDD = "base-de-donnees", "Base de données"
        BACK = "developpement-back-end", "Développement Back-end"
        FRONT = "developpement-front-end", "Développement Front-end"
        FULL = "developpement-full-stack", "Développement Full-Stack"
        PROJECT = "gestion-de-projet", "Gestion de projet"
        SOCIAL = (
            "gestion-de-site-reseaux-sociaux",
            "Gestion de site & réseaux sociaux",
        )  # noqa: E501
        MARKETING = "marketing", "Marketing"
        PRODUCT = "produit", "Produit"
        LEARNING = "pedagogie-formation", "Pédagogie & formation"
        ADS = "seo-sea", "SEO/SEA"
        SUPPORT = "support", "Support"
        SYSTEME = "systeme", "Système"

    name = models.CharField(
        verbose_name="compétences",
        max_length=(50),
        unique=True,
        blank=True,
        choices=CandidateActivity.choices,
    )

    def __str__(self):
        return self.get_name_display()
