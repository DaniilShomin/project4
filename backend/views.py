from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from inertia import render as inertia_render
from inertia import location

from backend.forms import LoginForm


class IndexView(View):
    def get(self, request):
        return inertia_render(request, "Index", props={})


class LoginView(View):
    def get(self, request):
        return self._render_form(request, data={})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, _("You are login"))
                return location("/")
            else:
                return self._render_form(
                    request,
                    data={
                        "error": "Пользователь с такими данными не найден",
                    },
                )
        return self._render_form(
            request,
            data={
                "error": f"{form.errors.as_text()}",
            },
        )

    def _render_form(self, request, data):
        return inertia_render(request, "Login", props=data)


class LogoutView(View):
    def get(self, request):
        return redirect("index")

    def post(self, request):
        logout(request)
        messages.info(request, _("You are logout"))
        return redirect("index")
