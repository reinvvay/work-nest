from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import QuerySet

from tasks.forms import TaskCreateForm
from tasks.models import Task


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "tasks/index.html")


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self) -> QuerySet[Task]:
        return (
            Task.objects
            .select_related("task_type")
            .prefetch_related("assignees")
            .order_by("is_completed", "deadline", "name")
        )


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form: TaskCreateForm) -> HttpResponse:
        return super().form_valid(form)


class TaskToggleView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return redirect("tasks:task_list")


class TaskDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect("tasks:task_list")


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self) -> QuerySet[Task]:
        return (
            Task.objects
            .select_related("task_type")
            .prefetch_related("assignees__position")
        )
