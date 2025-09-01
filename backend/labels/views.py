from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View

from backend.labels.forms import CreateLabelForm
from backend.labels.models import Label
from backend.tasks.models import Task
from inertia import render as inertia_render
from inertia import location


class BaseLabelsView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in.")
            )
        return super().dispatch(request, *args, **kwargs)


class IndexLabelsView(BaseLabelsView):
    def get(self, request):
        labels = Label.objects.all()
        return inertia_render(request, "Labels", props={"labels": labels})


class CreateLabelsView(BaseLabelsView):
    def get(self, request):
        return self._render_form(request, data={})

    def post(self, request):
        form = CreateLabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("The label was successfully created."))
            return redirect("labels:index")
        return self._render_form(
            request,
            data={"error": f"{form.errors.as_text()}"},
        )

    def _render_form(self, request, data):
        print(data)
        return inertia_render(request, "LabelsCreate", props=data)


class UpdateLabelsView(BaseLabelsView):
    def get(self, request, pk):
        label = get_object_or_404(Label, pk=pk)
        return self._render_form(
            request,
            data={"label": label},
        )

    def post(self, request, pk):
        label = get_object_or_404(Label, pk=pk)
        form = CreateLabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _("Label successfully updated"))
            return location("/labels/")
        return self._render_form(
            request,
            data={
                "label": label,
                "error": f"{form.errors.as_text()}",
            },
        )

    def _render_form(self, request, data):
        return inertia_render(
            request,
            "LabelsUpdate",
            props=data,
        )


class DeleteLabelsView(BaseLabelsView):
    def get(self, request, pk):
        label = Label.objects.get(pk=pk)
        return inertia_render(
            request,
            "LabelsDelete",
            props={
                "label": label,
            },
        )

    def post(self, request, pk):
        label = get_object_or_404(Label, pk=pk)
        if Task.objects.filter(labels=label).exists():
            messages.error(
                request, _("Cannot delete label because it is in use")
            )
            return location("/labels/")
        label.delete()
        messages.success(request, _("Label successfully deleted"))
        return location("/labels/")
