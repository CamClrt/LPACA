from django.views.generic import DetailView, ListView

from users.models import CustomUser


class Dashboard(ListView):
    """Display template which contains a list of `users.CustomUser` instances
    Args:
        ListView (class): Render a list of `users.CustomUser` instances
    """

    queryset = CustomUser.objects.filter(status="BENEVOLE")
    template_name = "organization/dashboard.html"
    context_object_name = "users"
    paginate_by = 10


class CandidateDetail(DetailView):
    """Display template based on `users.CustomUser` instance
    Args:
        DetailView (class): Render details of `users.CustomUser` instance
    """

    queryset = CustomUser.objects.filter(status="BENEVOLE")
    template_name = "organization/details.html"
    context_object_name = "user"
