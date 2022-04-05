from datetime import date

from django import forms

from candidate.models import Activity
from users.models import Availability, Sector, Wish

today = date.today()


class ActivityForm(forms.Form):
    """
    Form to display and update candidate's activities
    """

    name = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        label="",
        widget=forms.CheckboxSelectMultiple,
    )


class AvailabilityForm(forms.ModelForm):
    """
    Form to display and update candidate's availabilities
    """

    class Meta:
        model = Availability
        fields = [
            "type",
            "hour_per_session",
            "start_date",
            "end_date",
        ]
        labels = {
            "type": "Récurrence",
            "start_date": "Début",
            "end_date": "Fin (si connue)",
            "hour_per_session": "Nombre d'heure par session",
        }

        CURRENT_MONTHS = {
            1: ("jan"),
            2: ("feb"),
            3: ("mar"),
            4: ("apr"),
            5: ("may"),
            6: ("jun"),
            7: ("jul"),
            8: ("aug"),
            9: ("sep"),
            10: ("oct"),
            11: ("nov"),
            12: ("dec"),
        }

        current_month = []
        for month in range(1, today.month):
            del CURRENT_MONTHS[month]

        MONTHS = {
            1: ("jan"),
            2: ("feb"),
            3: ("mar"),
            4: ("apr"),
            5: ("may"),
            6: ("jun"),
            7: ("jul"),
            8: ("aug"),
            9: ("sep"),
            10: ("oct"),
            11: ("nov"),
            12: ("dec"),
        }

        HOURS_CHOICES = [
            ("1", "1 heure"),
            ("2", "2 heures"),
            ("3", "3 heures"),
            ("4", "4 heures"),
            ("5", "5 heures"),
            ("6", "6 heures"),
            ("7", "7 heures"),
        ]

        widgets = {
            "start_date": forms.SelectDateWidget(
                years=(today.year, (today.year + 1)),
                months=CURRENT_MONTHS,
            ),
            "end_date": forms.SelectDateWidget(
                years=(today.year, (today.year + 1)),
                months=MONTHS,
            ),
            "hour_per_session": forms.RadioSelect(choices=HOURS_CHOICES),
        }


class WishForm(forms.ModelForm):
    """
    Form to display and update candidate's wish
    """

    sector = forms.MultipleChoiceField(
        choices=Sector.OrganizationSector.choices,
        label="Secteur(s) d'activité (1 choix min)",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Wish
        fields = [
            "remote",
            "scoop",
            "sector",
        ]
        labels = {
            "remote": "A distance",
            "scoop": "Zone de déplacement possible",
        }
