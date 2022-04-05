from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import CandidateProfile, OrganizationProfile, Sector

from .forms import (  # isort:skip
    LocationForm,
    CandidateProfileForm,
    OrganizationProfileForm,
    UserForm,
    UserRegistrationForm,
    SectorForm,
)


def register(request):
    """Display template and form to create `users.CustomUser` instance

    Returns:
        HttpRequest (class): display `users/register` template
        and `UserRegistrationForm` instance
    """

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    """Display template and form to read user data or update them from
    `users.CandidateProfile` instance or `users.OrganizationProfile` instance

    Returns:
        HttpResponseRedirect (class): HttpResponse subclasses
        to redirect user when the profile update is a success

        or

        HttpRequest (class): render() combines a given template with
        a given context dictionary and returns an HttpResponse object
    """
    user = request.user

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()

        if CandidateProfile.objects.filter(user=user.id).exists():
            candidate = request.user.candidateprofile
            candidate_form = CandidateProfileForm(
                request.POST, request.FILES, instance=candidate
            )
            location_form = LocationForm(
                request.POST,
                instance=candidate.location,
            )

            if candidate_form.is_valid() and location_form.is_valid():
                candidate_form.save()
                location_form.save()

        if OrganizationProfile.objects.filter(user=user.id).exists():
            organization = request.user.organizationprofile
            organization_form = OrganizationProfileForm(
                request.POST, request.FILES, instance=organization
            )
            location_form = LocationForm(
                request.POST,
                instance=organization.location,
            )

            if location_form.is_valid():
                location_form.save()

            organization_updated = organization_form.save(commit=False)
            organization_updated.sector = Sector.objects.get(
                entitled=request.POST["entitled"],
            )
            organization_updated.save()

        return HttpResponseRedirect(request.path)

    else:
        if CandidateProfile.objects.filter(user=user.id).exists():
            candidate = request.user.candidateprofile
            context = {
                "candidate_profile_form": CandidateProfileForm(
                    instance=candidate,
                ),
                "location_form": LocationForm(instance=candidate.location),
            }

        if OrganizationProfile.objects.filter(user=user.id).exists():
            organization = request.user.organizationprofile
            context = {
                "organization_profile_form": OrganizationProfileForm(
                    instance=organization
                ),
                "location_form": LocationForm(instance=organization.location),
                "sector_form": SectorForm(instance=organization.sector),
            }

        context["user_form"] = UserForm(instance=user)
        return render(request, "users/profile.html", context)
