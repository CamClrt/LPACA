from django.urls import path

from .views import CandidateDetail, Dashboard

app_name = "organization"

urlpatterns = [
    path(
        "dashboard/",
        Dashboard.as_view(),
        name="dashboard",
    ),
    path(
        "details/<int:pk>/",
        CandidateDetail.as_view(),
        name="details",
    ),
]
