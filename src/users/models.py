from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel
from PIL import Image


class Sector(models.Model):
    """
    Model for a sector, related to OrganizationProfile and Wish
    """

    class OrganizationSector(models.TextChoices):
        ASH = "ASH", "Action sociale, Santé, Humanitaire"
        CL = "CL", "Culture et loisirs"
        DD = "DD", "Défense des droits"
        EFI = "EFI", "Education, Formation, Insertion"
        S = "S", "Sports"
        A = "A", "Autres"

    entitled = models.CharField(
        "intitulé",
        max_length=(5),
        unique=True,
        blank=True,
        choices=OrganizationSector.choices,
    )

    def __str__(self):
        return self.entitled


class Location(TimeStampedModel):
    """
    Model for a location, related to Profile (abstract class)
    """

    address_1 = models.CharField(
        "adresse",
        max_length=250,
        blank=True,
    )
    address_2 = models.CharField(
        "complément d'adresse",
        max_length=250,
        blank=True,
    )

    city = models.CharField(
        "ville",
        max_length=50,
        blank=True,
    )
    zip_code = models.CharField(
        "code postale",
        max_length=5,
        blank=True,
    )

    def __str__(self):
        return f"{self.address_1}, {self.zip_code} {self.city}"

    def save(self, *args, **kwargs):
        self.city = self.city.upper()
        super().save(*args, **kwargs)


class CustomUser(AbstractUser):
    """
    Custom model for an user, related to Profile (abstract class)
    """

    class UserStatus(models.TextChoices):
        BENEVOLE = "BENEVOLE", "Un bénévole"
        ASSOCIATION = "ASSOCIATION", "Une association"

    status = models.CharField(
        "type de compte",
        max_length=15,
        choices=UserStatus.choices,
        blank=False,
    )

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "email",
        "status",
    ]

    def __str__(self):
        return f"{self.username}, {self.email}"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.upper()
        super().save(*args, **kwargs)


class Profile(TimeStampedModel):
    """
    Model for a profil, related to OrganizationProfile and CandidateProfile
    """

    user = models.OneToOneField(
        "users.CustomUser",
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        "users.Location",
        on_delete=models.SET_NULL,
        null=True,
    )
    description = models.TextField(
        "bio",
        max_length=500,
        blank=True,
    )
    web_site_url = models.URLField(
        "site",
        blank=True,
    )

    class Meta:
        abstract = True


class OrganizationProfile(Profile):
    """
    Model for an organization profile related to Sector
    """

    sector = models.ForeignKey(
        "users.Sector",
        on_delete=models.SET_NULL,
        null=True,
        related_name="organizationprofiles",
    )
    denomination = models.CharField(
        max_length=50,
        blank=True,
    )
    rna_code = models.CharField(
        "code RNA",
        max_length=10,
        blank=True,
    )
    siret_code = models.CharField(
        "code SIRET",
        max_length=14,
        blank=True,
    )
    email = models.EmailField(
        "email",
        blank=True,
    )
    phone_number = models.CharField(
        "téléphone",
        max_length=10,
        blank=True,
    )
    logo = models.ImageField(
        "logo",
        default="default.jpg",
        upload_to="organization",
    )

    def __str__(self):
        return f"{self.user}: {self.denomination}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)


class Availability(TimeStampedModel):
    """
    Model for a availability, related to CandidateProfile
    """

    class CandidateAvailability(models.TextChoices):
        OPTION_1 = "ponctuel", "Ponctuel"
        OPTION_2 = "journalier", "Chaque jour"
        OPTION_3 = "hebdomadaire", "Chaque semaine"
        OPTION_4 = "quinzomadaire", "Toutes les 2 semaines"
        OPTION_5 = "mensuel", "Chaque mois"
        OPTION_6 = "bimestriel", "Tous les 2 mois"
        OPTION_7 = "trimestriel", "Chaque trimestre"

    type = models.CharField(
        "récurrence",
        max_length=(50),
        choices=CandidateAvailability.choices,
    )
    start_date = models.DateField(
        "date de début",
    )
    end_date = models.DateField(
        "date de fin",
        blank=True,
        null=True,
    )
    hour_per_session = models.PositiveSmallIntegerField(
        "nombre d'heures par session",
    )

    def __str__(self):
        return f"{self.id}: {self.type}, {self.hour_per_session}h"


class CandidateProfile(Profile):
    """
    Model for a candidate profile related to Activity, Availability and Wish
    """

    activities = models.ManyToManyField(
        "candidate.Activity",
        related_name="candidates_as_activity",
    )
    availabilities = models.ManyToManyField(
        "users.Availability",
        related_name="candidates_as_availability",
    )
    linkedin_url = models.URLField(
        "Linkedin",
        blank=True,
    )
    github_url = models.URLField(
        "GitHub",
        blank=True,
    )
    gitlab_url = models.URLField(
        "GitLab",
        blank=True,
    )
    avatar = models.ImageField(
        "avatar",
        default="default.jpg",
        upload_to="candidate",
    )

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Wish(TimeStampedModel):
    """
    Model for a wish, related to CandidateProfile and Sector
    """

    class CandidateWish(models.TextChoices):
        OPTION_1 = "city", "Local"
        OPTION_2 = "department", "Départemental"
        OPTION_3 = "region", "Régional"
        OPTION_4 = "country", "National"

    candidate = models.OneToOneField(
        "users.CandidateProfile",
        on_delete=models.CASCADE,
    )
    sectors = models.ManyToManyField(
        "users.Sector",
        related_name="wishes_as_sector",
    )
    remote = models.BooleanField(
        "à distance",
        default=False,
    )
    scoop = models.CharField(
        "zone de déplacement",
        max_length=(20),
        blank=True,
        choices=CandidateWish.choices,
    )

    def __str__(self):
        return f"{self.candidate}: {self.remote}, {self.scoop}, {self.sector}"


def post_profile_save_receiver(sender, instance, created, **kwargs):
    """
    Create a candidate or organization profile when user is registered
    """
    if created:
        location = Location.objects.create(
            address_1="",
            address_2="",
            city="",
            zip_code="",
        )

        if instance.status == "BENEVOLE":
            CandidateProfile.objects.create(
                user=instance,
                location=location,
            )

        if instance.status == "ASSOCIATION":
            OrganizationProfile.objects.create(
                user=instance,
                location=location,
                sector=Sector.objects.get(entitled="A"),
            )


post_save.connect(
    post_profile_save_receiver,
    sender="users.CustomUser",
)
