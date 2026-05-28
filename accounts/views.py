from django.contrib.auth import login
from django.shortcuts import redirect, render

from accounts.forms import RegistrationForm
from accounts.services.auth_service import AuthService


def register(request):
    if request.user.is_authenticated:
        return redirect("movie_list")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = AuthService().register(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            login(request, user)
            return redirect("movie_list")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})
