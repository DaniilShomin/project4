from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View

from backend.tasks.models import Task

from .forms import CreateStatusForm
from .models import Status
from inertia import render as inertia_render
from inertia import location


class BaseStatusView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in.")
            )
        return super().dispatch(request, *args, **kwargs)


class IndexStatusesView(BaseStatusView):
    def get(self, request):
        statuses = Status.objects.all().order_by("id")
        return inertia_render(
            request, "Statuses", props={"statuses": statuses}
        )


class CreateStatusesView(BaseStatusView):
    def get(self, request):
        return self._render_form(request, data={})

    def post(self, request):
        form = CreateStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Status successfully created"))
            return location("/statuses/")
        return self._render_form(
            request, data={"error": form.errors.as_text()}
        )

    def _render_form(self, request, data):
        return inertia_render(request, "StatusesCreate", props=data)


class UpdateStatusesView(BaseStatusView):
    def get(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        return self._render_form(request, data={"status": status})

    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        form = CreateStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _("Status successfully updated"))
            return location("/statuses/")
        return self._render_form(
            request,
            data={"error": f"{form.errors.as_text()}", "status": status},
        )

    def _render_form(self, request, data):
        return inertia_render(
            request,
            "StatusesUpdate",
            props=data,
        )


class DeleteStatusesView(BaseStatusView):
    def get(self, request, pk):
        status = Status.objects.get(pk=pk)
        return inertia_render(
            request,
            "StatusesDelete",
            props={
                "status": status,
            },
        )

    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        print(status)
        if Task.objects.filter(status=status).exists():
            messages.error(
                request, _("Cannot delete status because it is in use")
            )
            return location("/statuses/")
        status.delete()
        messages.success(request, _("Status successfully deleted"))
        return location("/statuses/")
