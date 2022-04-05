from django.urls import path
from django.views.generic import TemplateView

app_name = "home"

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="home/home.html"),
        name="home",
    ),
    path(
        "legal_notices",
        TemplateView.as_view(template_name="home/legal_notices.html"),
        name="legal_notices",
    ),
]
