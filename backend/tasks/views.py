from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from backend.labels.models import Label
from backend.statuses.models import Status
from backend.tasks.filters import TaskFilter
from backend.tasks.forms import CreateTaskForm
from backend.tasks.models import Task
from inertia import render as inertia_render
from inertia import location

from backend.users.models import User


class BaseTaskView(LoginRequiredMixin, View):
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in.")
            )
        return super().dispatch(request, *args, **kwargs)


class IndexTaskView(BaseTaskView):
    def get(self, request):
        tasks = Task.objects.all()
        filterset = TaskFilter(request.GET, queryset=tasks, request=request)
        labels = Label.objects.all()
        users = User.objects.all()
        statuses = Status.objects.all()
        return inertia_render(
            request,
            "Tasks",
            props={
                "tasks": filterset.qs,
                "labels": labels,
                "users": users,
                "statuses": statuses,
                "filter": dict(request.GET),
            },
        )


class CreateTaskView(BaseTaskView):
    def get(self, request):
        labels = Label.objects.all()
        users = User.objects.all()
        statuses = Status.objects.all()
        return self._render_form(
            request,
            data={"labels": labels, "users": users, "statuses": statuses},
        )

    def post(self, request):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, _("Task successfully created"))
            return location("/tasks/")
        labels = Label.objects.all()
        users = User.objects.all()
        statuses = Status.objects.all()
        return self._render_form(
            request,
            data={
                "error": f"{form.errors.as_text()}",
                "labels": labels,
                "users": users,
                "statuses": statuses,
            },
        )

    def _render_form(self, request, data):
        return inertia_render(request, "TasksCreate", props=data)


class DeleteTaskView(BaseTaskView):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.author.id != request.user.id:
            messages.error(
                request, _("A task can only be deleted by its author.")
            )
            return location("/tasks/")
        return inertia_render(
            request,
            "TasksDelete",
            props={
                "task": task,
            },
        )

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        messages.success(request, _("Task successfully deleted"))
        return location("/tasks/")


class UpdateTaskView(BaseTaskView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        labels = Label.objects.all()
        users = User.objects.all()
        statuses = Status.objects.all()
        return self._render_form(
            request,
            data={
                "task": task,
                "labels": labels,
                "users": users,
                "statuses": statuses,
            },
        )

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _("Task successfully updated"))
            return location("/tasks/")
        return self._render_form(
            request, data={"task": task, "error": f"{form.errors.as_text()}"}
        )

    def _render_form(self, request, data):
        return inertia_render(request, "TasksUpdate", props=data)


class ShowTaskView(BaseTaskView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return inertia_render(request, "TasksShow", props={"task": task})
