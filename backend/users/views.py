from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from backend.tasks.models import Task
from backend.users.forms import CreateUserForm
from backend.users.models import User
from inertia import render as inertia_render
from inertia import location


class BaseUserView(LoginRequiredMixin, View):
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in.")
            )
        return super().dispatch(request, *args, **kwargs)


class IndexUserView(View):
    def get(self, request):
        users = User.objects.all().order_by("id")
        return inertia_render(
            request,
            "Users",
            props={"users": users},
        )


class CreateUserView(View):
    def get(self, request):
        return self._render_form(request, data={})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(request, _("User registered successfully"))
            return location("/login/")
        return self._render_form(
            request, data={"error": f"{form.errors.as_text()}"}
        )

    def _render_form(self, request, data):
        print(data)
        return inertia_render(request, "Registration", props=data)


class UpdateUserView(BaseUserView):
    def get(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return location("/users/")
        return self._render_form(request, data={"user": user})

    def post(self, request, pk):
        user = self._get_user(pk)
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            updated_user.set_password(form.cleaned_data["password1"])
            updated_user.save()
            messages.success(request, _("User successfully changed."))
            return location("/")
        return self._render_form(
            request, data={"user": user, "error": f"{form.errors.as_text()}"}
        )

    def _get_user(self, user_id):
        user = get_object_or_404(User, id=user_id)
        auth_user_id = self.request.user.id

        if auth_user_id != int(user_id) and not self.request.user.is_superuser:
            messages.error(
                self.request,
                _("You do not have permission to change another user."),
            )
            return None
        return user

    def _render_form(self, request, data):
        return inertia_render(request, "UsersUpdate", props=data)


class DeleteUserView(BaseUserView):
    def get(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return location("/users/")
        return inertia_render(request, "UsersDelete", props={"user": user})

    def post(self, request, pk):
        user = self._get_user(pk)
        if Task.objects.filter(executor=user).exists():
            messages.error(
                request, _("Cannot delete user because it is in use")
            )
            return location("/users/")
        user.delete()
        messages.success(request, _("User successfully deleted"))
        return location("/users")

    def _get_user(self, user_id):
        user = get_object_or_404(User, id=user_id)
        auth_user_id = self.request.user.id

        if auth_user_id != int(user_id) and not self.request.user.is_superuser:
            messages.error(
                self.request,
                _("You do not have permission to change another user."),
            )
            return None
        return user
